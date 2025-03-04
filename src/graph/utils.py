import json
from pydantic import BaseModel

from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda


def create_chain(
    prompt_template: str,
    pydantic_model: BaseModel,
    example: dict,
    model: ChatGroq,
    temperature: float
) -> RunnableLambda:
    """Create validated chain with error recovery"""
    parser = JsonOutputParser(pydantic_object=pydantic_model)

    full_prompt = PromptTemplate(
            template=prompt_template + "\n\n{format_instructions}\nExample:\n{example}",
            input_variables=prompt_template.count("{") // 2,
            partial_variables={
                "format_instructions": parser.get_format_instructions(),
                "example": json.dumps(example, indent=2)
            }
        )\
        | model\
        | parser\
        | RunnableLambda(lambda x: pydantic_model.model_validate(x))

    return full_prompt.with_fallbacks([
        RunnableLambda(lambda _: pydantic_model(
            **example,
            followup_message="Could not process response"
        ))
    ])
