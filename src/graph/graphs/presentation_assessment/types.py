from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class InputValidation(BaseModel):
    is_valid: bool
    issues: List[str] = Field(default_factory=list)
    correction_guidance: Optional[str] = None
    
    @classmethod
    def example(cls):
        return cls(
            is_valid=False,
            issues = ["too short", "no complete sentences"],
            correction_guidance = "Please add more content. Try to use complete sentences."
            )

class StructureEvaluation(BaseModel):
    intro_score: int = Field(1, ge=1, le=5)
    conclusion_score: int = Field(1, ge=1, le=5)
    transition_score: int = Field(1, ge=1, le=5)
    structure_comment: str

    @classmethod
    def example(cls):
        return cls(
            intro_score=3,
            conclusion_score=2,
            transition_score=4,
            structure_comment="Needs stronger conclusion"
        )

class DeliveryEvaluation(BaseModel):
    pacing_score: int = Field(1, ge=1, le=5)
    clarity_score: int = Field(1, ge=1, le=5)
    filler_words: List[str] = Field(default_factory=list)
    delivery_comment: str

    @classmethod
    def example(cls):
        return cls(
            pacing_score=4,
            clarity_score=3,
            filler_words=["um", "like"],
            delivery_comment="Good pace but needs to reduce fillers"
        )

class ContentEvaluation(BaseModel):
    relevance_score: int = Field(1, ge=1, le=5)
    persuasiveness_score: int = Field(1, ge=1, le=5)
    vocabulary_level: Literal["basic", "intermediate", "advanced"]
    content_comment: str

    @classmethod
    def example(cls):
        return cls(
            relevance_score=5,
            persuasiveness_score=4,
            vocabulary_level="intermediate",
            content_comment="Well-researched but needs more examples"
        )

class PresentationAssessmentEvaluation(BaseModel):
    structure: StructureEvaluation
    delivery: DeliveryEvaluation
    content: ContentEvaluation
    feedback: str

class PresentationAssessmentData(BaseModel):
    user_input: str
    user_transcript_validation: InputValidation
    user_transcript_evaluation: PresentationAssessmentEvaluation
    overall_score: float = 0.0
    priority_improvements: List[str] = Field(default_factory=list)
