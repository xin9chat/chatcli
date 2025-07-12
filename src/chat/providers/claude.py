#!/usr/bin/env python3
"""
Claude Chat Provider (Anthropic)
"""

import os
from typing import List, Dict
from anthropic import Anthropic
from ..base import BaseLLMChat


class ClaudeChat(BaseLLMChat):
    """Anthropic Claude chat provider"""
    
    def __init__(self, api_key: str = None, model: str = None):
        super().__init__(api_key, model or self._get_default_model())
        self.client = Anthropic(api_key=self.api_key)
        
    def _get_default_model(self) -> str:
        """Return the default model for Claude"""
        return "claude-3-5-sonnet-20241022"
        
    def _get_available_models(self) -> List[str]:
        """Return list of available Claude models"""
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
        
    def _make_api_request(self, messages: List[Dict[str, str]]) -> str:
        """Make API request to Claude"""
        # Claude expects system messages to be separate
        system_message = None
        chat_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                chat_messages.append(msg)
        
        kwargs = {
            "model": self.model,
            "max_tokens": 4000,
            "messages": chat_messages
        }
        
        if system_message:
            kwargs["system"] = system_message
            
        response = self.client.messages.create(**kwargs)
        return response.content[0].text
        
    def _get_api_key_env_var(self) -> str:
        """Return the environment variable name for Claude API key"""
        return "ANTHROPIC_API_KEY"