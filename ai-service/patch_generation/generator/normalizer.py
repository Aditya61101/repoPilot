from collections import defaultdict

def normalize_patch_plan(patch_plan, file_chunks):
    normalized = []
    seen_ids = set()

    # ---------- Step 1: basic validation + canonical fields ----------
    for i, step in enumerate(patch_plan):
        step = step.copy()

        path = step.get("file")
        start = step.get("start_line")
        end = step.get("end_line")

        if not path or path not in file_chunks:
            continue

        if start is None or end is None:
            continue

        if start > end:
            start, end = end, start

        # clamp to file length
        file_len = max(chunk["end_line"] for chunk in file_chunks[path])
        start = max(1, start)
        end = min(end, file_len)

        # ensure id
        if not step.get("id"):
            step["id"] = f"patch_{i+1}"

        if step["id"] in seen_ids:
            raise ValueError(f"Duplicate patch id: {step['id']}")

        seen_ids.add(step["id"])

        step["start_line"] = start
        step["end_line"] = end
        step["edit_type"] = step.get("edit_type", "modify")
        step["edit_strategy"] = step.get("edit_strategy", "")
        step["depends_on"] = list(step.get("depends_on", []))

        normalized.append(step)

    if not normalized:
        return []

    # ---------- Step 2: group patches per file ----------
    file_groups = defaultdict(list)

    for step in normalized:
        file_groups[step["file"]].append(step)

    merged = []

    # ---------- Step 3: merge overlapping patches ----------
    for path, steps in file_groups.items():

        steps.sort(key=lambda x: x["start_line"])

        current = steps[0]

        for nxt in steps[1:]:

            overlap = nxt["start_line"] <= current["end_line"]

            if overlap:

                # merge ranges
                current["end_line"] = max(
                    current["end_line"],
                    nxt["end_line"]
                )

                # merge dependencies
                deps = set(current["depends_on"]) | set(nxt["depends_on"])
                current["depends_on"] = list(deps)

                # combine strategies
                if nxt["edit_strategy"]:
                    current["edit_strategy"] += "\n" + nxt["edit_strategy"]

            else:
                merged.append(current)
                current = nxt

        merged.append(current)

    # ---------- Step 4: dependency cleanup ----------
    valid_ids = { step["id"] for step in merged }

    for step in merged:
        # remove invalid dependencies
        step["depends_on"] = [
            dep for dep in step["depends_on"]
            if dep in valid_ids
        ]

        # remove self dependency
        step["depends_on"] = [
            dep for dep in step["depends_on"]
            if dep != step["id"]
        ]

    # ---------- Step 5: deterministic ordering ----------
    merged.sort(
        key=lambda x: (
            x["file"],
            x["start_line"]
        )
    )

    return merged