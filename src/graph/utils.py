import json
from pydantic import BaseModel

from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq

from src.common.config import load_config
# from src.llm.huggingface import huggingface_model

CONFIG = load_config()


def create_chain(
    prompt_template: str,
    pydantic_model: BaseModel,
    example: dict,
    model: ChatGroq,
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

def get_llms(text_llm_config: dict = None, voice_llm_config: dict = None):
    
    if CONFIG.llms.llm_use == "opensource":
        if CONFIG.llms.opensource.text_llm == "groq":
            text_model_name = CONFIG.llms.opensource.groq.text_llm
            text_model = ChatGroq(model_name=text_model_name, **text_llm_config)
        else:
            text_model_name = CONFIG.llms.opensource.huggingface.text_llm
            # text_model = huggingface_model(model_name=text_model_name, **text_llm_config)
        if CONFIG.llms.opensource.voice_llm == "groq":
            voice_model_name = CONFIG.llms.opensource.groq.voice_llm
            voice_model = ChatGroq(model_name=voice_model_name, **text_llm_config)

        else:
            voice_model_name = CONFIG.llms.opensource.huggingface.voice_llm
            # voice_model = huggingface_model(model_name=text_model_name, **text_llm_config)

        return text_model, voice_model

    else:
        return None, None