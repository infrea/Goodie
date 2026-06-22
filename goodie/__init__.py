"""
GOODIE AI Assistant
A lightweight, professional AI desktop companion powered by Qwen3 4B
"""

__version__ = "1.0.0"
__author__ = "Infrea"
__description__ = "GOODIE AI Assistant - Desktop companion powered by Qwen3 4B"

from .config import GoodieConfig, config
from .model_manager import ModelManager

__all__ = [
    "GoodieConfig",
    "config",
    "ModelManager",
    "__version__",
]
