from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from src.graph.utils import create_chain
from src.types.impromptu_types import (
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


# os.environ['GROQ_API_KEY'] = userdata.get('GROQ_API')
model_name = "llama-3.1-8b-instant"
#"llama-3.2-3b-preview" "llama-3.1-8b-instant" "llama-3.3-70b-versatile" "llama3-8b-8192"


# ======== Validation Chain ========
impromptu_validation_chain = create_chain(
    impromptu_validation_prompt,
    ImpromptuValidationResponse,
    impromptu_validation_example,
    ChatGroq(model=model_name),
    0.3
)

# ======== Structure Analysis Chain ========
impromptu_structure_analyzer = create_chain(
    impromptu_structure_prompt,
    ImpromptuStructureEvaluationResponse,
    impromptu_structure_example,
    ChatGroq(model=model_name),
    0.2
)

# ======== Fluency Evaluation Chain ========
impromptu_fluency_evaluator = create_chain(
    impromptu_fluency_prompt,
    ImpromptuFluencyEvaluationResponse,
    impromptu_fluency_example,
    ChatGroq(model=model_name),
    0.1
)

# ======== Feedback Chain ========
impromptu_feedback_chain = (
    PromptTemplate.from_template(
        impromptu_feedback_prompt
    )
    | ChatGroq(model=model_name, temperature=0.5)
)

# ======== Topic Generation Chain ========
impromptu_topic_chain = (
    PromptTemplate.from_template(
        impromptu_topic_prompt
    )
    | ChatGroq(model=model_name, temperature=0.7)
)

# ======== Followup Chain ========
impromptu_followup_chain = (
    PromptTemplate.from_template(
        impromptu_followup_prompt
    )
    | ChatGroq(model=model_name, temperature=0.3)
)
