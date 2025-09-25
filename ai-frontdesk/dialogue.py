import os
import random
from datetime import datetime, timedelta
from openai import OpenAI

class DialogueManager:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        self.conversation_history = []
        self.current_context = {
            'task': None,
            'patient_name': None,
            'reason': None,
            'suggested_department': None,
            'doctor': None,
            'appointment_time': None,
            'insurance_provider': None,
            'step': 0
        }
        
        if self.api_key and self.api_key.startswith('sk-'):
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("🎯 Using OpenAI GPT")
            except Exception as e:
                print(f"❌ OpenAI setup failed: {e}")
                self.client = None
        else:
            print("🌟 Using fallback mode")
            self.client = None
        
        self.clinic_info = {
            'name': "SweetCare Medical Clinic",
            'hours': "Monday-Friday: 8AM-6PM, Saturday: 9AM-1PM"
        }
        
        self.departments_doctors = {
            "General Practice": ["Dr. Smith", "Dr. Johnson", "Dr. Williams"],
            "Dermatology": ["Dr. Brown", "Dr. Davis"],
            "Cardiology": ["Dr. Miller", "Dr. Wilson"],
            "Pediatrics": ["Dr. Moore", "Dr. Taylor"]
        }
        
        self.symptom_mapping = {
            'headache': 'General Practice',
            'rash': 'Dermatology',
            'skin': 'Dermatology',
            'heart': 'Cardiology',
            'chest': 'Cardiology',
            'fever': 'General Practice',
            'checkup': 'General Practice',
            'children': 'Pediatrics',
            'child': 'Pediatrics'
        }
        
        self.accepted_insurance = ['Blue Cross', 'Aetna', 'Cigna', 'UnitedHealth', 'Medicare']
        self.available_slots = self._generate_time_slots()

    def get_response(self, user_input):
        self._update_context(user_input)
        
        if self.client:
            try:
                return self._get_ai_response(user_input)
            except Exception as e:
                print(f"⚠️ AI failed: {e}")
                return self._get_fallback_response(user_input)
        
        return self._get_fallback_response(user_input)
    
    def _update_context(self, user_input):
        input_lower = user_input.lower()
        
        if not self.current_context['task']:
            if any(word in input_lower for word in ['appointment', 'schedule', 'book', 'see doctor']):
                self.current_context['task'] = 'appointment'
                self.current_context['step'] = 1
        
        if self.current_context['step'] == 1 and not self.current_context['patient_name']:
            if any(word in input_lower for word in ['name', "i'm", 'call me']):
                name = self._extract_name(user_input)
                if name:
                    self.current_context['patient_name'] = name
                    self.current_context['step'] = 2
        
        if self.current_context['step'] == 2 and not self.current_context['reason']:
            self.current_context['reason'] = user_input
            department = self._suggest_department(user_input)
            if department:
                self.current_context['suggested_department'] = department
                self.current_context['step'] = 3
        
        if self.current_context['step'] == 3 and not self.current_context['doctor']:
            doctor = self._extract_doctor(user_input)
            if doctor:
                self.current_context['doctor'] = doctor
                self.current_context['step'] = 4
        
        if self.current_context['step'] == 4 and not self.current_context['appointment_time']:
            if any(word in input_lower for word in ['time', 'when', 'schedule', 'appointment', 'monday', 'tuesday']):
                time_pref = self._extract_time_preference(user_input)
                if time_pref:
                    self.current_context['appointment_time'] = time_pref
                    self.current_context['step'] = 5
        
        if 'insurance' in input_lower and not self.current_context['insurance_provider']:
            provider = self._extract_insurance_provider(user_input)
            if provider:
                self.current_context['insurance_provider'] = provider
    
    def _get_ai_response(self, user_input):
        system_prompt = self._create_system_prompt()
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if self.conversation_history:
            messages.extend(self.conversation_history[-6:])
        
        messages.append({"role": "user", "content": user_input})
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=250,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        if len(self.conversation_history) > 12:
            self.conversation_history = self.conversation_history[-12:]
        
        return ai_response
    
    def _create_system_prompt(self):
        insurance_status = ""
        if self.current_context['insurance_provider']:
            is_accepted = self.current_context['insurance_provider'] in self.accepted_insurance
            status = "ACCEPTED 🌟" if is_accepted else "NOT ACCEPTED ❌"
            insurance_status = f"\nINSURANCE STATUS: {self.current_context['insurance_provider']} is {status}"
        
        base_prompt = f"""You are SweetCare, a warm AI assistant. Use sweet terms like 'sunshine', 'love', 'dear'.

        CONVERSATION FLOW:
        Step {self.current_context['step']}:
        - Name: {self.current_context['patient_name'] or 'not asked yet'}
        - Reason: {self.current_context['reason'] or 'not asked yet'}
        - Suggested Department: {self.current_context['suggested_department'] or 'not suggested yet'}
        - Doctor: {self.current_context['doctor'] or 'not chosen yet'}
        - Time: {self.current_context['appointment_time'] or 'not scheduled yet'}
        {insurance_status}

        REQUIRED FLOW:
        1. Ask for patient's name
        2. Ask why they want to book appointment
        3. Suggest appropriate department based on symptoms
        4. Offer doctor choices from that department
        5. Ask for preferred appointment time
        6. Handle insurance verification

        ACCEPTED INSURANCE ONLY: {', '.join(self.accepted_insurance)}
        REJECT all other insurance providers clearly.

        DEPARTMENT SUGGESTIONS:
        - headache/fever/checkup → General Practice
        - rash/skin → Dermatology  
        - heart/chest → Cardiology
        - children → Pediatrics

        Be natural, ask one question at a time, remember context."""

        return base_prompt
    
    def _suggest_department(self, user_input):
        input_lower = user_input.lower()
        for symptom, department in self.symptom_mapping.items():
            if symptom in input_lower:
                return department
        return "General Practice"
    
    def _extract_doctor(self, user_input):
        input_lower = user_input.lower()
        if self.current_context['suggested_department']:
            for doctor in self.departments_doctors.get(self.current_context['suggested_department'], []):
                if doctor.lower() in input_lower:
                    return doctor
        return None
    
    def _extract_insurance_provider(self, user_input):
        input_lower = user_input.lower()
        for provider in self.accepted_insurance:
            if provider.lower() in input_lower:
                return provider
        return None
    
    def _extract_name(self, text):
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in ['my', 'name', 'is', "i'm"] and i + 1 < len(words):
                name = words[i + 1].strip('.,!?')
                return name.title()
        return None
    
    def _extract_time_preference(self, text):
        input_lower = text.lower()
        if 'tomorrow' in input_lower:
            return "tomorrow"
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
            if day in input_lower:
                return day
        return None
    
    def _generate_time_slots(self):
        base_date = datetime.now() + timedelta(days=1)
        slots = []
        for i in range(7):
            slot_date = base_date + timedelta(days=i)
            if slot_date.weekday() < 6:
                slots.append(slot_date.strftime("%A"))
        return slots
    
    def _get_fallback_response(self, user_input):
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            return "Hello sunshine! 🌟 How can I help you today?"
        elif any(word in user_input_lower for word in ['appointment', 'schedule', 'book']):
            return "I'd love to help schedule your appointment! What's your name, darling?"
        elif any(word in user_input_lower for word in ['insurance', 'coverage']):
            return "I can verify your insurance! What's your provider name, love?"
        else:
            return "I can help with appointments or insurance. What do you need, princess?"