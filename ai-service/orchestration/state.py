from typing import TypedDict, Optional

class GraphState(TypedDict, total=False):
    repo_key: str
    commit_sha: str
    is_indexed: bool
    
    issue: str

    analysis: dict
    patch_plan: list

    patch_set: dict
    patch_results: dict

    file_diffs: list

    file_reviews: list
    rejected_files: dict
    attempt: int

    pr_url: Optional[str]