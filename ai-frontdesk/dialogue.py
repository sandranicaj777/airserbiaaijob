class DialogueManager:
    def get_response(self, user_input):
        user_input = user_input.lower()
        
        if "hello" in user_input or "hi" in user_input:
            return "Hello! I'm your AI bestie. How could I assist you today sunshine?"
        elif "appointment" in user_input:
            return "I can def help to schedule an appointment! What's your name princess?"
        elif "insurance" in user_input:
            return "I can absolutely verify insurance coverage love. What's your insurance provider?"
        else:
            return "I can help with both appointments or insurance. What do you need?"