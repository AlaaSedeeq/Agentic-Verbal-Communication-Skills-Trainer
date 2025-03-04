import json
from typing import Tuple, Union
from pydantic import ValidationError
from langchain_groq import ChatGroq
from src.types.impromptu_types import ImpromptuValidationResponse


model_name = ""

def validate_response(response: str, scheme: str, max_tries: int = 3) -> Tuple[Union[dict, str], bool]:

    try:
        parsed_response = json.loads(response)
        if parsed_response.get("properties") and len(parsed_response.keys()) > 1:
            parsed_response = parsed_response["properties"]
        ImpromptuValidationResponse(**parsed_response)
        return parsed_response, True
    except (json.JSONDecodeError, ValidationError):
        if max_tries == 0:
            return response, False

    model = ChatGroq(model=model_name, temperature=0.3)
    prompt = (
        f"Update this response: {response}\n"
        f"to follow this JSON schema: {json.dumps(ImpromptuValidationResponse.model_json_schema(), ensure_ascii=False)}\n"
        "Reply ONLY with the new JSON values with no additional properties keys.\n"
        "JSON:\n"
    )

    for attempt in range(max_tries):
        try:
            json_response_str = model.invoke(prompt).content
            parsed_json = json.loads(json_response_str)
            ImpromptuValidationResponse(**parsed_json)
            return parsed_json, True
        except json.JSONDecodeError:
            continue
        except ValidationError:
            continue
        print(f"Try {attempt + 1}/{max_tries} failed")

    return response, False
