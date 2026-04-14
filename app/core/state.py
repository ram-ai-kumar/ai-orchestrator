from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    # Input
    task: str

    # Planning
    plan: List[str]
    current_step: int

    # Retrieval context
    context: List[str]

    # Execution
    patch: Optional[str]

    # Validation
    review: Optional[str]
    approved: bool

    # Debug
    logs: List[str]
