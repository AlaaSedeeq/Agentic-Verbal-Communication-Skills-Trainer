import json
from typing import Tuple
from pydantic import BaseModel

from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.llms.base import LLM
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from src.llm.huggingface import HuggingFaceLLM
from src.common.config import load_config

CONFIG = load_config()

def create_chain(
    prompt_template: str,
    pydantic_model: BaseModel,
    example: dict,
    model: LLM,
) -> RunnableLambda:
    """Create validated chain with error recovery"""
    parser = JsonOutputParser(pydantic_object=pydantic_model)

    if model.llm_type == "huggingface":
        parser = JsonOutputParser(pydantic_object=pydantic_model)
        
        # Escape curly braces in the JSON example
        example_instruct = "Output Example:\n" + json.dumps(example, indent=2).replace("{", "{{").replace("}", "}}")
        output_instruct = "Your output should be a JSON object with the following keys: " + ", ".join(pydantic_model.model_fields.keys())
        final_out = "Output:\n" if pydantic_model is not None else "JSON Output:\n"

        # Create the full prompt template
        full_prompt = PromptTemplate(
            template=prompt_template + "\n\n" + output_instruct + "\n\n" + example_instruct + final_out,
            input_variables=["topic", "transcript"],  # Only expect these variables
        )
        chain = (
            full_prompt
            | model
            | RunnableLambda(lambda x: x.strip().split("Output:")[-1])
            | parser
            | RunnableLambda(lambda x: pydantic_model.model_validate(x))
        )    

    else:
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


def get_llms() -> Tuple[LLM, LLM]:
    if CONFIG.llms.llm_use == "groq": 
        # Text LLM
        text_model_name = CONFIG.llms.opensource.groq.text_llm
        text_llm_config = CONFIG.llms.opensource.groq.text_llm.config
        text_model = ChatGroq(model_name=text_model_name, **text_llm_config)
        # Voice LLM
        voice_llm_config = CONFIG.llms.opensource.groq.voice_llm.config
        voice_model = ChatGroq(**voice_llm_config)
    
    elif CONFIG.llms.llm_use == "huggingface":
        # Text LLM
        text_llm_config = CONFIG.llms.opensource.huggingface.text_llm.config
        text_model = HuggingFaceLLM(**text_llm_config)
        # Voice LLM
        voice_llm_config = CONFIG.llms.opensource.huggingface.voice_llm.config
        voice_model = HuggingFaceLLM(model_name=text_model_name, **voice_llm_config)

    else:
        raise ValueError(f"Invalid LLM use: {CONFIG.llms.llm_use}")

    return text_model, voice_model
