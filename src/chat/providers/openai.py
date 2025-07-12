#!/usr/bin/env python3
"""
OpenAI Chat Provider (ChatGPT)
"""

import os
from typing import List, Dict
from openai import OpenAI
from ..base import BaseLLMChat


class OpenAIChat(BaseLLMChat):
    """OpenAI ChatGPT chat provider"""
    
    def __init__(self, api_key: str = None, model: str = None):
        super().__init__(api_key, model or self._get_default_model())
        self.client = OpenAI(api_key=self.api_key)
        
    def _get_default_model(self) -> str:
        """Return the default model for OpenAI"""
        return "gpt-4o-mini"
        
    def _get_available_models(self) -> List[str]:
        """Return list of available OpenAI models"""
        return [
            "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4",
            "gpt-3.5-turbo", "o1-preview", "o1-mini"
        ]
        
    def _make_api_request(self, messages: List[Dict[str, str]]) -> str:
        """Make API request to OpenAI"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
        
    def _get_api_key_env_var(self) -> str:
        """Return the environment variable name for OpenAI API key"""
        return "OPENAI_API_KEY"