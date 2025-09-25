import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from dialogue import DialogueManager
from sweet_voice import SweetVoice, SimpleListener

print("🌸" * 20)
print("🌸   SWEET AI FRONT DESK ASSISTANT   🌸")
print("🌸" * 20)
print("🎯 AI-Powered • 🎀 Sweet Voice • ⚕️ Healthcare")
print("🌸" * 20)

ai = DialogueManager()
voice = SweetVoice()
listener = SimpleListener()

# Sweet welcome message
welcome_msg = "Hello darling! I'm your sweet AI assistant. How may I help you today?"
voice.speak_sweetly(welcome_msg)

while True:
    # Get user input
    user_input = listener.get_input()
    
    if not user_input:
        continue
        
    # Exit command
    if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye', 'q']:
        farewell = "Thank you for calling, sweetheart! Have a beautiful day!"
        print(f"🎀 Assistant: {farewell} 💖")
        voice.speak_sweetly(farewell)
        break
    
    # Get AI response
    response = ai.get_response(user_input)
    
    # Speak with clean text
    voice.speak_sweetly(response)
    print("━" * 50)
