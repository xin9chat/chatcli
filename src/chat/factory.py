#!/usr/bin/env python3
"""
LLM Provider Factory
Factory class for creating LLM provider instances
"""

import os
from typing import Dict, Type, Optional, List
from .base import BaseLLMChat
from .providers.deepseek import DeepSeekChat
from .providers.openai import OpenAIChat
from .providers.claude import ClaudeChat
from .providers.gemini import GeminiChat
from .providers.grok import GrokChat


class LLMProviderFactory:
    """Factory for creating LLM provider instances"""
    
    # Registry of available providers
    PROVIDERS: Dict[str, Type[BaseLLMChat]] = {
        "deepseek": DeepSeekChat,
        "openai": OpenAIChat,
        "claude": ClaudeChat,
        "gemini": GeminiChat,
        "grok": GrokChat
    }
    
    # Provider aliases for convenience
    ALIASES = {
        "chatgpt": "openai",
        "gpt": "openai",
        "anthropic": "claude",
        "google": "gemini",
        "xai": "grok"
    }
    
    @classmethod
    def get_provider_names(cls) -> List[str]:
        """Get list of available provider names"""
        return list(cls.PROVIDERS.keys())
    
    @classmethod
    def get_provider_aliases(cls) -> Dict[str, str]:
        """Get provider aliases mapping"""
        return cls.ALIASES.copy()
    
    @classmethod
    def resolve_provider_name(cls, name: str) -> str:
        """Resolve provider name from aliases"""
        name = name.lower()
        return cls.ALIASES.get(name, name)
    
    @classmethod
    def create_provider(cls, provider_name: str, api_key: str = None, model: str = None) -> BaseLLMChat:
        """Create a provider instance"""
        provider_name = cls.resolve_provider_name(provider_name)
        
        if provider_name not in cls.PROVIDERS:
            available = ", ".join(cls.PROVIDERS.keys())
            raise ValueError(f"Unknown provider: {provider_name}. Available: {available}")
        
        provider_class = cls.PROVIDERS[provider_name]
        
        # Try to get API key from environment if not provided
        if api_key is None:
            instance = provider_class.__new__(provider_class)
            env_var = instance._get_api_key_env_var()
            api_key = os.getenv(env_var)
        
        if api_key is None:
            raise ValueError(f"API key required for {provider_name}. Set {instance._get_api_key_env_var()} environment variable or provide api_key parameter.")
        
        return provider_class(api_key=api_key, model=model)
    
    @classmethod
    def auto_detect_provider(cls, model: str = None) -> str:
        """Auto-detect provider based on model name"""
        if not model:
            return "openai"  # Default provider
        
        model = model.lower()
        
        # Model name patterns for auto-detection
        if "gpt" in model or "o1" in model:
            return "openai"
        elif "claude" in model:
            return "claude"
        elif "gemini" in model:
            return "gemini"
        elif "deepseek" in model:
            return "deepseek"
        elif "grok" in model:
            return "grok"
        else:
            return "openai"  # Default fallback
    
    @classmethod
    def get_provider_info(cls, provider_name: str = None) -> Dict:
        """Get information about a provider or all providers"""
        if provider_name:
            provider_name = cls.resolve_provider_name(provider_name)
            if provider_name not in cls.PROVIDERS:
                raise ValueError(f"Unknown provider: {provider_name}")
            
            # Create a temporary instance to get info
            provider_class = cls.PROVIDERS[provider_name]
            temp_instance = provider_class.__new__(provider_class)
            return {
                "name": provider_name,
                "class": provider_class.__name__,
                "default_model": temp_instance._get_default_model(),
                "available_models": temp_instance._get_available_models(),
                "api_key_env": temp_instance._get_api_key_env_var()
            }
        else:
            # Return info for all providers
            info = {}
            for name in cls.PROVIDERS:
                info[name] = cls.get_provider_info(name)
            return info