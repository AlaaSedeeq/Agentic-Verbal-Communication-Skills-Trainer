from pydantic import BaseModel, Field
from typing import List, Literal

class ImpromptuValidationResponse(BaseModel):
    is_valid: bool = Field(
        ...,
        description="If the transcript meets basic validation"
    )
    invalid_reasons: List[str] = Field(
        default_factory=list,
        description=(
            "List of reasons why the content is invalid. Empty list if valid. "
            "Standardized reasons: off_topic, too_short, offensive, gibberish"
        )
    )
    followup_message: str = Field(
        ...,
        description="Brief, neutral message explaining why the content was rejected or a simple acknowledgment if valid"
    )

class ImpromptuStructureEvaluationResponse(BaseModel):
    score: int = Field(..., ge=1, le=10, description="Overall structure quality 1-10")
    has_intro: bool = Field(..., description="Clear introduction with thesis statement")
    has_conclusion: bool = Field(..., description="Defined ending summary/call-to-action")
    organization: Literal["chaotic", "adequate", "logical"]
    key_strength: str = Field(..., example="Good use of examples")
    to_improve: str = Field(..., example="Better transitions needed")

class ImpromptuFluencyEvaluationResponse(BaseModel):
    # pace: Literal["too slow", "ideal", "too fast"]
    filler_words: int = Field(..., ge=0, description="Count of filler words (uh/um/like, ..etc")
    clarity: Literal["mumbled", "clear", "excellent"]
    fluency_score: int = Field(..., ge=1, le=10)

class ImpromptuEvaluation(BaseModel):
    structure: ImpromptuStructureEvaluationResponse
    fluency: ImpromptuFluencyEvaluationResponse
    feedback: str

class ImpromptuData(BaseModel):
    topic: Literal[
        "Ethics and Philosophy", "Social Issues", "Technology and Innovation",
        "Leadership and Teamwork", "Personal Development", "General Knowledge"
    ]
    topic_title: str = Field(..., description="Generated topic title")
    user_input: str
    user_transcript_validation: ImpromptuValidationResponse
    user_transcript_evaluation: ImpromptuEvaluation
