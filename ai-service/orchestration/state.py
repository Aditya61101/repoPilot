from typing import TypedDict, Optional

class GraphState(TypedDict, total=False):
    repo_key: str
    commit_sha: str
    is_indexed: bool
    
    issue: str

    analysis: dict
    patch_plan: list

    patch_set: dict
    diff: str

    approved: bool
    feedback: Optional[str]
    pr_url: Optional[str]