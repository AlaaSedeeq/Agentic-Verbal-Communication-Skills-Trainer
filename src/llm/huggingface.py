
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from langchain.llms.base import LLM
from pydantic import Field, PrivateAttr
import torch
from typing import Optional, List, Dict, Any

class HuggingFaceLLM(LLM):
    """
    LangChain-compatible LLM wrapper for Hugging Face Causal Language Models.
    """
    
    model_name: str = Field(default="meta-llama/Llama-3.2-3B", description="Hugging Face model identifier")
    quantization_config: Optional[BitsAndBytesConfig] = Field(
        default=None, 
        description="Configuration for model quantization"
    )
    max_new_tokens: int = Field(
        default=50, 
        description="Maximum number of new tokens to generate"
    )
    temperature: float = Field(
        default=0.7, 
        description="Temperature parameter for generation"
    )

    _tokenizer: AutoTokenizer = PrivateAttr()
    _model: AutoModelForCausalLM = PrivateAttr()
    _device: torch.device = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            padding_side="left",  # Optimize for left-padded generation
            truncation_side="left"
        )
        
        # Set pad token if missing
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        model_args = {
            "pretrained_model_name_or_path": self.model_name,
            "quantization_config": self.quantization_config,
            "device_map": "auto",
            "trust_remote_code": True,
            # "attn_implementation": "flash_attention_2",  # Use flash attention if available
            "torch_dtype": torch.bfloat16,  # Optimized for modern GPUs
        }

        self._model = AutoModelForCausalLM.from_pretrained(**model_args)
        
        # Determine the device of the model
        self._device = next(self._model.parameters()).device
        
        # Compile model for faster inference (requires PyTorch 2.0+)
        if hasattr(torch, "compile"):
            self._model = torch.compile(self._model)

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        inputs = self._tokenizer(prompt, return_tensors="pt")
        # Move inputs to the same device as the model
        inputs = {k: v.to(self._device) for k, v in inputs.items()}

        generate_args = {
            **inputs,
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "do_sample": True,
        }
        
        with torch.no_grad():
            outputs = self._model.generate(**generate_args)

        response = self._tokenizer.decode(
            outputs[0], 
            skip_special_tokens=True
        )
        
        # Post-processing for stop sequences
        if stop:
            for sequence in stop:
                if sequence in response:
                    response = response.split(sequence)[0]
        return response

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "quantization": bool(self.quantization_config),
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature
        }

    @property
    def _llm_type(self) -> str:
        return "huggingface_causal_lm"
