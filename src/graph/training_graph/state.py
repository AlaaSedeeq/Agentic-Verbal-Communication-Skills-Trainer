from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Annotated, Union, TypedDict
from langgraph.graph.message import add_messages, AnyMessage

from src.types import ImpromptuData, StoryData, ConflictResolutionData

class TrainingModuleState(BaseModel):
    name: Literal["impromptu", "storytelling", "conflict_resolution"]
    data: Union[ImpromptuData, StoryData, ConflictResolutionData]
    attempts: Optional[int] = 0
    start_time: str = Field(default_factory=lambda: datetime.now().isoformat())
    last_feedback: Optional[str] = None

class AssessmentModuleState(BaseModel):
    pass

class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    # completed_modules: Annotated[
    #     Literal["Impromptu Speaking", "Storytelling", "Conflict Resolution"], lambda x, y: list(set(x + y))
    #     ]
    training_sessions: List[Union[TrainingModuleState, AssessmentModuleState]]
    latest_module: Union[TrainingModuleState, AssessmentModuleState]
    start: str
