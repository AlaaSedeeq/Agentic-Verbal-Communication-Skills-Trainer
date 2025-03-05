from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Annotated, Union, TypedDict
from langgraph.graph.message import add_messages, AnyMessage

from src.graph.training_graph.graphs.skills_training.imrpomptu_speaking.types import ImpromptuData
from src.graph.training_graph.graphs.skills_training.storytelling_training.types import StoryData
from src.graph.training_graph.graphs.skills_training.conflict_resolution.types import ConflictResolutionData

class TrainingModuleState(BaseModel):
    name: Optional[Literal["impromptu", "storytelling", "conflict_resolution"]]
    data: Optional[Union[ImpromptuData, StoryData, ConflictResolutionData]]
    attempts: Optional[int] = 0
    start_time: str = Field(default_factory=lambda: datetime.now().isoformat())
    last_feedback: Optional[str] = None

class AssessmentModuleState(BaseModel):
    pass

class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    sessions: Optional[List[Union[TrainingModuleState, AssessmentModuleState]]]
    current_module: Optional[Union[TrainingModuleState, AssessmentModuleState]]
