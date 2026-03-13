# from concurrent.futures import ThreadPoolExecutor
from models.patch_generator import PatchSet
from rag.index_manager import get_index
from patch_generation.normalizer import normalize_patch_plan
from patch_generation.patch_scheduler import schedule_patch_plan
from patch_generation.generator import generate_batch_patches

def flatten_patch_results(patch_results):
    patches = []

    for p_id in sorted(patch_results.keys()):
        patch_set = patch_results[p_id]

        patches.extend(patch_set.patches)
    return PatchSet(patches=patches)

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
            file_chunks, 
            patch_lookup, 
            repo_state
        )
        for step, patch_set in zip(batch,responses):
            patch_results[step['id']]=patch_set

    # result aggregation
    final_patch_set = flatten_patch_results(patch_results)
    return final_patch_set.model_dump()
    # patches = []
    # def process_step(step):
    #     return generate_patch(
    #         issue=issue,
    #         step=step,
    #         file_chunks=file_chunks
    #     )
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     results = executor.map(process_step, patch_plan)

    # for patch in results:
    #     patches.append(patch)
    
    # return patches