from dialogue import DialogueManager

print("🤖 Welcome to the BEST Front Desk Assistant! 🌟")
print("Hello sunshine! I'm your AI bestie. How can I assist you today?")

ai = DialogueManager()

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
        print("Thank you for calling, princess! Have an amazing day! 💖")
        break
        
    response = ai.get_response(user_input)
    print(f"Assistant: {response}")