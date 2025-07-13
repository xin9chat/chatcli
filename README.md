# ChatCLI

A powerful terminal-based chat interface that supports multiple LLM providers. Chat with OpenAI GPT models, Anthropic Claude, Google Gemini, DeepSeek, and xAI Grok all from your command line.

## Features

- **Multi-Provider Support**: OpenAI, Anthropic Claude, Google Gemini, DeepSeek, xAI Grok
- **Interactive Terminal Chat**: Full conversation history during session
- **Provider Switching**: Change providers mid-conversation with `/switch` command
- **Model Selection**: Choose specific models for each provider
- **Secure API Key Management**: Store keys safely with proper permissions
- **Provider Shortcuts**: Quick access with `--claude`, `--gemini`, etc.
- **Easy Installation**: One-command setup script

## Supported Providers

| Provider | Models | Shortcut | Environment Variable |
|----------|--------|----------|---------------------|
| **OpenAI** | GPT-4o, GPT-4o-mini, GPT-4-turbo, o1-preview, o1-mini | `--openai`, `--gpt4` | `OPENAI_API_KEY` |
| **Anthropic Claude** | Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus | `--claude` | `ANTHROPIC_API_KEY` |
| **Google Gemini** | Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash | `--gemini` | `GOOGLE_API_KEY` |
| **DeepSeek** | deepseek-chat, deepseek-reasoner | `--deepseek`, `--reasoner` | `DEEPSEEK_API_KEY` |
| **xAI Grok** | grok-4, grok-3, grok-3-mini | `--grok` | `XAI_API_KEY` |

## Installation

1. Clone or download this project:
   ```bash
   git clone https://github.com/yourusername/chatcli.git
   cd chatcli
   ```

2. Run the installation script:
   ```bash
   ./install.sh
   ```

This will:
- Install the required Python packages (`openai`, `anthropic`, `google-generativeai`)
- Create a global `chatcli` command
- Set up the necessary PATH configuration

## Setup

Configure your API keys for the providers you want to use:

```bash
chatcli --setup
```

Or set them as environment variables:
```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-claude-key" 
export GOOGLE_API_KEY="your-gemini-key"
export DEEPSEEK_API_KEY="your-deepseek-key"
export XAI_API_KEY="your-grok-key"
```

### Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google AI**: https://makersuite.google.com/app/apikey
- **DeepSeek**: https://platform.deepseek.com/api_keys
- **xAI**: https://console.x.ai/

## Usage

### Basic Usage

```bash
# Start with default provider (OpenAI)
chatcli

# Use specific provider
chatcli --provider claude
chatcli --provider gemini
chatcli --provider deepseek

# Use shortcuts
chatcli --claude
chatcli --gemini
chatcli --deepseek
chatcli --grok
```

### Advanced Usage

```bash
# Use specific model
chatcli --provider openai --model gpt-4o
chatcli --claude --model claude-3-opus-20240229

# Quick shortcuts for popular models
chatcli --gpt4              # GPT-4o
chatcli --gpt4-mini         # GPT-4o-mini
chatcli --reasoner          # DeepSeek Reasoner
```

### Configuration Commands

```bash
# Interactive setup for API keys
chatcli --setup

# Interactive configuration for defaults
chatcli --configure-defaults

# Set default provider
chatcli --set-default-provider claude
chatcli --set-default-provider openai

# Set default model for a provider
chatcli --set-default-model openai gpt-4.1
chatcli --set-default-model claude claude-sonnet-4
chatcli --set-default-model gemini gemini-2.5-pro

# Show current configuration
chatcli --config
```

### Information Commands

```bash
# List available providers
chatcli --list-providers

# List models for a provider
chatcli --list-models openai
chatcli --list-models claude
```

### Interactive Commands

Once in a chat session, you can use these commands:

- `/quit`, `/exit`, `/q` - Exit the chat
- `/clear` - Clear conversation history
- `/switch <provider>` - Switch to different provider (e.g., `/switch claude`)
- `/model <model>` - Switch to different model
- `/info` - Show current provider and model info
- `/help` - Show available commands

### Example Session

```bash
$ chatcli --claude
ChatCLI - CLAUDE
Model: claude-sonnet-4
==============================
Commands:
  /quit, /exit, /q     - Exit chat
  /clear              - Clear conversation
  /switch <provider>  - Switch provider
  /model <model>      - Switch model
  /info               - Provider info
  /help               - Show commands

You: Hello! Can you help me with Python?
Claude: Hello! I'd be happy to help you with Python...

You: /switch openai
Switched to openai

You: What's the latest in AI?
Openai: The field of AI is rapidly evolving...

You: /quit
Goodbye!
```

## Project Structure

```
chatcli/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── install.sh                   # Installation script
├── bin/
│   └── chatcli                 # Main executable
├── src/
│   ├── chatcli.py              # Main application
│   ├── chat/
│   │   ├── base.py             # Base LLM provider class
│   │   ├── factory.py          # Provider factory
│   │   └── providers/          # Individual provider implementations
│   │       ├── openai.py
│   │       ├── claude.py
│   │       ├── gemini.py
│   │       ├── deepseek.py
│   │       └── grok.py
│   └── config/
│       └── manager.py          # Configuration management
└── config/                     # Configuration storage (~/.chatcli/)
```

## Configuration

API keys and settings are stored in `~/.chatcli/config.json` with secure permissions (600). 

### Configuration Options

- **Multiple provider API keys**: Store API keys for all providers
- **Default provider preference**: Set which provider to use when none is specified
- **Per-provider default models**: Configure default models for each provider
- **Application settings**: Conversation history limits, auto-save, etc.

### Quick Configuration

```bash
# Set up everything interactively
chatcli --setup                           # Configure API keys
chatcli --configure-defaults              # Set default provider and models

# Or configure individually
chatcli --set-default-provider claude     # Make Claude the default
chatcli --set-default-model openai gpt-4.1 # Set GPT-4o as OpenAI default
```

### Configuration File Structure

The config file (`~/.chatcli/config.json`) structure:
```json
{
  "default_provider": "claude",
  "providers": {
    "openai": {
      "api_key": "your-key",
      "default_model": "gpt-4.1"
    },
    "claude": {
      "api_key": "your-key", 
      "default_model": "claude-sonnet-4"
    }
  },
  "settings": {
    "conversation_history_limit": 100,
    "auto_save_conversations": false
  }
}
```

## Requirements

- Python 3.6+
- Internet connection for API calls
- API keys for desired providers

## Security

- API keys are stored securely with restricted file permissions
- No sensitive data is logged or transmitted unnecessarily
- Configuration files are created with user-only access

## Troubleshooting

### Common Issues

1. **"API key not found"**
   - Run `chatcli --setup` to configure keys
   - Or set environment variables

2. **"Command not found: chatcli"**
   - Restart your terminal
   - Or run `source ~/.bashrc` / `source ~/.zshrc`

3. **"Permission denied"**
   - Make sure install script has execute permissions: `chmod +x install.sh`

4. **Package installation errors**
   - Try: `pip3 install --user openai anthropic google-generativeai`

### Getting Help

```bash
chatcli --help        # Show all command options
chatcli --config      # Check current configuration
chatcli --list-providers  # See available providers
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).