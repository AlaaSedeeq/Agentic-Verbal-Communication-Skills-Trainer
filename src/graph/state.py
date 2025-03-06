from datetime import datetime
from typing import List, Literal, Optional, Annotated, Union
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict

from src.graph.graphs.skills_training.imrpomptu_speaking.types import ImpromptuData
from src.graph.graphs.skills_training.storytelling_training.types import StoryData
from src.graph.graphs.skills_training.conflict_resolution.types import ConflictResolutionData
from src.graph.graphs.presentation_assessment.types import PresentationAssessmentData

class TrainingModuleState(BaseModel):
    name: Literal["impromptu", "storytelling", "conflict_resolution"]
    data: Union[ImpromptuData, StoryData, ConflictResolutionData]
    attempts: Optional[int] = 0
    start_time: str = Field(default_factory=lambda: datetime.now().isoformat())
    last_feedback: Optional[str] = None

class AssessmentModuleState(BaseModel):
    name: str = "Assessment"
    data: PresentationAssessmentData
    start_time: str = Field(default_factory=lambda: datetime.now().isoformat())
    last_feedback: Optional[str] = None

class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    sessions: List[Union[TrainingModuleState, AssessmentModuleState]]
    latest_module: Union[TrainingModuleState, AssessmentModuleState]

