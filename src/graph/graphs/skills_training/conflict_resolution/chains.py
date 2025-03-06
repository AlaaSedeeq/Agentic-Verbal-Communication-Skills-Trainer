from langchain_core.prompts import PromptTemplate

from src.graph.utils import create_chain, get_llms
from .types import (
    ConflictDiplomacyEvaluation,
    ConflictValidationResponse
    )
from .prompts import (
    conflict_scenario_prompt,
    conflict_validation_prompt,
    conflict_validation_example,
    conflict_diplomacy_evaluation_prompt,
    conflict_feedback_prompt
)

text_llm_1, _ = get_llms(text_llm_config={"temperature": 0.1}, voice_llm_config={})
text_llm_7, _ = get_llms(text_llm_config={"temperature": 0.7}, voice_llm_config={})

# Scenario Generation Chain
conflict_scenario_chain = PromptTemplate.from_template(conflict_scenario_prompt) | text_llm_7


# Response Validation Chain
conflict_validation_chain = create_chain(
    conflict_validation_prompt,
    ConflictValidationResponse,
    conflict_validation_example,
    text_llm_1
)

# Diplomacy Evaluation Chain
conflict_diplomacy_evaluation_example = {
    "empathy_score": 4,
    "clarity_score": 3,
    "solution_focus": 5,
    "professionalism": "excellent",
    "negative_indicators": []
}

conflict_diplomacy_evaluator = create_chain(
    conflict_diplomacy_evaluation_prompt,
    ConflictDiplomacyEvaluation,
    conflict_diplomacy_evaluation_example,
    text_llm_1
)

# Feedback Chain
conflict_feedback_chain = PromptTemplate.from_template(conflict_feedback_prompt) | text_llm_7
