import os
from dotenv import load_dotenv


load_dotenv()

from dialogue import DialogueManager

print("🤖 Welcome to the BEST Front Desk Assistant! 🌟")
print("Hello sunshine! I'm your AI bestie. How can I assist you today?")


api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key loaded: {'Yes' if api_key and api_key.startswith('sk-') else 'No'}")

ai = DialogueManager()

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
        print("Thank you for calling, princess! Have an amazing day! 💖")
        break
        
    response = ai.get_response(user_input)
    print(f"Assistant: {response}")
