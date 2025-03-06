from langchain_core.prompts import PromptTemplate

from src.graph.utils import create_chain, get_llms
from .types import (
    ImpromptuValidationResponse, 
    ImpromptuStructureEvaluationResponse, 
    ImpromptuFluencyEvaluationResponse
    )
from .prompts import (
    impromptu_validation_prompt,
    impromptu_validation_example,
    impromptu_structure_prompt,
    impromptu_structure_example,
    impromptu_fluency_prompt,
    impromptu_fluency_example,
    impromptu_feedback_prompt,
    impromptu_followup_prompt,
    impromptu_topic_prompt
)

text_llm_1, _ = get_llms(text_llm_config={"temperature": 0.1}, voice_llm_config={})
text_llm_7, _ = get_llms(text_llm_config={"temperature": 0.7}, voice_llm_config={})


# ======== Validation Chain ========
impromptu_validation_chain = create_chain(
    impromptu_validation_prompt,
    ImpromptuValidationResponse,
    impromptu_validation_example,
    text_llm_1
)

# ======== Structure Analysis Chain ========
impromptu_structure_analyzer = create_chain(
    impromptu_structure_prompt,
    ImpromptuStructureEvaluationResponse,
    impromptu_structure_example,
    text_llm_1
    )

# ======== Fluency Evaluation Chain ========
impromptu_fluency_evaluator = create_chain(
    impromptu_fluency_prompt,
    ImpromptuFluencyEvaluationResponse,
    impromptu_fluency_example,
    text_llm_1
)

# ======== Feedback Chain ========
impromptu_feedback_chain = (
    PromptTemplate.from_template(
        impromptu_feedback_prompt
    )
    | text_llm_7
)

# ======== Topic Generation Chain ========
impromptu_topic_chain = (
    PromptTemplate.from_template(
        impromptu_topic_prompt
    )
    | text_llm_7
)

# ======== Followup Chain ========
impromptu_followup_chain = (
    PromptTemplate.from_template(
        impromptu_followup_prompt
    )
    | text_llm_7
)
