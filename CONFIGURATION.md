# GOODIE AI ASSISTANT - CONFIGURATION REFERENCE

## Default AI Model Configuration

GOODIE is configured with Qwen3 4B GGUF as the default AI model.

### MODEL SETTINGS

- **Default Model**: Qwen3 4B
- **Quantization**: Q4_K_M (4-bit quantization)
- **Engine**: llama.cpp
- **Context Length**: 8192 tokens
- **Threads**: Auto Detect (uses available CPU cores)
- **GPU Acceleration**: Enable when available
- **Fallback**: CPU Mode (automatic fallback if GPU unavailable)

### MODEL MANAGER

- ✓ Download Qwen3 4B automatically during setup
- ✓ Show model size
- ✓ Show RAM requirements
- ✓ Verify model integrity after download
- ✓ Allow model switching (Q5_K_M, Q6_K, FP16 available)
- ✓ Allow model deletion
- ✓ Allow model updates

### STARTUP BEHAVIOR

- ✓ Load Qwen3 4B automatically on launch
- ✓ Display loading progress
- ✓ Show estimated memory usage
- ✓ Ready status when model is loaded

## OPTIMIZATION

- ✓ Fast response mode enabled
- ✓ Cache recent conversations (200MB)
- ✓ Optimize for Office tasks
- ✓ Optimize for Windows automation commands
- ✓ Minimize idle RAM usage
- ✓ Background model loading

## PERSONALITY

- **Tone**: Friendly and professional
- **Style**: Helpful desktop companion
- **Response Mode**: Concise by default, detailed on request
- **Languages**: English (en) and Tamil (ta)

## OFFICE ASSISTANT OPTIMIZATION

- ✓ Word document creation and editing
- ✓ Grammar correction
- ✓ Document summarization
- ✓ Excel formulas and assistance
- ✓ Data analysis
- ✓ PowerPoint slide generation
- ✓ OnlyOffice integration
- ✓ LibreOffice integration

## VOICE ASSISTANT

- **Speech Recognition**: Faster-Whisper
- **Text-to-Speech**: Piper TTS
- **Wake Word**: "Hey Goodie"
- **Custom Wake Words**: Supported
- **Languages**: English, Tamil

## PERFORMANCE TARGETS

- **Startup**: Under 5 seconds
- **Simple Commands**: Under 1 second
- **AI Responses**: Under 3 seconds
- **Smooth Operation**: On 8GB RAM systems

## SYSTEM REQUIREMENTS

- **OS**: Windows 10/11 (x64)
- **RAM**: 8GB minimum (12GB+ recommended)
- **Storage**: 5GB for model + application
- **Processor**: Intel i5 or equivalent
- **GPU**: NVIDIA (CUDA 11.8+) for acceleration (optional)

## CONFIGURATION FILES

Configuration is stored in: `~/.goodie/`

- `config.json` - Main configuration
- `models/` - Downloaded models
- `cache/` - Conversation cache
- `logs/` - Application logs

## ENVIRONMENT VARIABLES

- `GOODIE_CONFIG_DIR` - Custom configuration directory
- `GOODIE_MODELS_DIR` - Custom models directory
- `GOODIE_CACHE_DIR` - Custom cache directory
- `GOODIE_LOG_DIR` - Custom logs directory

## CUSTOMIZATION

All settings can be customized by modifying the configuration files or through the GOODIE settings UI.

### Python API Usage

```python
from goodie import GoodieConfig, ModelManager

# Get configuration
config = GoodieConfig.get_instance()

# Print summary
config.print_summary()

# Access settings
print(config.model.name)  # "Qwen3 4B"
print(config.model.quantization.value)  # "Q4_K_M"

# Model management
manager = ModelManager(config)
manager.print_model_summary()
```

---

**Note**: Qwen3 4B is preselected and recommended throughout the application as the default model.
