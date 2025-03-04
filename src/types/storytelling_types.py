from pydantic import BaseModel, Field
from typing import List, Literal

class StoryValidationResponse(BaseModel):
    is_valid: bool = Field(..., description="If story meets basic requirements")
    invalid_reasons: List[str] = Field(
        default_factory=list,
        description=(
            "List of reasons why the content is invalid. Empty list if valid. "
            "Standardized reasons: off_genre, too_short, no_arc, disjointed, offensive"
        )
    )
    followup_message: str = Field(
        ...,
        description="Brief, neutral message explaining why the content was rejected or a simple acknowledgment if valid"
    )

class StoryNarrativeEvaluation(BaseModel):
    narrative_score: int = Field(..., ge=1, le=10)
    character_development: int = Field(..., ge=1, le=5)
    plot_complexity: int = Field(..., ge=1, le=5)
    literary_devices: List[str] = Field(..., example=["metaphor", "dialogue"])
    key_strength: str = Field(..., example="Strong character motivations")
    to_improve: str = Field(..., example="Add more sensory details")

class StoryEngagementEvaluation(BaseModel):
    engagement_score: int = Field(..., ge=1, le=10)
    hook_quality: Literal["weak", "adequate", "strong"]
    pacing_analysis: Literal["uneven", "consistent", "excellent"]
    reader_interest: Literal["low", "moderate", "high"]
    satisfaction: Literal["unsatisfying", "adequate", "fulfilling"]

class StoryEvaluation(BaseModel):
    narrative: StoryNarrativeEvaluation
    engagement: StoryEngagementEvaluation
    feedback: str

class StoryData(BaseModel):
    genre: Literal["personal", "fictional", "historical"]
    story_prompt: str
    user_transcript_validation: StoryValidationResponse
    user_transcript_evaluation: StoryEvaluation
