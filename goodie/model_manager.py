"""
Model Manager for GOODIE
Handles model downloading, verification, and loading
"""

import hashlib
import os
from pathlib import Path
from typing import Optional, Callable
try:
    import httpx
except ImportError:
    httpx = None

from .config import GoodieConfig, ModelConfig, QuantizationType


class ModelManager:
    """Manages AI model lifecycle"""
    
    def __init__(self, config: GoodieConfig = None):
        self.config = config or GoodieConfig.get_instance()
        self.current_model = None
        self.is_loading = False
    
    def calculate_file_hash(self, file_path: Path, algorithm: str = "sha256") -> str:
        """Calculate file hash for integrity verification"""
        hash_obj = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    async def download_model(
        self,
        quantization: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Path:
        """
        Download model with progress tracking
        
        Args:
            quantization: Model quantization type
            progress_callback: Callback function(downloaded_bytes, total_bytes)
        
        Returns:
            Path to downloaded model
        """
        if httpx is None:
            raise RuntimeError("httpx is required for model downloading")
        
        quantization = quantization or self.config.model.quantization.value
        model_path = self.config.get_model_path(quantization)
        
        # Check if already downloaded
        if model_path.exists():
            print(f"✓ Model already exists: {model_path}")
            return model_path
        
        # Create models directory
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get download URL
        url = self.config.model.get_model_url(quantization)
        print(f"\n📥 Downloading {self.config.model.name} ({quantization})...")
        print(f"   URL: {url}")
        print(f"   Size: ~{self.config.model.size_gb}GB")
        print(f"   Location: {model_path}\n")
        
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", url, follow_redirects=True) as response:
                    response.raise_for_status()
                    
                    total_size = int(response.headers.get("content-length", 0))
                    downloaded = 0
                    
                    with open(model_path, "wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                
                                if progress_callback:
                                    progress_callback(downloaded, total_size)
                                else:
                                    # Default progress display
                                    if total_size > 0:
                                        percent = (downloaded / total_size) * 100
                                        print(f"\r   Progress: {percent:.1f}% ({downloaded/1024/1024:.1f}MB / {total_size/1024/1024:.1f}MB)", end="")
                    
                    print("\n✓ Download completed")
                    
                    # Verify integrity
                    print("🔍 Verifying model integrity...")
                    file_hash = self.calculate_file_hash(model_path)
                    print(f"✓ SHA256: {file_hash[:16]}...")
                    
                    return model_path
        
        except Exception as e:
            # Clean up on failure
            if model_path.exists():
                model_path.unlink()
            raise RuntimeError(f"Failed to download model: {e}")
    
    def get_model_info(self, quantization: Optional[str] = None) -> dict:
        """Get information about a model"""
        quantization = quantization or self.config.model.quantization.value
        model_path = self.config.get_model_path(quantization)
        
        info = {
            "name": self.config.model.name,
            "quantization": quantization,
            "context_length": self.config.model.context_length,
            "engine": self.config.model.engine.value,
            "downloaded": model_path.exists(),
        }
        
        if model_path.exists():
            size_bytes = model_path.stat().st_size
            info["file_size_gb"] = round(size_bytes / (1024**3), 2)
            info["file_path"] = str(model_path)
        
        return info
    
    def list_available_models(self) -> list:
        """List all available quantizations"""
        return [
            {
                "quantization": q.value,
                "downloaded": self.config.is_model_downloaded(q.value),
                **self.get_model_info(q.value)
            }
            for q in QuantizationType
        ]
    
    def delete_model(self, quantization: Optional[str] = None) -> bool:
        """Delete a downloaded model"""
        quantization = quantization or self.config.model.quantization.value
        model_path = self.config.get_model_path(quantization)
        
        if model_path.exists():
            try:
                model_path.unlink()
                print(f"✓ Deleted model: {quantization}")
                return True
            except Exception as e:
                print(f"✗ Failed to delete model: {e}")
                return False
        
        print(f"ℹ Model not found: {quantization}")
        return False
    
    def switch_model(self, quantization: str) -> bool:
        """Switch to a different model quantization"""
        if not self.config.is_model_downloaded(quantization):
            print(f"✗ Model not downloaded: {quantization}")
            return False
        
        self.config.model.quantization = QuantizationType(quantization)
        print(f"✓ Switched to model: {quantization}")
        return True
    
    def check_storage_space(self) -> dict:
        """Check available storage space"""
        import shutil
        
        models_path = self.config.models_dir
        stats = shutil.disk_usage(models_path)
        
        return {
            "total_gb": round(stats.total / (1024**3), 2),
            "used_gb": round(stats.used / (1024**3), 2),
            "free_gb": round(stats.free / (1024**3), 2),
        }
    
    def print_model_summary(self):
        """Print model status summary"""
        print("\n" + "="*50)
        print("GOODIE MODEL MANAGER")
        print("="*50)
        
        print(f"\n📦 AVAILABLE MODELS")
        models = self.list_available_models()
        for model in models:
            status = "✓ Downloaded" if model["downloaded"] else "○ Not Downloaded"
            size = f"({model['file_size_gb']}GB)" if model["downloaded"] else f"(~{self.config.model.size_gb}GB)"
            print(f"  {model['quantization']}: {status} {size}")
        
        storage = self.check_storage_space()
        print(f"\n💾 STORAGE")
        print(f"  Total: {storage['total_gb']}GB")
        print(f"  Used: {storage['used_gb']}GB")
        print(f"  Free: {storage['free_gb']}GB")
        
        print(f"\n⭐ DEFAULT")
        print(f"  Model: {self.config.model.name}")
        print(f"  Quantization: {self.config.model.quantization.value}")
        print(f"  Downloaded: {'✓' if self.config.is_model_downloaded() else '✗'}")
        print("\n" + "="*50 + "\n")
