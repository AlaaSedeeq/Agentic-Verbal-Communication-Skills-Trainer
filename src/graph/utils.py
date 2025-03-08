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

    if model._llm_type == "huggingface":
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


def get_llms(**kargs) -> Tuple[LLM, LLM]:
    """Get text and voice LLMs based on configuration, with option to override parameters.
    
    Args:
        text_llm_config: Optional dict of parameters to override the text LLM config
        voice_llm_config: Optional dict of parameters to override the voice LLM config
        
    Returns:
        Tuple of (text_model, voice_model)
    """
    if CONFIG.llms.llm_use == "groq":
        # Text LLM
        base_text_config = CONFIG.llms.groq.text_llm.config
        # Safely convert to dict only if config exists
        base_text_params = {}
        if base_text_config is not None:
            try:
                base_text_params = base_text_config.to_dict()
            except AttributeError:
                # If to_dict() isn't available but config exists
                base_text_params = base_text_config
        
        # Override with user-provided parameters
        if kargs is not None:
            base_text_params.update(kargs)

        # Pass the model name separately and config params as kwargs
        text_model = ChatGroq(
            model=CONFIG.llms.groq.text_llm.model,
            **base_text_params
        )
        
        # Voice LLM
        base_voice_config = CONFIG.llms.groq.voice_llm.config
        base_voice_params = {}
        if base_voice_config is not None:
            try:
                base_voice_params = base_voice_config.to_dict()
            except AttributeError:
                base_voice_params = base_voice_config
        
        # Override with user-provided parameters
        if kargs is not None:
            base_voice_params.update(kargs)
                
        voice_model = ChatGroq(
            model=CONFIG.llms.groq.voice_llm.model,
            **base_voice_params
        )
    
    elif CONFIG.llms.llm_use == "huggingface":
        # Text LLM
        base_text_config = CONFIG.llms.huggingface.text_llm.config
        base_text_params = {}
        if base_text_config is not None:
            try:
                base_text_params = base_text_config.to_dict()
            except AttributeError:
                base_text_params = base_text_config
        
        # Override with user-provided parameters
        if kargs is not None:
            base_text_params.update(kargs)
                
        text_model = HuggingFaceLLM(
            model_name=CONFIG.llms.huggingface.text_llm.model_name,
            **base_text_params
        )
        
        # Voice LLM
        base_voice_config = CONFIG.llms.huggingface.voice_llm.config
        base_voice_params = {}
        if base_voice_config is not None:
            try:
                base_voice_params = base_voice_config.to_dict()
            except AttributeError:
                base_voice_params = base_voice_config
        
        # Override with user-provided parameters
        if kargs is not None:
            base_voice_params.update(kargs)
                
        voice_model = HuggingFaceLLM(
            model_name=CONFIG.llms.huggingface.voice_llm.model_name,
            **base_voice_params
        )

    else:
        raise ValueError(f"Invalid LLM use: {CONFIG.llms.llm_use}")

    return text_model, voice_model
