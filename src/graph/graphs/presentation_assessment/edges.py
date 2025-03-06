from typing_extensions import Literal
from src.graph.state import State

def route_validation(state: State) -> Literal["valid", "invalid"]:
    return "valid" if state["latest_module"].data.user_transcript_validation.is_valid else "invalid"
