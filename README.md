# 🎀 Sweet Assistant - AI Front Desk for Healthcare

A sweet, voice-enabled AI assistant that simulates a healthcare front desk scenario, handling appointment scheduling and insurance verification with warm, natural conversation.

##Features

- **Voice Interface**: Speech-to-text and text-to-speech capabilities
- **AI-Powered Conversations**: GPT-3.5-turbo driven natural dialogue
- **Appointment Scheduling**: Books appointments with smart department/doctor matching
- **Insurance Verification**: Checks against accepted insurance providers
- **Sweet Personality**: Warm, empathetic healthcare-appropriate tone
- **Fallback Support**: Works even without API keys (text-only mode)

##Use Cases

- **Appointment Booking**: "I need to see a doctor about a rash next week"
- **Insurance Check**: "Do you accept Blue Cross insurance?"
- **Clinic Information**: "What are your hours?"

##Quick Start

### Prerequisites

- Python 3.8+
- macOS (for system voice) or ElevenLabs API key for premium voices
- OpenAI API key (optional, for enhanced AI responses)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/sandranicaj777/airserbiaaijob.git
cd ai-frontdesk

2.Create Virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3.Install dependencies
pip install -r requirements.txt

4.Set up environment variables
cp .env.example .env
# Edit .env with your API keys

API Keys (Optional)
Add to your .env file:
OPENAI_API_KEY=sk-your-openai-key-here
ELEVENLABS_API_KEY=sk-your-elevenlabs-key-here

Usage
Voice Mode (Recommended)
python sweet_assistant.py
Speak when you see "Listening..."


Text-Only Mode
python sweet_assistant.py
# Type your responses instead of speaking

Example Conversation
text
Assistant: Hello darling! I'm your sweet AI assistant. How can I help you today?
You: I need to book an appointment for a skin rash
Assistant: I'd love to help schedule your appointment! What's your name, darling?
You: My name is Alex
Assistant: Nice to meet you, Alex! I'm suggesting Dermatology for your skin rash. 
         Would you like to see Dr. Brown or Dr. Davis?

 Project Structure
text
sweet-assistant/
├── dialogue.py           # Main conversation logic & AI integration
├── sweet_voice.py        # Voice input/output (STT/TTS)  
├── sweet_assistant.py    # Main application entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file

 Supported Insurance Providers
-Blue Cross
-Aetna
-Cigna
-UnitedHealth
-Medicare

Voice Options:
 -Premium (ElevenLabs)
High-quality, natural female voice
Requires ElevenLabs API key

 -System (macOS)
Uses built-in "Samantha" voice
Works offline, no API required

 Limitations:
Prototype Scope: Simplified scheduling logic

Mock Data: Sample doctors, schedules, and insurance

Single Speaker: Optimized for one person at a time

English Only: Primary language support

Demo
Check the examples/ folder for sweet audio demonstrations!

Created with 💖 for the Confido AI take-home challenge

