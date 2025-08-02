import os
import logging
from openai import OpenAI

class ChatbotService:
    def __init__(self):
        """Initialize the chatbot service with OpenAI API"""
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logging.warning("OPENAI_API_KEY not found in environment variables")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
        
        # System prompt for the chatbot
        self.system_prompt = {
            "role": "system",
            "content": """You are a helpful AI assistant. You provide clear, accurate, and helpful responses to user questions. 
            Be conversational but professional. If you're unsure about something, say so rather than guessing. 
            Keep your responses concise but informative."""
        }
    
    def get_response(self, conversation_history):
        """
        Get AI response for the conversation
        
        Args:
            conversation_history (list): List of message dictionaries with 'role' and 'content'
        
        Returns:
            str: AI response text
        """
        if not self.client:
            return "Sorry, the AI service is not available. Please check the API configuration."
        
        try:
            # Prepare messages with system prompt and conversation history
            messages = [self.system_prompt]
            
            # Add conversation history (limit to last 10 exchanges to manage token usage)
            recent_messages = conversation_history[-20:] if len(conversation_history) > 20 else conversation_history
            messages.extend(recent_messages)
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            
            # Handle specific OpenAI errors
            if "insufficient_quota" in str(e).lower():
                return "Sorry, the AI service quota has been exceeded. Please try again later."
            elif "invalid_api_key" in str(e).lower():
                return "Sorry, there's an issue with the AI service authentication."
            elif "rate_limit" in str(e).lower():
                return "Sorry, too many requests. Please wait a moment and try again."
            else:
                return f"Sorry, I encountered an error while processing your request. Please try again."
    
    def is_available(self):
        """Check if the chatbot service is available"""
        return self.client is not None and self.api_key is not None
