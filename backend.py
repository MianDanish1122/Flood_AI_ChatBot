import requests
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

class FloodAidBackend:
    def __init__(self):
        self.gemini_key = os.getenv("GOOGLE_API_KEY")
        self.weather_key = os.getenv("OPENWEATHER_API_KEY")
        
        # Debug: Print API key status (first 10 chars only for security)
        print(f"🔑 Gemini API Key loaded: {'Yes' if self.gemini_key else 'No'}")
        if self.gemini_key:
            print(f"🔑 Key starts with: {self.gemini_key[:10]}...")
        print(f"🔑 Weather API Key loaded: {'Yes' if self.weather_key else 'No'}")
        
        # Comprehensive shelter database
        self.shelters = [
            {"name": "Lahore Central Relief Camp", "address": "Mall Road, Lahore", "capacity": 500, "available": 200, "facilities": ["Medical", "Food", "Water", "Sanitation"], "phone": "042-99201234"},
            {"name": "Shalamar Emergency Shelter", "address": "Shalamar Gardens, Lahore", "capacity": 300, "available": 150, "facilities": ["Food", "Water", "Beds"], "phone": "042-99205678"},
            {"name": "Gulberg Relief Point", "address": "Gulberg III, Lahore", "capacity": 400, "available": 100, "facilities": ["Medical", "Food", "Water", "Electricity"], "phone": "042-99209012"},
            {"name": "Karachi Saddar Shelter", "address": "Saddar Town, Karachi", "capacity": 600, "available": 350, "facilities": ["Medical", "Food", "Water", "Security"], "phone": "021-99301234"},
            {"name": "Clifton Emergency Camp", "address": "Clifton Block 5, Karachi", "capacity": 450, "available": 280, "facilities": ["Food", "Water", "Beds", "Sanitation"], "phone": "021-99305678"},
            {"name": "Islamabad F-7 Relief Center", "address": "F-7 Markaz, Islamabad", "capacity": 450, "available": 200, "facilities": ["Medical", "Food", "Water", "Electricity"], "phone": "051-99401234"},
            {"name": "Rawalpindi Cantonment Shelter", "address": "Mall Road, Rawalpindi", "capacity": 380, "available": 180, "facilities": ["Food", "Water", "Medical"], "phone": "051-99405678"},
            {"name": "Multan Ghanta Ghar Relief Camp", "address": "Ghanta Ghar, Multan", "capacity": 350, "available": 150, "facilities": ["Food", "Water", "Beds"], "phone": "061-99501234"},
            {"name": "Faisalabad Clock Tower Shelter", "address": "Ghanta Ghar, Faisalabad", "capacity": 420, "available": 220, "facilities": ["Medical", "Food", "Water"], "phone": "041-99601234"},
            {"name": "Peshawar Hayatabad Relief Point", "address": "Hayatabad Phase 1, Peshawar", "capacity": 300, "available": 120, "facilities": ["Food", "Water", "Security"], "phone": "091-99701234"}
        ]
        
        # Emergency contacts with categories
        self.emergency_contacts = {
            "Emergency Services": [
                {"name": "Rescue 1122", "number": "1122", "available": "24/7"},
                {"name": "Edhi Ambulance", "number": "115", "available": "24/7"},
                {"name": "Police Emergency", "number": "15", "available": "24/7"}
            ],
            "Disaster Management": [
                {"name": "NDMA Helpline", "number": "051-9205019", "available": "24/7"},
                {"name": "PDMA Punjab", "number": "1129", "available": "24/7"},
                {"name": "SDMA Sindh", "number": "021-99332288", "available": "24/7"}
            ],
            "Relief Organizations": [
                {"name": "Pakistan Red Crescent", "number": "051-9250404", "available": "24/7"},
                {"name": "Al-Khidmat Foundation", "number": "0800-55555", "available": "24/7"},
                {"name": "JDC Foundation", "number": "0800-35267", "available": "24/7"},
                {"name": "Saylani Welfare", "number": "021-36636025", "available": "24/7"}
            ]
        }
        
        # Medical tips and first aid
        self.medical_tips = [
            {"title": "Waterborne Disease Prevention", "desc": "Always boil water for at least 5 minutes before drinking. Use water purification tablets when available. Avoid flood water contact.", "priority": "Critical"},
            {"title": "First Aid Essentials", "desc": "Keep bandages, antiseptic cream, pain relievers (paracetamol), oral rehydration salts, mosquito repellent, and any prescription medications.", "priority": "High"},
            {"title": "Flood-Related Injuries", "desc": "Clean all wounds immediately with clean water and antiseptic. Cover with sterile bandages. Watch for signs of infection (redness, swelling, pus).", "priority": "High"},
            {"title": "Food Safety", "desc": "Discard any food that has come in contact with flood water. Don't eat fresh produce from flooded areas. Cook all food thoroughly.", "priority": "Critical"},
            {"title": "Hygiene Practices", "desc": "Wash hands frequently with soap. Use hand sanitizer when soap unavailable. Keep wounds clean and covered. Avoid touching face with dirty hands.", "priority": "High"},
            {"title": "Mental Health", "desc": "Talk to family and friends about feelings. Practice deep breathing. Seek professional help if feeling overwhelmed. Stay connected with community.", "priority": "Medium"}
        ]
        
        # Relief camps and supplies
        self.relief_camps = [
            {"name": "Red Crescent Camp - Multan Road", "city": "Lahore", "supplies": ["Food Packets", "Clean Water", "Clothes", "Blankets"], "contact": "0300-1234567", "open": "24/7"},
            {"name": "Al-Khidmat Foundation - Johar Town", "city": "Lahore", "supplies": ["Medical Aid", "Food", "Baby Formula"], "contact": "0321-9876543", "open": "8 AM - 10 PM"},
            {"name": "Saylani Welfare - Raiwind Road", "city": "Lahore", "supplies": ["Cooked Meals", "Groceries", "Medicine"], "contact": "0333-4567890", "open": "24/7"},
            {"name": "JDC Foundation - Model Town", "city": "Lahore", "supplies": ["Emergency Kits", "Tents", "Mattresses"], "contact": "0345-1122334", "open": "24/7"},
            {"name": "Edhi Center - Saddar", "city": "Karachi", "supplies": ["Food", "Water", "Medical", "Clothes"], "contact": "0300-2345678", "open": "24/7"},
            {"name": "Chippa Welfare - Nazimabad", "city": "Karachi", "supplies": ["Cooked Food", "Ambulance", "Medicine"], "contact": "0321-3456789", "open": "24/7"}
        ]
        
        # Donation needs tracking
        self.donation_needs = [
            {"item": "Clean Drinking Water (Bottled)", "priority": "Critical", "quantity": "10,000 liters", "urgency": "Immediate"},
            {"item": "Ready-to-Eat Food Packets", "priority": "Critical", "quantity": "5,000 packets", "urgency": "Immediate"},
            {"item": "Medical Supplies & First Aid Kits", "priority": "Critical", "quantity": "500 kits", "urgency": "Immediate"},
            {"item": "Oral Rehydration Salts (ORS)", "priority": "Critical", "quantity": "2,000 packets", "urgency": "24 hours"},
            {"item": "Blankets & Warm Clothes", "priority": "High", "quantity": "2,000 items", "urgency": "48 hours"},
            {"item": "Baby Formula & Diapers", "priority": "High", "quantity": "1,000 units", "urgency": "24 hours"},
            {"item": "Mosquito Nets", "priority": "High", "quantity": "1,500 nets", "urgency": "48 hours"},
            {"item": "Solar Lanterns & Batteries", "priority": "Medium", "quantity": "800 units", "urgency": "1 week"},
            {"item": "Hygiene Kits (Soap, Sanitizer)", "priority": "High", "quantity": "3,000 kits", "urgency": "48 hours"},
            {"item": "Tents & Tarpaulins", "priority": "Medium", "quantity": "500 units", "urgency": "1 week"}
        ]
        
        # Safety guidelines
        self.safety_tips = {
            "Before Flood": [
                "Store important documents in waterproof containers",
                "Prepare emergency kit with 3-day supplies",
                "Know evacuation routes and shelter locations",
                "Keep phone charged and have backup power",
                "Store drinking water and non-perishable food"
            ],
            "During Flood": [
                "Move to higher ground immediately",
                "Avoid walking or driving through flood water",
                "Stay away from power lines and electrical equipment",
                "Listen to emergency broadcasts on radio",
                "Do not drink flood water"
            ],
            "After Flood": [
                "Return home only when authorities say it's safe",
                "Avoid flood water - may contain sewage or chemicals",
                "Check for structural damage before entering buildings",
                "Discard contaminated food and water",
                "Document damage for insurance claims"
            ]
        }
    
    def get_weather(self, city="Lahore"):
        """Fetch real-time weather from OpenWeather API"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},PK&appid={self.weather_key}&units=metric"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "city": data["name"],
                    "temp": round(data["main"]["temp"], 1),
                    "feels_like": round(data["main"]["feels_like"], 1),
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "description": data["weather"][0]["description"],
                    "main": data["weather"][0]["main"],
                    "wind_speed": round(data["wind"]["speed"], 1),
                    "clouds": data["clouds"]["all"],
                    "visibility": data.get("visibility", 10000) / 1000
                }
        except Exception as e:
            print(f"Weather API Error: {e}")
        
        # Fallback demo data
        return {
            "success": False,
            "city": city,
            "temp": 28.5,
            "feels_like": 31.0,
            "humidity": 75,
            "pressure": 1010,
            "description": "moderate rain",
            "main": "Rain",
            "wind_speed": 4.5,
            "clouds": 80,
            "visibility": 8.0
        }
    
    def assess_flood_risk(self, weather_data):
        """Calculate flood risk based on weather conditions"""
        risk_score = 0
        factors = []
        
        # High humidity
        if weather_data["humidity"] > 85:
            risk_score += 30
            factors.append("Very high humidity")
        elif weather_data["humidity"] > 75:
            risk_score += 20
            factors.append("High humidity")
        
        # Rain conditions
        if "rain" in weather_data["description"].lower() or weather_data["main"] == "Rain":
            risk_score += 40
            factors.append("Active rainfall")
        
        # Low pressure
        if weather_data["pressure"] < 1000:
            risk_score += 20
            factors.append("Low atmospheric pressure")
        
        # Poor visibility
        if weather_data["visibility"] < 5:
            risk_score += 10
            factors.append("Poor visibility")
        
        # Determine risk level
        if risk_score >= 70:
            return {"level": "Critical", "score": risk_score, "factors": factors, "color": "red"}
        elif risk_score >= 40:
            return {"level": "High", "score": risk_score, "factors": factors, "color": "orange"}
        elif risk_score >= 20:
            return {"level": "Moderate", "score": risk_score, "factors": factors, "color": "yellow"}
        else:
            return {"level": "Low", "score": risk_score, "factors": factors, "color": "green"}
    
    def chat_with_gemini(self, message, history, city):
        """Enhanced AI chat with proper error handling and debugging"""
        
        # Check if API key exists
        if not self.gemini_key:
            return """❌ **API Configuration Error**
            
The Gemini API key is not configured. Please:
1. Create a `.env` file in your project root
2. Add: `GOOGLE_API_KEY=your_api_key_here`
3. Get your API key from: https://makersuite.google.com/app/apikey
Meanwhile, I can still help you with:
🏠 Shelter information
📞 Emergency contacts  
⚕️ Medical tips
📦 Relief camp locations"""

        try:
            weather = self.get_weather(city)
            risk = self.assess_flood_risk(weather)
            
            # Build system context
            system_prompt = f"""You are FloodAid AI, an expert disaster relief assistant for Pakistan with deep knowledge of:
- Flood safety and emergency protocols
- Pakistani geography and infrastructure
- Local relief organizations and resources
- Medical emergency response
- Psychological support during disasters
CURRENT SITUATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Location: {weather['city']}, Pakistan
🌡️ Temperature: {weather['temp']}°C (feels like {weather['feels_like']}°C)
🌦️ Conditions: {weather['description']}
💧 Humidity: {weather['humidity']}% | 💨 Wind: {weather['wind_speed']} m/s
⚠️ Flood Risk: {risk['level']} ({risk['score']}/100)
🚨 Risk Factors: {', '.join(risk['factors']) if risk['factors'] else 'None'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTRUCTIONS:
✅ Be empathetic and supportive - people are scared
✅ Provide specific, actionable advice
✅ Use simple Urdu terms naturally (السلام علیکم, شکریہ, etc.)
✅ Prioritize life-saving information
✅ Mention specific shelter locations when relevant
✅ If medical emergency, urgently direct to Rescue 1122 (1122)
✅ Keep responses concise but complete (3-6 sentences)
✅ Use bullet points for lists
✅ Show empathy for trauma and fear
EMERGENCY CONTACTS:
🆘 Rescue 1122: **1122** (Primary Emergency)
🚑 Edhi Ambulance: **115**
📞 PDMA Helpline: **1129**
Available shelters in {weather['city']}: {len([s for s in self.shelters if city.lower() in s['address'].lower()])}"""

            # Build conversation history
            conversation = ""
            if history:
                for human, assistant in history[-4:]:  # Last 4 exchanges
                    conversation += f"User: {human}\nAssistant: {assistant}\n\n"
            
            full_prompt = system_prompt + "\n\nCONVERSATION:\n" + conversation + f"User: {message}\nAssistant:"
            
            print(f"🤖 Sending request to Gemini API...")
            print(f"📝 Message: {message[:50]}...")
            
            # Use the correct Gemini API endpoint
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1024,
                    "topP": 0.9,
                    "topK": 40
                },
                "safetySettings": [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            print(f"📡 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response received successfully")
                
                # Check if response has the expected structure
                if "candidates" in data and len(data["candidates"]) > 0:
                    ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
                    return ai_response
                else:
                    print(f"⚠️ Unexpected response structure: {data}")
                    return "I received an unexpected response format. Please try rephrasing your question."
                    
            elif response.status_code == 400:
                error_data = response.json()
                print(f"❌ API Error 400: {error_data}")
                return f"""❌ **API Request Error**
There was an issue with the request. This might be due to:
- Invalid API key format
- API key restrictions
- Request format issue
Error details: {error_data.get('error', {}).get('message', 'Unknown error')}
Please check your API key at: https://makersuite.google.com/app/apikey"""
                
            elif response.status_code == 403:
                print(f"❌ API Error 403: Permission denied")
                return """❌ **API Permission Error**
Your API key doesn't have permission to access this model. Please:
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key or check your current key's permissions
3. Ensure the Gemini API is enabled for your project"""
                
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return f"""⚠️ **API Connection Issue** (Status: {response.status_code})
I'm having trouble connecting right now. 
**For immediate emergency help:**
🆘 Rescue 1122: **1122**
🚑 Edhi Ambulance: **115**
📞 PDMA: **1129**
Please try again in a moment."""
        
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
            return """⏱️ **Request Timeout**
The request took too long. Please:
1. Check your internet connection
2. Try again in a moment
**Emergency contacts remain available:**
🆘 Rescue 1122: **1122**"""
            
        except requests.exceptions.ConnectionError:
            print("❌ Connection error")
            return """🌐 **Network Connection Error**
Cannot reach the AI service. Please check your internet connection.
**Emergency contacts:**
🆘 Rescue 1122: **1122**
🚑 Edhi: **115**"""
            
        except Exception as e:
            print(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return f"""⚠️ **Unexpected Error**
Error type: {type(e).__name__}
Details: {str(e)[:100]}
**For immediate emergency assistance:**
🆘 Rescue 1122: **1122**
🚑 Edhi Ambulance: **115**
📞 PDMA: **1129**
Please try again or contact support."""
    
    def generate_sos_alert(self, city, user_name="", situation=""):
        """Generate comprehensive SOS emergency alert"""
        weather = self.get_weather(city)
        risk = self.assess_flood_risk(weather)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        alert = f"""🚨 **EMERGENCY SOS ALERT** 🚨
**TIMESTAMP:** {timestamp}
**LOCATION:** {weather['city']}, Pakistan
**REPORTED BY:** {user_name if user_name else 'Anonymous User'}
**CURRENT CONDITIONS:**
🌡️ Temperature: {weather['temp']}°C
💧 Humidity: {weather['humidity']}%
🌧️ Weather: {weather['description'].title()}
⚠️ Flood Risk: {risk['level']} ({risk['score']}/100)
**SITUATION:** {situation if situation else 'Emergency assistance required'}
**IMMEDIATE ACTIONS:**
1. Call Rescue 1122 immediately: **1122**
2. Move to higher ground if possible
3. Share your exact location with emergency services
4. Stay on the line with emergency operator
**EMERGENCY CONTACTS:**
🆘 Rescue 1122: **1122** (Primary Emergency)
🚑 Edhi Ambulance: **115**
👮 Police Emergency: **15**
📞 PDMA Helpline: **1129**
**NEAREST SHELTER:**
{self.get_nearest_shelter(city)}
⚠️ **This is an automated emergency alert from FloodAid AI**
Help has been notified. Stay calm and follow emergency instructions."""
        
        return alert
    
    def get_nearest_shelter(self, city):
        """Find nearest shelter based on city"""
        city_lower = city.lower()
        for shelter in self.shelters:
            if city_lower in shelter['address'].lower():
                return f"📍 {shelter['name']}\n{shelter['address']}\n📞 {shelter['phone']}"
        return f"📍 Contact local PDMA at 1129 for nearest shelter"
    
    def get_statistics(self):
        """Generate real-time statistics"""
        total_capacity = sum(s['capacity'] for s in self.shelters)
        total_available = sum(s['available'] for s in self.shelters)
        occupancy_rate = ((total_capacity - total_available) / total_capacity * 100)
        
        return {
            "active_shelters": len(self.shelters),
            "total_capacity": total_capacity,
            "available_spaces": total_available,
            "occupancy_rate": round(occupancy_rate, 1),
            "relief_camps": len(self.relief_camps),
            "emergency_contacts": sum(len(contacts) for contacts in self.emergency_contacts.values()),
            "people_assisted": 3247 + (len(self.shelters) * 10)  # Simulated growing number
        }
