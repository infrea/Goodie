# GOODIE AI ASSISTANT

A lightweight, professional AI desktop companion powered by Qwen3 4B GGUF with llama.cpp, optimized for Windows productivity tasks.

## Features

- **Fast & Efficient**: Qwen3 4B model with Q4_K_M quantization
- **Multi-Language**: English and Tamil support
- **Office Integration**: Word, Excel, PowerPoint, LibreOffice, OnlyOffice
- **Voice Assistant**: Speech recognition and text-to-speech
- **Windows Automation**: Desktop task automation
- **GPU Acceleration**: Fallback to CPU mode when unavailable

## Default Configuration

- **Model**: Qwen3 4B (Q4_K_M)
- **Engine**: llama.cpp
- **Context Length**: 8192
- **Platform**: Windows (x64, x86)
- **Performance Target**: <5s startup, <3s AI responses

## Quick Start

1. Download the installer (EXE or MSI)
2. Run and follow the setup wizard
3. Qwen3 4B will auto-download during installation
4. Launch and use the "Hey Goodie" wake word

## System Requirements

- **OS**: Windows 10/11
- **RAM**: 8GB minimum (12GB+ recommended)
- **Storage**: 5GB for model + application
- **Processor**: Intel i5 or equivalent
- **GPU**: NVIDIA (CUDA 11.8+) for acceleration

## Build

```bash
# Build EXE
python build.py --format exe

# Build MSI
python build.py --format msi
```

## License

[Add your license here]
