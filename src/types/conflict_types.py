from pydantic import BaseModel, Field
from typing import List, Literal

class ConflictValidationResponse(BaseModel):
    is_valid: bool = Field(..., description="If response meets basic requirements")
    invalid_reasons: List[Literal["off_topic", "aggressive", "avoidant", "vague"]] = Field(default_factory=list)
    followup_message: str = Field(..., description="Guidance for improvement")

class ConflictDiplomacyEvaluation(BaseModel):
    empathy_score: int = Field(..., ge=1, le=5)
    clarity_score: int = Field(..., ge=1, le=5)
    solution_focus: int = Field(..., ge=1, le=5)
    professionalism: Literal["poor", "adequate", "excellent"]
    negative_indicators: List[Literal["aggression", "avoidance", "blame"]]

class ConflictEvaluation(BaseModel):
    diplomacy: ConflictDiplomacyEvaluation
    feedback: str

class ConflictResolutionData(BaseModel):
    category: Literal[
        "Workplace/Professional", "Family Dynamics", "Community/Social",
        "Personal Relationships", "Educational/Academic"
        ]
    scenario: str
    user_transcript_validation: ConflictValidationResponse
    user_transcript_evaluation: ConflictEvaluation
