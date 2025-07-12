#!/usr/bin/env python3
"""
ChatCLI - Multi-LLM Terminal Chat
A terminal-based chat interface supporting multiple LLM providers
"""

import sys
import argparse
from typing import Optional
from chat.factory import LLMProviderFactory
from config.manager import ConfigManager


class ChatCLI:
    """Main ChatCLI application"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.current_chat = None
        
    def start_chat(self, provider: str = None, model: str = None):
        """Start interactive chat session"""
        if not provider:
            provider = self.config_manager.get_default_provider()
        
        try:
            # Get API key for the provider
            api_key = self.config_manager.get_api_key(provider)
            if not api_key:
                print(f"API key not found for {provider}.")
                print(f"Run 'chatcli --setup' to configure API keys.")
                return
            
            # Get default model if not specified
            if not model:
                model = self.config_manager.get_default_model(provider)
            
            # Create provider instance
            self.current_chat = LLMProviderFactory.create_provider(
                provider_name=provider,
                api_key=api_key,
                model=model
            )
            
            print(f"ChatCLI - {provider.upper()}")
            if model:
                print(f"Model: {model}")
            print("=" * 30)
            print("Commands:")
            print("  /quit, /exit, /q     - Exit chat")
            print("  /clear              - Clear conversation")
            print("  /switch <provider>  - Switch provider")
            print("  /model <model>      - Switch model")
            print("  /info               - Provider info")
            print("  /help               - Show commands")
            print()
            
            self._chat_loop()
            
        except Exception as e:
            print(f"Error starting chat: {e}")
            return
    
    def _chat_loop(self):
        """Main chat interaction loop"""
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    if self._handle_command(user_input):
                        continue
                    else:
                        break
                
                # Get response from LLM
                print(f"{self.current_chat.provider_name.title()}: ", end="", flush=True)
                response = self.current_chat.get_response(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
    
    def _handle_command(self, command: str) -> bool:
        """Handle chat commands. Returns True to continue, False to exit"""
        parts = command[1:].split()
        cmd = parts[0].lower() if parts else ""
        
        if cmd in ['quit', 'exit', 'q']:
            print("Goodbye!")
            return False
        
        elif cmd == 'clear':
            self.current_chat.clear_history()
            print("Conversation history cleared.")
        
        elif cmd == 'switch':
            if len(parts) < 2:
                print("Usage: /switch <provider>")
                print("Available providers:", ", ".join(LLMProviderFactory.get_provider_names()))
            else:
                new_provider = parts[1]
                try:
                    api_key = self.config_manager.get_api_key(new_provider)
                    if not api_key:
                        print(f"API key not found for {new_provider}")
                        return True
                    
                    self.current_chat = LLMProviderFactory.create_provider(
                        provider_name=new_provider,
                        api_key=api_key
                    )
                    print(f"Switched to {new_provider}")
                except Exception as e:
                    print(f"Error switching provider: {e}")
        
        elif cmd == 'model':
            if len(parts) < 2:
                info = self.current_chat.get_provider_info()
                print(f"Current model: {info['model']}")
                print(f"Available models: {', '.join(info['available_models'])}")
            else:
                new_model = parts[1]
                try:
                    self.current_chat.set_model(new_model)
                    print(f"Switched to model: {new_model}")
                except Exception as e:
                    print(f"Error switching model: {e}")
        
        elif cmd == 'info':
            info = self.current_chat.get_provider_info()
            print(f"Provider: {info['name']}")
            print(f"Current model: {info['model']}")
            print(f"Available models: {', '.join(info['available_models'])}")
        
        elif cmd == 'help':
            print("\nAvailable commands:")
            print("  /quit, /exit, /q     - Exit chat")
            print("  /clear              - Clear conversation")
            print("  /switch <provider>  - Switch provider")
            print("  /model <model>      - Switch model")
            print("  /info               - Provider info")
            print("  /help               - Show this help")
        
        else:
            print(f"Unknown command: /{cmd}")
            print("Type /help for available commands")
        
        return True
    
    def list_providers(self):
        """List available providers"""
        print("Available providers:")
        info = LLMProviderFactory.get_provider_info()
        for name, details in info.items():
            api_key = self.config_manager.get_api_key(name)
            status = "✓" if api_key else "✗"
            print(f"  {status} {name} - {details['default_model']}")
        
        print("\nAliases:")
        for alias, provider in LLMProviderFactory.get_provider_aliases().items():
            print(f"  {alias} -> {provider}")
    
    def list_models(self, provider: str):
        """List models for a provider"""
        try:
            info = LLMProviderFactory.get_provider_info(provider)
            print(f"Models for {provider}:")
            print(f"  Default: {info['default_model']}")
            print(f"  Available: {', '.join(info['available_models'])}")
        except ValueError as e:
            print(f"Error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="ChatCLI - Multi-LLM Terminal Chat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  chatcli                                    # Use default provider
  chatcli --provider openai                 # Use OpenAI
  chatcli --claude                          # Use Claude (shortcut)
  chatcli --provider gemini --model gemini-2.0-flash
  chatcli --setup                           # Interactive setup for API keys
  chatcli --configure-defaults              # Configure default provider and models
  chatcli --set-default-provider claude     # Set Claude as default provider
  chatcli --set-default-model openai gpt-4o # Set GPT-4o as default for OpenAI
  chatcli --config                          # Show current configuration
  chatcli --list-providers                  # Show providers
        """
    )
    
    parser.add_argument("--setup", action="store_true", 
                       help="Interactive setup for API keys")
    parser.add_argument("--config", action="store_true",
                       help="Show current configuration")
    parser.add_argument("--configure-defaults", action="store_true",
                       help="Interactive configuration for default provider and models")
    parser.add_argument("--set-default-provider", type=str, metavar="PROVIDER",
                       help="Set the default provider")
    parser.add_argument("--set-default-model", nargs=2, metavar=("PROVIDER", "MODEL"),
                       help="Set default model for a provider")
    parser.add_argument("--provider", type=str,
                       help="LLM provider to use (openai, deepseek, claude, gemini, grok)")
    parser.add_argument("--model", type=str,
                       help="Model to use")
    parser.add_argument("--list-providers", action="store_true",
                       help="List available providers")
    parser.add_argument("--list-models", type=str, metavar="PROVIDER",
                       help="List models for a provider")
    
    # Provider shortcuts
    parser.add_argument("--openai", action="store_true", help="Use OpenAI (shortcut)")
    parser.add_argument("--gpt4", action="store_true", help="Use GPT-4o (shortcut)")
    parser.add_argument("--gpt4-mini", action="store_true", help="Use GPT-4o-mini (shortcut)")
    parser.add_argument("--claude", action="store_true", help="Use Claude (shortcut)")
    parser.add_argument("--gemini", action="store_true", help="Use Gemini (shortcut)")
    parser.add_argument("--deepseek", action="store_true", help="Use DeepSeek (shortcut)")
    parser.add_argument("--reasoner", action="store_true", help="Use DeepSeek Reasoner (shortcut)")
    parser.add_argument("--grok", action="store_true", help="Use Grok (shortcut)")
    
    args = parser.parse_args()
    
    app = ChatCLI()
    
    # Handle setup
    if args.setup:
        app.config_manager.setup_interactive()
        return
    
    # Handle config display
    if args.config:
        app.config_manager.show_config()
        return
    
    # Handle interactive defaults configuration
    if args.configure_defaults:
        app.config_manager.configure_defaults_interactive()
        return
    
    # Handle setting default provider
    if args.set_default_provider:
        if app.config_manager.validate_provider(args.set_default_provider):
            app.config_manager.set_default_provider(args.set_default_provider)
            print(f"Default provider set to: {args.set_default_provider}")
        else:
            print(f"Invalid provider: {args.set_default_provider}")
            print("Available providers:", ", ".join(["openai", "deepseek", "claude", "gemini", "grok"]))
        return
    
    # Handle setting default model for provider
    if args.set_default_model:
        provider, model = args.set_default_model
        if app.config_manager.validate_provider(provider):
            if app.config_manager.validate_model_for_provider(provider, model):
                app.config_manager.set_default_model(provider, model)
                print(f"Default model for {provider} set to: {model}")
            else:
                # Show available models for the provider
                try:
                    from chat.factory import LLMProviderFactory
                    info = LLMProviderFactory.get_provider_info(provider)
                    print(f"Invalid model for {provider}: {model}")
                    print(f"Available models: {', '.join(info['available_models'])}")
                except Exception:
                    print(f"Invalid model for {provider}: {model}")
        else:
            print(f"Invalid provider: {provider}")
            print("Available providers:", ", ".join(["openai", "deepseek", "claude", "gemini", "grok"]))
        return
    
    # Handle provider/model listing
    if args.list_providers:
        app.list_providers()
        return
    
    if args.list_models:
        app.list_models(args.list_models)
        return
    
    # Determine provider and model from arguments
    provider = None
    model = args.model
    
    # Check shortcuts first
    if args.openai:
        provider = "openai"
    elif args.gpt4:
        provider = "openai"
        model = model or "gpt-4o"
    elif args.gpt4_mini:
        provider = "openai"
        model = model or "gpt-4o-mini"
    elif args.claude:
        provider = "claude"
    elif args.gemini:
        provider = "gemini"
    elif args.deepseek:
        provider = "deepseek"
    elif args.reasoner:
        provider = "deepseek"
        model = model or "deepseek-reasoner"
    elif args.grok:
        provider = "grok"
    elif args.provider:
        provider = args.provider
    
    # Start chat
    try:
        app.start_chat(provider=provider, model=model)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()