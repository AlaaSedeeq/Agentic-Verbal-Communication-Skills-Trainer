import json
from typing import Literal
from pydantic import BaseModel
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import JsonOutputParser

from src.graph.state import State, PresentationAssessmentData
from src.graph.utils import get_llms
from .types import (
    PresentationAssessmentEvaluation,
    PresentationAssessmentData,
    InputValidation,
    ContentEvaluation,
    DeliveryEvaluation,
    StructureEvaluation
)
from .prompts import (
    VALIDATION_PROMPT,
    STRUCTURE_PROMPT,
    DELIVERY_PROMPT,
    CONTENT_PROMPT
)

text_llm_1, _ = get_llms(temperature = 0.1)
text_llm_7, _ = get_llms(temperature = 0.7)

def create_analyzer(prompt: str, output_model: BaseModel):
    parser = JsonOutputParser(pydantic_object=output_model)
    
    return (
        PromptTemplate.from_template(
            f"{prompt}\nRespond with valid JSON only!\nExample:\n{{example}}",
            partial_variables={
                "example": json.dumps(output_model.example().model_dump(), indent=2)
            }
        )
        | text_llm_1
        | parser
        | RunnableLambda(lambda x: output_model(**x))
        .with_fallbacks([
            RunnableLambda(lambda _: output_model.example())
        ])
    )

# Initialize analyzers
validation_chain = create_analyzer(VALIDATION_PROMPT, InputValidation)
structure_analyzer = create_analyzer(STRUCTURE_PROMPT, StructureEvaluation)
delivery_analyzer = create_analyzer(DELIVERY_PROMPT, DeliveryEvaluation)
content_analyzer = create_analyzer(CONTENT_PROMPT, ContentEvaluation)
