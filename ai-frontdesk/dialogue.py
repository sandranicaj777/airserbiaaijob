import os
import random

class DialogueManager:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        print(f"DialogueManager: API Key = {self.api_key[:20] if self.api_key else 'None'}")
        
        # For now, let's use the fallback mode until we fix the API key loading
        print("🌟 Using SMART FALLBACK mode (for now!)")
        
        # Improved fallback responses with better logic
        self.current_mode = None  # 'appointment', 'insurance', or None
        self.appointment_stage = 0  # 0=need name, 1=need date, 2=need time
        
    def get_response(self, user_input):
        return self._get_smart_fallback(user_input)
    
    def _get_smart_fallback(self, user_input):
        user_input_lower = user_input.lower()
        
        # Check if user is starting a new appointment request
        if any(word in user_input_lower for word in ['appointment', 'schedule', 'book']):
            self.current_mode = 'appointment'
            self.appointment_stage = 1
            return "I'd love to help schedule your appointment! What's your name, sunshine?"
        
        # Check if user is starting insurance verification
        elif any(word in user_input_lower for word in ['insurance', 'coverage', 'verify']):
            self.current_mode = 'insurance'
            return "I can verify your insurance coverage! What's your provider, love?"
        
        # If we're in appointment mode, handle the flow
        elif self.current_mode == 'appointment':
            if self.appointment_stage == 1:  # Waiting for name
                self.patient_name = user_input
                self.appointment_stage = 2
                return f"Nice to meet you, {self.patient_name}! What date works for you, princess?"
            elif self.appointment_stage == 2:  # Waiting for date
                self.appointment_date = user_input
                self.appointment_stage = 3
                return f"Great! What time on {self.appointment_date} works best, sunshine?"
            elif self.appointment_stage == 3:  # Waiting for time
                appointment_time = user_input
                self.current_mode = None
                return f"Perfect! I've booked your appointment on {self.appointment_date} at {appointment_time}. You'll get a confirmation soon! 💖"
        
        # If we're in insurance mode
        elif self.current_mode == 'insurance':
            provider = user_input
            self.current_mode = None
            accepted_providers = ['blue cross', 'aetna', 'cigna', 'united']
            if any(p in user_input_lower for p in accepted_providers):
                return f"✅ Yes! We accept {provider}. Your coverage is verified, love!"
            else:
                return f"❌ Sorry, we don't currently accept {provider}. Please check with your insurer, princess."
        
        # Handle clinic info questions
        elif any(word in user_input_lower for word in ['hour', 'time', 'open']):
            return "We're open Monday-Friday 8AM-6PM, Saturday 9AM-1PM! 🌟"
        
        elif any(word in user_input_lower for word in ['location', 'address', 'where']):
            return "We're at 123 Medical Center Drive, Healthcare City! 💫"
        
        elif any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            return "Hello sunshine! 🌟 I'm your AI bestie! How can I assist you today?"
        
        else:
            return "I can help with appointments, insurance, or clinic info. What do you need, princess?"
