import os
from openai import OpenAI
from typing import List, Dict, Optional, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentBrain:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 20
        
        self.system_prompt = """You are a helpful, professional, and intelligent AI assistant. 
You provide clear, concise, and accurate responses. You are friendly but professional.
Keep your responses conversational and natural for voice interaction.
Avoid overly long responses - aim for clarity and brevity."""
        
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def process_input(
        self, 
        user_input: str, 
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> str:
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = [
                    self.conversation_history[0]
                ] + self.conversation_history[-(self.max_history-1):]
            
            if stream_callback:
                response_text = ""
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    stream=True,
                    temperature=0.7,
                    max_tokens=500
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        response_text += content
                        stream_callback(content)
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                
                return response_text
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=0.7,
                    max_tokens=500
                )
                
                response_text = response.choices[0].message.content
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                
                return response_text
        
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            logger.error(error_msg)
            return "I apologize, but I encountered an error processing your request. Please try again."
    
    def clear_history(self):
        self.conversation_history = [{
            "role": "system",
            "content": self.system_prompt
        }]
    
    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt
        self.conversation_history[0] = {
            "role": "system",
            "content": prompt
        }
