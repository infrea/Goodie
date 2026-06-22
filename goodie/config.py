"""
GOODIE Configuration Manager
Default AI model: Qwen3 4B GGUF with llama.cpp
"""

from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class EngineType(str, Enum):
    """Supported AI engines"""
    LLAMA_CPP = "llama.cpp"
    OLLAMA = "ollama"


class QuantizationType(str, Enum):
    """Model quantization types"""
    Q4_K_M = "Q4_K_M"  # Default
    Q5_K_M = "Q5_K_M"
    Q6_K = "Q6_K"
    FP16 = "FP16"


@dataclass
class ModelConfig:
    """Model configuration"""
    name: str = "Qwen3 4B"
    model_type: str = "qwen"
    size_gb: float = 3.5
    quantization: QuantizationType = QuantizationType.Q4_K_M
    context_length: int = 8192
    threads: Optional[int] = None  # None = auto-detect
    gpu_acceleration: bool = True
    engine: EngineType = EngineType.LLAMA_CPP
    
    # Model URLs
    model_urls: dict = None
    
    def __post_init__(self):
        if self.model_urls is None:
            self.model_urls = {
                "Q4_K_M": "https://huggingface.co/Qwen/Qwen3-4B-Instruct-GGUF/resolve/main/qwen3-4b-instruct-q4_k_m.gguf",
                "Q5_K_M": "https://huggingface.co/Qwen/Qwen3-4B-Instruct-GGUF/resolve/main/qwen3-4b-instruct-q5_k_m.gguf",
                "Q6_K": "https://huggingface.co/Qwen/Qwen3-4B-Instruct-GGUF/resolve/main/qwen3-4b-instruct-q6_k.gguf",
                "FP16": "https://huggingface.co/Qwen/Qwen3-4B-Instruct-GGUF/resolve/main/qwen3-4b-instruct-f16.gguf",
            }
    
    def get_model_url(self, quantization: Optional[str] = None) -> str:
        """Get model download URL"""
        quant = quantization or self.quantization.value
        return self.model_urls.get(quant, self.model_urls["Q4_K_M"])


@dataclass
class PerformanceConfig:
    """Performance optimization settings"""
    fast_response_mode: bool = True
    cache_recent_conversations: bool = True
    cache_size_mb: int = 200
    minimize_idle_ram: bool = True
    background_model_loading: bool = True
    startup_timeout_seconds: int = 5
    response_timeout_seconds: int = 3


@dataclass
class VoiceConfig:
    """Voice assistant configuration"""
    enabled: bool = True
    wake_word: str = "Hey Goodie"
    custom_wake_words: list = None
    speech_recognizer: str = "faster-whisper"
    text_to_speech: str = "piper-tts"
    language: str = "en"
    
    def __post_init__(self):
        if self.custom_wake_words is None:
            self.custom_wake_words = []


@dataclass
class OfficeConfig:
    """Office automation settings"""
    word_support: bool = True
    excel_support: bool = True
    powerpoint_support: bool = True
    libreoffice_support: bool = True
    onlyoffice_support: bool = True
    grammar_correction: bool = True
    document_summarization: bool = True
    data_analysis: bool = True


@dataclass
class PersonalityConfig:
    """GOODIE personality settings"""
    tone: str = "friendly_and_professional"
    response_style: str = "concise"  # concise by default
    supported_languages: list = None
    
    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = ["en", "ta"]  # English and Tamil


class GoodieConfig:
    """Main GOODIE configuration manager"""
    
    _instance: Optional['GoodieConfig'] = None
    
    def __init__(self):
        self.config_dir = Path.home() / ".goodie"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Default configurations
        self.model = ModelConfig()
        self.performance = PerformanceConfig()
        self.voice = VoiceConfig()
        self.office = OfficeConfig()
        self.personality = PersonalityConfig()
        
        # Model storage
        self.models_dir = self.config_dir / "models"
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache directory
        self.cache_dir = self.config_dir / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Logs directory
        self.logs_dir = self.config_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_instance(cls) -> 'GoodieConfig':
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_model_path(self, quantization: Optional[str] = None) -> Path:
        """Get path to model file"""
        quant = quantization or self.model.quantization.value
        model_filename = f"qwen3-4b-instruct-{quant.lower()}.gguf"
        return self.models_dir / model_filename
    
    def is_model_downloaded(self, quantization: Optional[str] = None) -> bool:
        """Check if model is already downloaded"""
        return self.get_model_path(quantization).exists()
    
    def get_all_available_models(self) -> list:
        """List all downloaded models"""
        return [f.stem for f in self.models_dir.glob("*.gguf")]
    
    def to_dict(self) -> dict:
        """Export configuration as dictionary"""
        return {
            "model": self.model.__dict__,
            "performance": self.performance.__dict__,
            "voice": self.voice.__dict__,
            "office": self.office.__dict__,
            "personality": self.personality.__dict__,
        }
    
    def print_summary(self):
        """Print configuration summary"""
        print("\n" + "="*50)
        print("GOODIE AI ASSISTANT CONFIGURATION")
        print("="*50)
        print(f"\n📦 MODEL SETTINGS")
        print(f"  Default Model: {self.model.name}")
        print(f"  Quantization: {self.model.quantization.value}")
        print(f"  Engine: {self.model.engine.value}")
        print(f"  Context Length: {self.model.context_length}")
        print(f"  GPU Acceleration: {'✓' if self.model.gpu_acceleration else '✗'}")
        
        print(f"\n⚡ PERFORMANCE")
        print(f"  Fast Response Mode: {'✓' if self.performance.fast_response_mode else '✗'}")
        print(f"  Cache Size: {self.performance.cache_size_mb}MB")
        print(f"  Startup Timeout: {self.performance.startup_timeout_seconds}s")
        
        print(f"\n🎤 VOICE ASSISTANT")
        print(f"  Status: {'✓ Enabled' if self.voice.enabled else '✗ Disabled'}")
        print(f"  Wake Word: '{self.voice.wake_word}'")
        print(f"  Languages: {', '.join(self.voice.language.upper() for _ in self.voice.language)}")
        
        print(f"\n📋 OFFICE INTEGRATION")
        print(f"  Word: {'✓' if self.office.word_support else '✗'}")
        print(f"  Excel: {'✓' if self.office.excel_support else '✗'}")
        print(f"  PowerPoint: {'✓' if self.office.powerpoint_support else '✗'}")
        
        print(f"\n💬 PERSONALITY")
        print(f"  Tone: {self.personality.tone}")
        print(f"  Default Style: {self.personality.response_style}")
        print(f"  Languages: {', '.join(self.personality.supported_languages).upper()}")
        print("\n" + "="*50 + "\n")


# Singleton instance
config = GoodieConfig.get_instance()
