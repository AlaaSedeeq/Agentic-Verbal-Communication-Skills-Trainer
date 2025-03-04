import torch
from abc import ABC, abstractmethod
from typing import Optional, List, Union
from dataclasses import dataclass

@dataclass
class GenerationConfig:
    max_length: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    do_sample: bool = True
    num_return_sequences: int = 1

class LLMBase(ABC):
    def __init__(
        self,
        model_name: str,
        system_prompt: str,
        device: Optional[str] = None,
        config: GenerationConfig = None,
        **kwargs
    ):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.model = None
        self.tokenizer = None
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.generation_config = config or GenerationConfig()
        self._initialize_model(**kwargs)

    @abstractmethod
    def _initialize_model(self, **kwargs) -> None:
        """Initialize the model and tokenizer."""
        pass

    @abstractmethod
    def tokenize(self, text: Union[str, List[str]]) -> torch.Tensor:
        """Convert input text to tokens."""
        pass
    
    @abstractmethod
    def detokenize(self, tokens: torch.Tensor) -> str:
        """Convert tokens back to text."""
        pass

    @abstractmethod
    def generate(
        self,
        prompt: Union[str, List[str]],
        generation_config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> Union[str, List[str]]:
        """Generate text based on the prompt."""
        pass

    def update_generation_config(self, **kwargs) -> None:
        """Update generation parameters."""
        for key, value in kwargs.items():
            if hasattr(self.generation_config, key):
                setattr(self.generation_config, key, value)

    @abstractmethod
    def get_num_tokens(self, text: str) -> int:
        """Get the number of tokens in the text."""
        pass

    def prepare_prompt(self, user_prompt: str) -> str:
        """Prepare the full prompt with system message."""
        return f"{self.system_prompt}\n\n{user_prompt}" if self.system_prompt else user_prompt

    @abstractmethod
    def get_model_context_length(self) -> int:
        """Get the maximum context length for the model."""
        pass

    def to(self, device: str) -> 'LLMBase':
        """Move model to specified device."""
        if hasattr(self.model, 'to'):
            self.model = self.model.to(device)
        self.device = device
        return self

