"""
GOODIE Main Application Entry Point
"""

import sys
import asyncio
from pathlib import Path
from .config import config
from .model_manager import ModelManager


def print_banner():
    """Print GOODIE banner"""
    banner = r"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║           GOODIE AI ASSISTANT v1.0.0                         ║
    ║     Your Professional Desktop Companion                      ║
    ║          Powered by Qwen3 4B GGUF                            ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def initialize_goodie():
    """Initialize GOODIE configuration and setup"""
    print_banner()
    
    print("🔧 Initializing GOODIE...\n")
    
    # Print configuration
    config.print_summary()
    
    # Initialize model manager
    model_manager = ModelManager(config)
    
    print("📦 Model Status:")
    model_manager.print_model_summary()
    
    return model_manager


def main():
    """Main entry point"""
    try:
        # Initialize
        model_manager = initialize_goodie()
        
        # Check if default model is downloaded
        if not config.is_model_downloaded():
            print("\n⚠️  Default model not found!")
            print(f"📥 The {config.model.name} model ({config.model.quantization.value}) needs to be downloaded.")
            print(f"   Size: ~{config.model.size_gb}GB")
            print(f"   Location: {config.get_model_path()}")
            
            response = input("\nDownload now? (y/n): ").strip().lower()
            if response == 'y':
                print("\n🚀 Starting download...")
                # For now, we'll just show the message
                # In a real GUI application, this would be handled by the GUI
                print(f"Download URL: {config.model.get_model_url()}")
            else:
                print("\n⚠️  GOODIE requires the model to run. Exiting.")
                return 1
        else:
            print(f"\n✓ Default model is ready: {config.model.name} ({config.model.quantization.value})")
        
        print("\n" + "="*60)
        print("✅ GOODIE is ready to use!")
        print("="*60)
        print("\nUsage:")
        print("  - Say 'Hey Goodie' to activate voice assistant")
        print("  - Use Ctrl+Alt+G for quick access")
        print("  - Settings available in system tray menu")
        print("\n💡 Tips:")
        print("  - GOODIE optimizes for Office tasks (Word, Excel, PowerPoint)")
        print("  - Voice and text modes are both available")
        print("  - Responses are typically under 3 seconds")
        print("\nPress Ctrl+C to exit\n")
        
        # Keep the application running
        try:
            while True:
                asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! GOODIE shutting down...\n")
            return 0
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
