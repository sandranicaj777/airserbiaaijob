import os
import random
from openai import OpenAI

class DialogueManager:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        self.conversation_history = []
        
        # Initialize OpenAI client
        if self.api_key and self.api_key.startswith('sk-'):
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("🎯 REAL AI ACTIVATED! Using OpenAI GPT")
            except Exception as e:
                print(f"❌ OpenAI setup failed: {e}")
                self.client = None
        else:
            print("🌟 Using SMART FALLBACK mode")
            self.client = None
        
        # Fallback responses (backup)
        self.fallback_responses = {
            'greeting': "Hello sunshine! 🌟 I'm your AI bestie! How can I assist you today?",
            'appointment': "I'd love to help schedule your appointment! What's your name, sunshine?",
            'insurance': "I can verify your insurance coverage! What's your provider, love?",
            'fallback': "I can help with appointments or insurance. What do you need, princess?"
        }

    def get_response(self, user_input):
        # Try real AI first
        if self.client:
            try:
                return self._get_ai_response(user_input)
            except Exception as e:
                print(f"⚠️ AI failed, using fallback: {e}")
                return self._get_fallback_response(user_input)
        
        # Use fallback if no AI
        return self._get_fallback_response(user_input)
    
    def _get_ai_response(self, user_input):
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Create system prompt with your personality
        system_prompt = """You are a friendly, warm AI assistant for a medical clinic. 
        Use natural, conversational language and occasionally use terms like 'princess', 'sunshine', 'love'.
        
        You ONLY handle:
        - Appointment scheduling (ask for name, preferred date/time)
        - Insurance verification (ask for provider name)
        - Basic clinic info (hours, location, services)
        
        Rules:
        1. Be super friendly and supportive
        2. Ask ONE question at a time
        3. Never give medical advice
        4. Keep responses concise but personal
        5. Use emojis occasionally 😊"""
        
        # Prepare messages for OpenAI
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 6 messages max)
        messages.extend(self.conversation_history[-6:])
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Add AI response to history
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        return ai_response
    
    def _get_fallback_response(self, user_input):
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            return self.fallback_responses['greeting']
        elif any(word in user_input_lower for word in ['appointment', 'schedule', 'book']):
            return self.fallback_responses['appointment']
        elif any(word in user_input_lower for word in ['insurance', 'coverage', 'verify']):
            return self.fallback_responses['insurance']
        else:
            return self.fallback_responses['fallback']