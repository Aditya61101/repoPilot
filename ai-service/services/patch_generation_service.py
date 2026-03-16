from patch_generation.generator.applier import apply_patch_set_to_repo_state
from patch_generation.prompts import build_repair_prompt
from rag.index_manager import get_index
from models.patch_generator import Patch, PatchSet
from patch_generation.generator.symbol_parser.extract_symbol import extract_symbol_range
from patch_generation.validation.validate import validate_patch_set
from patch_generation.generator.normalizer import normalize_patch_plan
from patch_generation.generator.patch_scheduler import schedule_patch_plan
from patch_generation.generator.generator import generate_batch_patches, generator_llm
from constants import MAX_REPAIR_ATTEMPTS

def compute_patch(new_code, step, repo_state):
    start, end = extract_symbol_range(repo_state, step)
    patch = Patch(
        file=step['file'],
        edit_type=step['edit_type'],
        start_line=start,
        end_line=end,
        replacement=new_code
    )
    return PatchSet(patches=[patch])


def flatten_patch_results(patch_results):
    patches = []

    for p_id in sorted(patch_results.keys()):
        patch_set = patch_results[p_id]

        patches.extend(patch_set.patches)
    return PatchSet(patches=patches)

def validate_and_repair_batch(issue, patch_sets, repo_state):
    # patch_sets are the list of independent patches generated for the current batch
    validated = []
    for step, patch_set in patch_sets:
        ok, error = validate_patch_set(repo_state, patch_set)

        # retry loop
        attempts = 0
        while not ok and attempts < MAX_REPAIR_ATTEMPTS:
            print(f"Validation failed for patch {step['id']}, attempt {attempts+1}: {error}")
            # build repair prompt
            repair_prompt = build_repair_prompt(
                issue, 
                step, 
                new_code,
                error
            )
            # regenerate patch
            repair_response = generator_llm.invoke(repair_prompt)
            new_code = repair_response.model_dump()['updated_symbol_code']
            
            patch_set = compute_patch(new_code, step, repo_state)

            # re-validate
            ok, error = validate_patch_set(repo_state, patch_set)
            attempts += 1
        
        if not ok:
            raise RuntimeError(f"patch validation failed for: {error}")
        
        validated.append((step, patch_set))

    return validated

def patch_generation(repo_key, issue, patch_plan):

    repo_index = get_index(repo_key)
    file_chunks = repo_index['file_chunks']
    repo_graph  = repo_index['repo_graph']
    repo_state = repo_index['repo_state']
    
    # normalize patch plan
    patch_plan = normalize_patch_plan(patch_plan, file_chunks)
    patch_lookup = { p['id']:p for p in patch_plan }
    
    # schedule patch plan
    scheduled_patches = schedule_patch_plan(patch_plan, repo_graph)

    patch_results = {}
    for batch in scheduled_patches:
        responses = generate_batch_patches(
            issue, 
            batch, 
            patch_results,
            patch_lookup, 
            repo_state
        )
        
        # for each step, now we do syntax validation (for now), if it fails we do 2 retry attempts with a repair prompt that includes the error message, if it still fails after 2 attempts we raise an error and stop the process, otherwise we save the patch result and move on to the next step
        patch_sets = []
        for step, response in zip(batch,responses):
            new_code = response.model_dump()['updated_symbol_code']
            patch_set = compute_patch(new_code, step, repo_state)

            patch_sets.append(patch_set)

        validated_patches = validate_and_repair_batch(
            issue,
            patch_sets,
            repo_state
        )

        for step, patch_set in validated_patches: 
            patch_results[step['id']] = patch_set
            # apply patch to the repo_state
            apply_patch_set_to_repo_state(repo_state, patch_set)

    # result aggregation
    final_patch_set = flatten_patch_results(patch_results)
    return final_patch_set.model_dump()
