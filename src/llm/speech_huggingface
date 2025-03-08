from contextlib import nullcontext
import numpy as np
import torch
import logging
from typing import Union, List, Optional
from pathlib import Path
import io
import soundfile as sf
import librosa
from urllib.request import urlopen
from transformers import WhisperForConditionalGeneration, WhisperProcessor, AutomaticSpeechRecognitionPipeline

logger = logging.getLogger(__name__)

class WhisperTranscriber:
    def __init__(
        self,
        model_name: str = "openai/whisper-small",
        device: Optional[str] = None,
        compile_model: bool = True,
        flash_attention: bool = True
    ):
        """
        Initialize Whisper speech-to-text transcriber
        
        Args:
            model_name: Hugging Face model identifier
            device: Force device (auto-detected if None)
            compile_model: Use torch.compile for faster inference
            flash_attention: Enable Flash Attention optimization
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        self.dtype = torch.float16 if "cuda" in self.device else torch.float32
        
        # Initialize model with optimizations
        self.model = WhisperForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=self.dtype,
        ).to(self.device)
        
        if compile_model and hasattr(torch, "compile"):
            self.model = torch.compile(self.model)
            
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.pipeline = AutomaticSpeechRecognitionPipeline(
            model=self.model,
            feature_extractor=self.processor.feature_extractor,
            tokenizer=self.processor.tokenizer,
            device=self.device,
            torch_dtype=self.dtype
        )

    def _load_audio(self, input_data: Union[str, Path, bytes, np.ndarray], target_sample_rate: int = 16000) -> np.ndarray:
        """Load and normalize audio from various input types with proper headers"""
        try:
            if isinstance(input_data, (str, Path)):
                input_str = str(input_data)
                if input_str.startswith(("http://", "https://")):
                    # Use requests with headers to mimic browser
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                        "Accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9",
                        "Referer": "https://www.example.com/"
                    }
                    response = requests.get(input_str, headers=headers, stream=True)
                    response.raise_for_status()
                    audio, sr = sf.read(io.BytesIO(response.content))
                else:
                    audio, sr = sf.read(input_str)
            elif isinstance(input_data, bytes):
                audio, sr = sf.read(io.BytesIO(input_data))
            elif isinstance(input_data, np.ndarray):
                return librosa.resample(input_data, orig_sr=sr, target_sr=target_sample_rate)
            else:
                raise ValueError("Unsupported input type")
                
            # Resample if needed
            if sr != target_sample_rate:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sample_rate)
            
            if len(audio.shape) > 1:
                audio = librosa.to_mono(audio.T)  # Handle multichannel audio
                
            # Ensure proper sample rate
            if sr != target_sample_rate:
                audio = librosa.resample(
                    audio, 
                    orig_sr=sr, 
                    target_sr=target_sample_rate
                )
                
            return audio.astype(np.float32)
        except Exception as e:
            logger.error(f"Error loading audio: {str(e)}")
            raise

    def transcribe(
        self,
        inputs: Union[str, Path, bytes, List[Union[str, Path, bytes]]],
        language: Optional[str] = "en",
        task: str = "transcribe",
        batch_size: int = 4,
        return_timestamps: bool = False,
        normalize: bool = True,
        **generation_kwargs
    ) -> Union[str, List[str]]:
        """
        Transcribe audio to text with Whisper
        
        Args:
            inputs: Audio file paths, URLs, bytes, or numpy arrays
            language: ISO language code (None for auto-detection)
            task: 'transcribe' or 'translate'
            batch_size: Number of parallel transcriptions
            return_timestamps: Return word-level timestamps
            normalize: Apply basic text normalization
            generation_kwargs: Additional model.generate parameters
            
        Returns:
            Transcribed text or list of texts
        """
        # Single input handling
        is_batch = isinstance(inputs, list)
        audio_inputs = [self._load_audio(inp) for inp in (inputs if is_batch else [inputs])]
        
        # Configure pipeline
        generate_kwargs = {
            "task": task,
            "language": language,
            "return_timestamps": return_timestamps,
            "batch_size": batch_size,
            **generation_kwargs
        }
        
        if not return_timestamps:
            generate_kwargs["max_new_tokens"] = generation_kwargs.get("max_new_tokens", 480_000)

        try:
            with torch.cuda.amp.autocast() if "cuda" in self.device else nullcontext():
                outputs = self.pipeline(
                    audio_inputs,
                    generate_kwargs=generate_kwargs,
                    # normalize=normalize
                )
                
            # Process outputs
            if return_timestamps:
                return outputs if is_batch else outputs[0]
                
            texts = [out["text"] for out in outputs]
            return texts if is_batch else texts[0]
            
        except torch.cuda.OutOfMemoryError:
            logger.error("CUDA out of memory - try reducing batch_size")
            raise
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise
