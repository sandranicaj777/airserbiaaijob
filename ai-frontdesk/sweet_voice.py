import os
import requests
import platform
import re
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import io

class SweetVoice:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_enabled = False
        
        if self.api_key and self.api_key.startswith('sk_'):
            self.voice_enabled = True
            print("🎀 SWEET VOICE READY! Using ElevenLabs")
        else:
            print("🎀 Using macOS system voice (Samantha)")
        
  
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.setup_microphone()
    
    def setup_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                print("Preparing microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone ready!")
        except:
            print("Microphone not available, using text input only")
    
    def listen_sweetly(self):
        """Listen to user voice input and convert to text"""
        try:
            print("Listening... (speak now)")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"👂 Heard: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except Exception as e:
            print(f" Microphone error: {e}")
            return input("Type your message: ").strip()
    
    def speak_sweetly(self, text):
        """Speak with a sweet feminine voice - CLEAN EMOJIS"""
        print(f"🎀 Assistant: {text}")
        
        clean_text = self._remove_emojis(text)
        
        if self.voice_enabled:
            success = self._elevenlabs_speak(clean_text)
            if not success:
                return self._macos_speak(clean_text)
        else:
            return self._macos_speak(clean_text)
    
    def _remove_emojis(self, text):
        """Remove emojis and special characters that sound weird when spoken"""
        clean_text = re.sub(r'[^\w\s.,!?;:]', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text
    
    def _elevenlabs_speak(self, text):
        """Use ElevenLabs API for high-quality sweet voice"""
        try:
            url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.7,
                    "similarity_boost": 0.8
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
                play(audio)
                return True
            else:
                print(f"ElevenLabs error {response.status_code}, using macOS voice")
                return False
                
        except Exception as e:
            print(f"ElevenLabs failed: {e}, using macOS voice")
            return False
    
    def _macos_speak(self, text):
        """Use macOS built-in sweet female voice - SAMANTHA"""
        try:
            os.system(f'say -v "Samantha" "{text}"')
            return True
        except Exception as e:
            try:
                os.system(f'say "{text}"')
                return True
            except:
                print(f" [Voice would say]: {text}")
                return True

class SimpleListener:
    def __init__(self, voice_mode=True):
        self.voice_mode = voice_mode
        self.voice = SweetVoice() if voice_mode else None
    
    def get_input(self):
        """Get input via voice or text"""
        if self.voice_mode and self.voice:
            user_input = self.voice.listen_sweetly()
            if user_input:
                return user_input
        return input("You (type): ").strip()