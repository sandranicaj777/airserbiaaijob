# System Design Document: SweetCare AI Assistant

## Architecture Overview

The system follows a modular pipeline architecture:

### Components Interaction:
1. **STT Module**: Converts spoken audio to text using Google Speech Recognition
2. **Dialogue Manager**: Processes text using OpenAI GPT-3.5 with state tracking
3. **Backend Simulator**: Mock calendar and insurance database
4. **TTS Module**: Converts AI responses to speech using ElevenLabs or macOS voices

## Tech Stack & Tools

### Speech-to-Text: Google Speech Recognition
- **Choice Reason**: Free, accurate, easy to implement
- **Alternative Considered**: OpenAI Whisper (more accurate but heavier)

### Large Language Model: OpenAI GPT-3.5-turbo
- **Choice Reason**: Good balance of cost, speed, and capability
- **Alternative**: GPT-4 (better but more expensive)

### Text-to-Speech: ElevenLabs + macOS fallback
- **Choice Reason**: ElevenLabs provides high-quality voices, macOS fallback ensures reliability
- **Alternative**: Google Cloud TTS (considered but ElevenLabs has better voice quality)

## Prompt Engineering Strategy

### System Prompt Design:
- **Role Definition**: Clear clinic assistant persona with specific boundaries
- **State Awareness**: Includes current conversation state in the prompt
- **Flow Guidance**: Explicit appointment and insurance verification workflows
- **Safety Rules**: No medical advice, one question at a time

### Challenges & Solutions:
- **Challenge**: LLM going off-topic
- **Solution**: Strict system prompt with explicit rules and state context
- **Challenge**: Handling ambiguous user inputs
- **Solution**: Multi-step clarification process with state tracking

## Assumptions & Limitations

### Current Assumptions:
- Single speaker environment
- Clear audio input without background noise
- English language only
- Basic date/time formats (no complex scheduling)

### Current Limitations:
- No persistent conversation storage
- Limited error handling for speech recognition failures
- Mock backend only (no real calendar integration)
- No HIPAA compliance for patient data

### Future Improvements:
- Real calendar API integration (Google Calendar, Outlook)
- Enhanced error handling and fallback mechanisms
- HIPAA-compliant data handling
- Multi-language support
- Real-time conversation analytics
