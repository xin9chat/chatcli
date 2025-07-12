#!/bin/bash
# ChatCLI Installation Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$SCRIPT_DIR/bin"
CHATCLI_SCRIPT="$BIN_DIR/chatcli"

echo -e "${GREEN}ChatCLI Installation${NC}"
echo "====================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "${RED}Error: pip is required but not installed.${NC}"
    exit 1
fi

# Install required Python packages
echo -e "${YELLOW}Installing required Python packages...${NC}"
if command -v pip3 &> /dev/null; then
    pip3 install --user -r "$SCRIPT_DIR/requirements.txt" --break-system-packages 2>/dev/null || pip3 install --user -r "$SCRIPT_DIR/requirements.txt"
else
    pip install --user -r "$SCRIPT_DIR/requirements.txt" --break-system-packages 2>/dev/null || pip install --user -r "$SCRIPT_DIR/requirements.txt"
fi

# Check if the chatcli script exists
if [ ! -f "$CHATCLI_SCRIPT" ]; then
    echo -e "${RED}Error: chatcli script not found at $CHATCLI_SCRIPT${NC}"
    exit 1
fi

# Make sure the script is executable
chmod +x "$CHATCLI_SCRIPT"

# Determine the appropriate directory to install the symlink
if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
elif [ -d "$HOME/.local/bin" ]; then
    INSTALL_DIR="$HOME/.local/bin"
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo -e "${YELLOW}Adding $HOME/.local/bin to PATH...${NC}"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
    fi
else
    mkdir -p "$HOME/.local/bin"
    INSTALL_DIR="$HOME/.local/bin"
    echo -e "${YELLOW}Created $HOME/.local/bin directory${NC}"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
fi

# Create symlink
SYMLINK_PATH="$INSTALL_DIR/chatcli"

if [ -L "$SYMLINK_PATH" ]; then
    echo -e "${YELLOW}Removing existing symlink...${NC}"
    rm "$SYMLINK_PATH"
fi

echo -e "${YELLOW}Creating symlink to $SYMLINK_PATH...${NC}"
ln -s "$CHATCLI_SCRIPT" "$SYMLINK_PATH"

echo -e "${GREEN}Installation completed successfully!${NC}"
echo
echo "Usage:"
echo "  chatcli                          # Start interactive chat (default provider)"
echo "  chatcli --setup                  # Configure API keys"
echo "  chatcli --provider openai        # Use OpenAI/ChatGPT"
echo "  chatcli --claude                 # Use Claude (shortcut)"
echo "  chatcli --gemini                 # Use Gemini (shortcut)"
echo "  chatcli --deepseek               # Use DeepSeek (shortcut)"
echo "  chatcli --grok                   # Use Grok (shortcut)"
echo "  chatcli --list-providers         # Show available providers"
echo "  chatcli --help                   # Show all options"
echo
echo "Supported LLM Providers:"
echo "  • OpenAI (ChatGPT, GPT-4, etc.)"
echo "  • Anthropic Claude"
echo "  • Google Gemini"
echo "  • DeepSeek"
echo "  • xAI Grok"
echo
echo -e "${YELLOW}Before using, run: chatcli --setup${NC}"
echo "Or set environment variables for your preferred providers:"
echo "  export OPENAI_API_KEY='your-openai-key'"
echo "  export ANTHROPIC_API_KEY='your-claude-key'"
echo "  export GOOGLE_API_KEY='your-gemini-key'"
echo "  export DEEPSEEK_API_KEY='your-deepseek-key'"
echo "  export XAI_API_KEY='your-grok-key'"
echo
echo -e "${YELLOW}Note: You may need to restart your terminal or run 'source ~/.bashrc' for the PATH changes to take effect.${NC}"