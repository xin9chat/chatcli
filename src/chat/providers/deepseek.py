#!/usr/bin/env python3
"""
DeepSeek Chat Provider
"""

import os
from typing import List, Dict
from openai import OpenAI
from ..base import BaseLLMChat


class DeepSeekChat(BaseLLMChat):
    """DeepSeek chat provider"""
    
    def __init__(self, api_key: str = None, model: str = None):
        super().__init__(api_key, model or self._get_default_model())
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        
    def _get_default_model(self) -> str:
        """Return the default model for DeepSeek"""
        return "deepseek-chat"
        
    def _get_available_models(self) -> List[str]:
        """Return list of available DeepSeek models"""
        return ["deepseek-chat", "deepseek-reasoner"]
        
    def _make_api_request(self, messages: List[Dict[str, str]]) -> str:
        """Make API request to DeepSeek"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content
        
    def _get_api_key_env_var(self) -> str:
        """Return the environment variable name for DeepSeek API key"""
        return "DEEPSEEK_API_KEY"