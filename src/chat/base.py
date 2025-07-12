#!/usr/bin/env python3
"""
Base LLM Chat Provider
Abstract base class for all LLM providers
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseLLMChat(ABC):
    """Abstract base class for LLM chat providers"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.provider_name = self.__class__.__name__.replace('Chat', '').lower()
        
    @abstractmethod
    def _get_default_model(self) -> str:
        """Return the default model for this provider"""
        pass
        
    @abstractmethod
    def _get_available_models(self) -> List[str]:
        """Return list of available models for this provider"""
        pass
        
    @abstractmethod
    def _make_api_request(self, messages: List[Dict[str, str]]) -> str:
        """Make API request to the provider and return response"""
        pass
        
    @abstractmethod
    def _get_api_key_env_var(self) -> str:
        """Return the environment variable name for the API key"""
        pass
        
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})
        
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        
    def get_response(self, user_input: str) -> str:
        """Get response from LLM provider"""
        self.add_message("user", user_input)
        
        try:
            response = self._make_api_request(self.conversation_history)
            self.add_message("assistant", response)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
            
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        return {
            "name": self.provider_name,
            "model": self.model,
            "available_models": self._get_available_models(),
            "default_model": self._get_default_model()
        }
        
    def set_model(self, model: str):
        """Set the model to use"""
        available_models = self._get_available_models()
        if model in available_models:
            self.model = model
        else:
            raise ValueError(f"Model {model} not available. Available models: {available_models}")