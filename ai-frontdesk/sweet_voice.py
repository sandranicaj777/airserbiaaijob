import os
import requests
import platform
import re

class SweetVoice:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_enabled = False
        
        if self.api_key and self.api_key.startswith('sk_'):
            self.voice_enabled = True
            print("🎀 SWEET VOICE READY! Using ElevenLabs")
        else:
            print("🎀 Using macOS system voice (Samantha)")
    
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
                with open("sweet_voice.mp3", "wb") as f:
                    f.write(response.content)
                
                os.system("afplay sweet_voice.mp3")
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
            print("Speaking with Samantha(MAC Os sweet lady princess) voice")
            return True
        except Exception as e:
            try:
                os.system(f'say "{text}"')
                print("Speaking with default voice")
                return True
            except:
                print(f" [Voice would say]: {text}")
                return True

class SimpleListener:
    def __init__(self):
        print("🎀 Text-based assistant ready! (Voice output only)")
    
    def get_input(self):
        """Simple text input - no voice simulation"""
        return input("You: ").strip()
