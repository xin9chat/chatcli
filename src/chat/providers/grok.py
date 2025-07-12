#!/usr/bin/env python3
"""
Grok Chat Provider (xAI)
"""

import os
from typing import List, Dict
from openai import OpenAI
from ..base import BaseLLMChat


class GrokChat(BaseLLMChat):
    """xAI Grok chat provider"""
    
    def __init__(self, api_key: str = None, model: str = None):
        super().__init__(api_key, model or self._get_default_model())
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1"
        )
        
    def _get_default_model(self) -> str:
        """Return the default model for Grok"""
        return "grok-4"
        
    def _get_available_models(self) -> List[str]:
        """Return list of available Grok models"""
        return ["grok-4", "grok-3", "grok-3-mini", "grok-beta"]
        
    def _make_api_request(self, messages: List[Dict[str, str]]) -> str:
        """Make API request to Grok"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content
        
    def _get_api_key_env_var(self) -> str:
        """Return the environment variable name for Grok API key"""
        return "XAI_API_KEY"