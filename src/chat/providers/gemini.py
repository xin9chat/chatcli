#!/usr/bin/env python3
"""
Gemini Chat Provider (Google)
"""

import os
from typing import List, Dict
import google.generativeai as genai
from ..base import BaseLLMChat


class GeminiChat(BaseLLMChat):
    """Google Gemini chat provider"""
    
    def __init__(self, api_key: str = None, model: str = None):
        super().__init__(api_key, model or self._get_default_model())
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
        self.chat_session = None
        
    def _get_default_model(self) -> str:
        """Return the default model for Gemini"""
        return "gemini-2.0-flash"
        
    def _get_available_models(self) -> List[str]:
        """Return list of available Gemini models"""
        return [
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ]
        
    def _make_api_request(self, messages: List[Dict[str, str]]) -> str:
        """Make API request to Gemini"""
        # If this is the first message or we need to reset the chat
        if self.chat_session is None or len(messages) == 1:
            self.chat_session = self.client.start_chat(history=[])
        
        # Get the last user message
        user_message = messages[-1]["content"]
        
        response = self.chat_session.send_message(user_message)
        return response.text
        
    def _get_api_key_env_var(self) -> str:
        """Return the environment variable name for Gemini API key"""
        return "GOOGLE_API_KEY"
        
    def clear_history(self):
        """Clear conversation history and reset chat session"""
        super().clear_history()
        self.chat_session = None