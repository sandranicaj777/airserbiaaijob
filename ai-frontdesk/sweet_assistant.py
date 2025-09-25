import os
from dotenv import load_dotenv

load_dotenv()

from dialogue import DialogueManager
from sweet_voice import SweetVoice, SimpleListener

print("🌸" * 20)
print("🌸   SWEET AI FRONT DESK ASSISTANT   🌸")
print("🌸" * 20)
print("🎀 Sunshine Healthcare")
print("🌸" * 20)

ai = DialogueManager()
voice = SweetVoice()
listener = SimpleListener(voice_mode=True) 

welcome_msg = "Hello darling! I'm your sweet AI assistant. How can I help you today?"
voice.speak_sweetly(welcome_msg)

while True:

    user_input = listener.get_input()
    
    if not user_input:
        continue
        
    if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye', 'q']:
        farewell = "Thank you for calling, sweetheart! Have a beautiful day!"
        print(f"🎀 Assistant: {farewell} 💖")
        voice.speak_sweetly(farewell)
        break
    

    response = ai.get_response(user_input)
    

    voice.speak_sweetly(response)
    print("━" * 50)