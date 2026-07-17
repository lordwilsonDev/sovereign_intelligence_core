# Level 33 Sovereign Architecture

## Executive Summary

This project implements a self-healing "Ouroboros Loop" AI agent system that merges NanoApex reasoning with Physical Agency (Level 33) using the Gemma 2 9B model running locally on Apple Silicon.

## System Architecture

### Core Components

1. **Gemma 2 9B Model** - The computational substrate running via Ollama
2. **Physical Hand** (`tools/physical_hand.py`) - Safe click execution with user confirmation
3. **Brain Core** (`architecture/brain_core.py`) - AutoGen agents with Gemma 2 integration
4. **DSPy Optimizer** (`optimization/optimize_prompt.py`) - Self-correction and prompt optimization

### Hardware Requirements

- **Architecture**: Apple Silicon (M1/M2/M3)
- **RAM**: 16GB minimum (tested on 16GB)
- **Disk Space**: ~6GB for Gemma 2 9B model
- **OS**: macOS

### Software Dependencies

- Ollama (for running Gemma 2 9B)
- cliclick (for physical mouse control)
- Python 3.9+
- pyautogen
- dspy-ai

## Installation

### Quick Start

```bash
cd ~/level33_sovereign
chmod +x level33_init.sh
./level33_init.sh
```

### Manual Installation

1. **Install Ollama**
   ```bash
   # Download from ollama.com or use Homebrew
   brew install ollama
   ```

2. **Install cliclick**
   ```bash
   brew install cliclick
   ```

3. **Pull Gemma 2 9B Model**
   ```bash
   ollama pull gemma2:9b
   ```

4. **Install Python Dependencies**
   ```bash
   pip3 install pyautogen dspy-ai
   ```

## Usage

### Testing Individual Components

1. **Test Physical Hand**
   ```bash
   python3 tools/physical_hand.py
   ```

2. **Test DSPy Optimization**
   ```bash
   python3 optimization/optimize_prompt.py
   ```

3. **Test Brain Core**
   ```bash
   python3 architecture/brain_core.py
   ```

### Running the Full Agent

```python
from architecture.brain_core import user_proxy, solver

# Start a conversation
user_proxy.initiate_chat(
    solver,
    message="Your task here"
)
```

## Safety Features

### Built-in Safety Mechanisms

1. **User Confirmation** - All clicks require user approval by default
2. **Coordinate Validation** - Negative coordinates are rejected
3. **Human-in-the-Loop** - AutoGen configured with `ALWAYS` human input mode
4. **Workspace Isolation** - Code execution confined to `workspace/` directory

### Safety Configuration

To disable click confirmation (use with caution):
```python
safe_click(x, y, confirm=False)
```

## Architecture Details

### The Physical Reflexion Loop

```
┌─────────────────────────────────────────┐
│  1. Plan (Gemma 2 9B via AutoGen)      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  2. Act (Physical Hand - cliclick)      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  3. Reflect (Error Detection)           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. Optimize (DSPy Self-Correction)     │
└──────────────┬──────────────────────────┘
               │
               └──────► Loop Back to Plan
```

### Memory Optimization

- **Model Size**: ~5.7GB (Q4_K_M quantization)
- **Available for Context**: ~10GB on 16GB Mac
- **Context Window**: 8K tokens
- **Mitigation**: Hard reset conversation every 10 turns

## Known Limitations

| Component | Risk | Mitigation |
|-----------|------|------------|
| Gemma 2 9B | Context overflow (8k limit) | Reset every 10 turns |
| Cliclick | Blind clicking (resolution mismatch) | Use screencapture to verify UI |
| DSPy | Over-optimization | Ensure metric includes execution success |
| Safety | Rogue loop (infinite clicking) | User confirmation + failsafe |

## Project Structure

```
level33_sovereign/
├── tools/
│   └── physical_hand.py          # Physical agency implementation
├── architecture/
│   └── brain_core.py             # AutoGen + Gemma 2 integration
├── optimization/
│   └── optimize_prompt.py        # DSPy self-correction
├── workspace/                    # Code execution sandbox
├── level33_init.sh              # Master initialization script
└── README.md                     # This file
```

## Testing Results

✅ System Architecture: Apple Silicon (arm64) confirmed
✅ RAM: 16GB available
✅ Ollama: Installed and running
✅ Cliclick: Installed and functional
✅ Gemma 2 9B: Downloaded and tested
✅ DSPy Integration: Self-correction working
✅ Physical Hand: Click execution successful

## Example: Self-Correction in Action

```
Original Plan: Click at coordinates 2000, 2000
Error: Coordinates exceed screen resolution (1920x1080)
Corrected Plan: Click at coordinates 1920, 1080
```

This demonstrates the Ouroboros Loop - the system learning from its own failures.

## Future Enhancements

1. **Vision Integration** - Add screencapture analysis before clicks
2. **Training Data** - Build dataset for DSPy optimization
3. **Multi-Agent** - Add specialized agents for different tasks
4. **Persistent Memory** - Save corrected plans for future use
5. **Performance Metrics** - Track success rates and optimization gains

## Troubleshooting

### Ollama Not Responding
```bash
# Check if Ollama is running
ps aux | grep ollama

# Restart Ollama
killall ollama
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Re-pull if needed
ollama pull gemma2:9b
```

### Python Import Errors
```bash
# Reinstall dependencies
pip3 install --upgrade pyautogen dspy-ai
```

## License

This is an experimental research project. Use at your own risk.

## Credits

Based on the Level 33 Sovereign Architecture blueprint, implementing:
- AutoGen for multi-agent orchestration
- DSPy for prompt optimization
- Ollama for local LLM inference
- Gemma 2 9B as the reasoning engine
