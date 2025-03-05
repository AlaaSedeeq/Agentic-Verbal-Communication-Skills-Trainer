from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from src.graph.utils import create_chain
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

# os.environ['GROQ_API_KEY'] = userdata.get('GROQ_API')
model_name = "llama-3.1-8b-instant"
#"llama-3.2-3b-preview" "llama-3.1-8b-instant" "llama-3.3-70b-versatile" "llama3-8b-8192"


# Scenario Generation Chain
conflict_scenario_chain = PromptTemplate.from_template(conflict_scenario_prompt) |\
                             ChatGroq(model=model_name, temperature=0.7)


# Response Validation Chain
conflict_validation_chain = create_chain(
    conflict_validation_prompt,
    ConflictValidationResponse,
    conflict_validation_example,
    ChatGroq(model=model_name, temperature=0.1),
    0.3
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
    ChatGroq(model=model_name, temperature=0.1),
    0.2
)

# Feedback Chain
conflict_feedback_chain = PromptTemplate.from_template(conflict_feedback_prompt) |\
                            ChatGroq(model=model_name, temperature=0.5)
