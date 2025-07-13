#!/usr/bin/env python3
"""
Configuration Manager
Handles configuration for all LLM providers
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Configuration manager for ChatCLI"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".chatcli"
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Return default config if file doesn't exist or is invalid
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "default_provider": "openai",
            "providers": {
                "openai": {
                    "api_key": "",
                    "default_model": "gpt-4.1"
                },
                "deepseek": {
                    "api_key": "",
                    "default_model": "deepseek-chat"
                },
                "claude": {
                    "api_key": "",
                    "default_model": "claude-sonnet-4"
                },
                "gemini": {
                    "api_key": "",
                    "default_model": "gemini-2.5-pro"
                },
                "grok": {
                    "api_key": "",
                    "default_model": "grok-4"
                }
            },
            "settings": {
                "conversation_history_limit": 100,
                "auto_save_conversations": False,
                "show_response_time": False
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
        
        # Save config
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        # Set secure permissions
        os.chmod(self.config_file, 0o600)
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for a provider"""
        # First check environment variables
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY", 
            "claude": "ANTHROPIC_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "grok": "XAI_API_KEY"
        }
        
        env_key = os.getenv(env_vars.get(provider, ""))
        if env_key:
            return env_key
        
        # Then check config file
        return self.config.get("providers", {}).get(provider, {}).get("api_key", "")
    
    def set_api_key(self, provider: str, api_key: str):
        """Set API key for a provider"""
        if "providers" not in self.config:
            self.config["providers"] = {}
        if provider not in self.config["providers"]:
            self.config["providers"][provider] = {}
        
        self.config["providers"][provider]["api_key"] = api_key
        self.save_config()
    
    def get_default_provider(self) -> str:
        """Get default provider"""
        return self.config.get("default_provider", "openai")
    
    def set_default_provider(self, provider: str):
        """Set default provider"""
        self.config["default_provider"] = provider
        self.save_config()
    
    def get_default_model(self, provider: str) -> Optional[str]:
        """Get default model for a provider"""
        return self.config.get("providers", {}).get(provider, {}).get("default_model")
    
    def set_default_model(self, provider: str, model: str):
        """Set default model for a provider"""
        if "providers" not in self.config:
            self.config["providers"] = {}
        if provider not in self.config["providers"]:
            self.config["providers"][provider] = {}
        
        self.config["providers"][provider]["default_model"] = model
        self.save_config()
    
    def get_setting(self, key: str, default=None):
        """Get a setting value"""
        return self.config.get("settings", {}).get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """Set a setting value"""
        if "settings" not in self.config:
            self.config["settings"] = {}
        
        self.config["settings"][key] = value
        self.save_config()
    
    def setup_interactive(self):
        """Interactive setup for all providers"""
        print("ChatCLI Configuration Setup")
        print("=" * 30)
        print("Configure API keys for LLM providers")
        print("(Press Enter to skip a provider)")
        print()
        
        providers = {
            "openai": "OpenAI (ChatGPT)",
            "deepseek": "DeepSeek", 
            "claude": "Anthropic Claude",
            "gemini": "Google Gemini",
            "grok": "xAI Grok"
        }
        
        for provider_key, provider_name in providers.items():
            current_key = self.get_api_key(provider_key)
            if current_key:
                print(f"{provider_name}: Already configured")
                update = input(f"Update {provider_name} API key? (y/N): ").lower().strip()
                if update != 'y':
                    continue
            
            api_key = input(f"Enter {provider_name} API key: ").strip()
            if api_key:
                self.set_api_key(provider_key, api_key)
                print(f"{provider_name} API key saved.")
            print()
        
        # Set default provider
        print("Available providers:", ", ".join(providers.keys()))
        default_provider = input(f"Default provider (current: {self.get_default_provider()}): ").strip()
        if default_provider and default_provider in providers:
            self.set_default_provider(default_provider)
        
        print("\nConfiguration saved!")
        print(f"Config file: {self.config_file}")
    
    def validate_provider(self, provider: str) -> bool:
        """Validate if provider is supported"""
        supported_providers = ["openai", "deepseek", "claude", "gemini", "grok"]
        return provider.lower() in supported_providers
    
    def validate_model_for_provider(self, provider: str, model: str) -> bool:
        """Validate if model is available for the provider"""
        # Import here to avoid circular imports
        from ..chat.factory import LLMProviderFactory
        try:
            info = LLMProviderFactory.get_provider_info(provider)
            return model in info['available_models']
        except ValueError:
            return False
    
    def configure_defaults_interactive(self):
        """Interactive configuration for defaults only"""
        print("ChatCLI Default Configuration")
        print("=" * 30)
        
        # Configure default provider
        providers = ["openai", "deepseek", "claude", "gemini", "grok"]
        print("Available providers:", ", ".join(providers))
        current_default = self.get_default_provider()
        print(f"Current default provider: {current_default}")
        
        new_default = input("Set new default provider (press Enter to keep current): ").strip().lower()
        if new_default and self.validate_provider(new_default):
            self.set_default_provider(new_default)
            print(f"Default provider set to: {new_default}")
        elif new_default and not self.validate_provider(new_default):
            print(f"Invalid provider: {new_default}")
        
        print()
        
        # Configure default models
        print("Configure default models for each provider:")
        from ..chat.factory import LLMProviderFactory
        
        for provider in providers:
            try:
                info = LLMProviderFactory.get_provider_info(provider)
                current_model = self.get_default_model(provider)
                print(f"\n{provider.title()}:")
                print(f"  Current default: {current_model}")
                print(f"  Available models: {', '.join(info['available_models'])}")
                
                new_model = input(f"  Set default model for {provider} (press Enter to keep current): ").strip()
                if new_model:
                    if self.validate_model_for_provider(provider, new_model):
                        self.set_default_model(provider, new_model)
                        print(f"  Default model for {provider} set to: {new_model}")
                    else:
                        print(f"  Invalid model for {provider}: {new_model}")
            except Exception as e:
                print(f"  Error getting info for {provider}: {e}")
        
        print("\nConfiguration saved!")
    
    def show_config(self):
        """Show current configuration (without API keys)"""
        print("ChatCLI Configuration")
        print("=" * 30)
        print(f"Config file: {self.config_file}")
        print(f"Default provider: {self.get_default_provider()}")
        print()
        
        print("Providers:")
        for provider in ["openai", "deepseek", "claude", "gemini", "grok"]:
            api_key = self.get_api_key(provider)
            status = "✓ Configured" if api_key else "✗ Not configured"
            default_model = self.get_default_model(provider) or "default"
            print(f"  {provider}: {status} (model: {default_model})")
        
        print("\nSettings:")
        settings = self.config.get("settings", {})
        for key, value in settings.items():
            print(f"  {key}: {value}")
    
    def set_config_value(self, key: str, value: str) -> bool:
        """Set a configuration value via command line"""
        if key == "default_provider":
            if self.validate_provider(value):
                self.set_default_provider(value)
                print(f"Default provider set to: {value}")
                return True
            else:
                print(f"Invalid provider: {value}")
                return False
        
        elif key.startswith("default_model."):
            provider = key.split(".", 1)[1]
            if self.validate_provider(provider):
                if self.validate_model_for_provider(provider, value):
                    self.set_default_model(provider, value)
                    print(f"Default model for {provider} set to: {value}")
                    return True
                else:
                    print(f"Invalid model for {provider}: {value}")
                    return False
            else:
                print(f"Invalid provider: {provider}")
                return False
        
        else:
            print(f"Unknown configuration key: {key}")
            return False