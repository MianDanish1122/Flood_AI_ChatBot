import gradio as gr
from backend import FloodAidBackend

# Initialize backend
backend = FloodAidBackend()

# Custom CSS for beautiful design
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.feature-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin: 10px 0;
    transition: transform 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.2);
}

.stat-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 15px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 5px;
}

.emergency-btn {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    color: white !important;
    font-weight: bold !important;
    font-size: 18px !important;
    padding: 15px 30px !important;
    border: none !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4) !important;
}

.weather-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.risk-critical {
    background: linear-gradient(135deg, #f5576c 0%, #ff6b6b 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
    animation: pulse 2s infinite;
}

.risk-high {
    background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
}

.risk-moderate {
    background: linear-gradient(135deg, #f5af19 0%, #f12711 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
}

.risk-low {
    background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.contact-item {
    background: #f8f9fa;
    padding: 15px;
    border-left: 4px solid #667eea;
    margin: 10px 0;
    border-radius: 8px;
}

.shelter-card {
    background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
    padding: 20px;
    border-radius: 12px;
    margin: 10px 0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.priority-critical {
    background: #ff6b6b;
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.priority-high {
    background: #ffa502;
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.priority-medium {
    background: #ffd93d;
    color: #333;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}
"""

def create_weather_display(city):
    """Create beautiful weather display"""
    weather = backend.get_weather(city)
    risk = backend.assess_flood_risk(weather)
    
    risk_class = f"risk-{risk['color']}"
    
    html = f"""
    <div class="weather-card">
        <h2>🌦️ {weather['city']}, Pakistan</h2>
        <div style="display: flex; justify-content: space-between; margin-top: 20px;">
            <div>
                <h1 style="margin: 0; font-size: 48px;">{weather['temp']}°C</h1>
                <p style="margin: 5px 0;">Feels like {weather['feels_like']}°C</p>
                <p style="text-transform: capitalize; font-size: 18px;">{weather['description']}</p>
            </div>
            <div style="text-align: right;">
                <p>💧 Humidity: {weather['humidity']}%</p>
                <p>💨 Wind: {weather['wind_speed']} m/s</p>
                <p>☁️ Clouds: {weather['clouds']}%</p>
                <p>👁️ Visibility: {weather['visibility']} km</p>
            </div>
        </div>
    </div>
    <br>
    <div class="{risk_class}">
        <h3 style="margin: 0;">⚠️ FLOOD RISK: {risk['level'].upper()}</h3>
        <p style="margin: 10px 0;">Risk Score: {risk['score']}/100</p>
        <p style="margin: 5px 0; font-size: 14px;">{', '.join(risk['factors']) if risk['factors'] else 'No immediate risk factors'}</p>
    </div>
    """
    return html

def create_shelter_display():
    """Create beautiful shelter cards"""
    html = "<h2>🏠 Emergency Shelters</h2>"
    for shelter in backend.shelters[:5]:  # Show first 5
        available_pct = (shelter['available'] / shelter['capacity']) * 100
        status_color = "#27ae60" if available_pct > 30 else "#e67e22" if available_pct > 10 else "#e74c3c"
        
        html += f"""
        <div class="shelter-card">
            <h3 style="margin: 0 0 10px 0;">{shelter['name']}</h3>
            <p style="margin: 5px 0;">📍 {shelter['address']}</p>
            <p style="margin: 5px 0;">📞 {shelter['phone']}</p>
            <div style="display: flex; gap: 10px; margin-top: 15px;">
                <div style="flex: 1; background: white; padding: 10px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; font-size: 24px; font-weight: bold; color: #667eea;">{shelter['capacity']}</p>
                    <p style="margin: 5px 0; font-size: 12px;">Total Capacity</p>
                </div>
                <div style="flex: 1; background: white; padding: 10px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; font-size: 24px; font-weight: bold; color: {status_color};">{shelter['available']}</p>
                    <p style="margin: 5px 0; font-size: 12px;">Available Now</p>
                </div>
            </div>
            <p style="margin: 10px 0 0 0; font-size: 14px;">🏥 Facilities: {', '.join(shelter['facilities'])}</p>
        </div>
        """
    return html

def create_contacts_display():
    """Create categorized emergency contacts"""
    html = "<h2>📞 Emergency Contacts</h2>"
    
    for category, contacts in backend.emergency_contacts.items():
        html += f"<h3 style='color: #667eea; margin-top: 20px;'>{category}</h3>"
        for contact in contacts:
            html += f"""
            <div class="contact-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0;">{contact['name']}</h4>
                        <p style="margin: 5px 0; font-size: 12px; color: #666;">Available: {contact['available']}</p>
                    </div>
                    <a href="tel:{contact['number']}" style="background: #667eea; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 18px;">{contact['number']}</a>
                </div>
            </div>
            """
    return html

def create_medical_display():
    """Create medical tips display"""
    html = "<h2>⚕️ Medical Assistance & Health Tips</h2>"
    
    for tip in backend.medical_tips:
        priority_class = f"priority-{tip['priority'].lower()}"
        html += f"""
        <div class="feature-card">
            <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 10px;">
                <h3 style="margin: 0; flex: 1;">{tip['title']}</h3>
                <span class="{priority_class}">{tip['priority']}</span>
            </div>
            <p style="margin: 10px 0; color: #555;">{tip['desc']}</p>
        </div>
        """
    
    html += """
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
        <h3>🚑 Emergency Medical Hotlines</h3>
        <p style="font-size: 18px; margin: 10px 0;">
            <strong>Rescue 1122:</strong> <a href="tel:1122" style="color: white;">1122</a><br>
            <strong>Edhi Ambulance:</strong> <a href="tel:115" style="color: white;">115</a><br>
            <strong>Red Crescent:</strong> <a href="tel:051-9250404" style="color: white;">051-9250404</a>
        </p>
    </div>
    """
    return html

def create_relief_display():
    """Create relief camps and donation needs display"""
    html = "<h2>📦 Relief Camps & Supply Distribution</h2>"
    
    for camp in backend.relief_camps:
        html += f"""
        <div class="feature-card">
            <h3 style="margin: 0 0 10px 0; color: #667eea;">🏕️ {camp['name']}</h3>
            <p style="margin: 5px 0;">📍 <strong>City:</strong> {camp['city']}</p>
            <p style="margin: 5px 0;">🎁 <strong>Available Supplies:</strong> {', '.join(camp['supplies'])}</p>
            <p style="margin: 5px 0;">📞 <strong>Contact:</strong> <a href="tel:{camp['contact']}">{camp['contact']}</a></p>
            <p style="margin: 5px 0;">🕐 <strong>Hours:</strong> {camp['open']}</p>
        </div>
        """
    
    html += "<h2 style='margin-top: 30px;'>👐 Urgent Donation Needs</h2>"
    html += "<p>Help us provide essential supplies to flood victims. These items are critically needed:</p>"
    
    for item in backend.donation_needs:
        priority_class = f"priority-{item['priority'].lower()}"
        html += f"""
        <div class="feature-card" style="border-left: 4px solid {'#ff6b6b' if item['priority'] == 'Critical' else '#ffa502' if item['priority'] == 'High' else '#ffd93d'};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 5px 0;">{item['item']}</h4>
                    <p style="margin: 5px 0; color: #666;">Quantity Needed: <strong>{item['quantity']}</strong></p>
                    <p style="margin: 5px 0; color: #666;">Urgency: <strong>{item['urgency']}</strong></p>
                </div>
                <span class="{priority_class}">{item['priority']}</span>
            </div>
        </div>
        """
    return html

def create_safety_display():
    """Create safety guidelines display"""
    html = "<h2>🛡️ Safety Guidelines & Flood Preparedness</h2>"
    
    for phase, tips in backend.safety_tips.items():
        color = "#667eea" if phase == "Before Flood" else "#ffa502" if phase == "During Flood" else "#27ae60"
        html += f"""
        <div style="background: {color}; color: white; padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="margin: 0 0 15px 0;">⚠️ {phase}</h3>
            <ul style="margin: 0; padding-left: 20px;">
        """
        for tip in tips:
            html += f"<li style='margin: 8px 0;'>{tip}</li>"
        html += "</ul></div>"
    
    return html

def create_statistics_display():
    """Create live statistics dashboard"""
    stats = backend.get_statistics()
    
    html = """
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
        <div class="stat-box">
            <h2 style="margin: 0; font-size: 36px;">{}</h2>
            <p style="margin: 5px 0;">Active Shelters</p>
        </div>
        <div class="stat-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h2 style="margin: 0; font-size: 36px;">{}</h2>
            <p style="margin: 5px 0;">Available Spaces</p>
        </div>
        <div class="stat-box" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <h2 style="margin: 0; font-size: 36px;">{}</h2>
            <p style="margin: 5px 0;">Relief Camps</p>
        </div>
        <div class="stat-box" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <h2 style="margin: 0; font-size: 36px;">{}</h2>
            <p style="margin: 5px 0;">People Assisted</p>
        </div>
    </div>
    """.format(stats['active_shelters'], stats['available_spaces'], stats['relief_camps'], stats['people_assisted'])
    
    return html

# Main Gradio Interface - Compatible with older Gradio versions
with gr.Blocks(title="FloodAid AI") as app:
    # Add CSS using gr.HTML at the top
    gr.HTML(f"<style>{custom_css}</style>")
    
    # Header
    gr.HTML("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 48px;">🌊 FloodAid AI</h1>
        <p style="margin: 10px 0 0 0; font-size: 20px; opacity: 0.9;">Real-Time Flood Relief & Disaster Management System</p>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">Powered by Gemini 2.5 Flash AI • OpenWeather API • 24/7 Emergency Support</p>
    </div>
    """)
    
    # Statistics Dashboard
    stats_display = gr.HTML(create_statistics_display())
    
    with gr.Row():
        # Left Column - Main Chat
        with gr.Column(scale=3):
            with gr.Tabs() as tabs:
                # AI Chat Tab
                with gr.Tab("💬 AI Assistant"):
                    gr.Markdown("""
                    ### Ask me anything about:
                    - 🏠 Emergency shelter locations
                    - ⚕️ Medical assistance and first aid
                    - 🚨 Evacuation procedures
                    - 💧 Water and food safety
                    - 📦 Relief supplies and donations
                    - 🛡️ Flood safety guidelines
                    """)
                    
                    city_input = gr.Textbox(
                        label="📍 Your Current City",
                        value="Lahore",
                        placeholder="Enter your city (e.g., Lahore, Karachi, Islamabad, Multan, Faisalabad)"
                    )
                    
                    chatbot = gr.Chatbot(
                        label="FloodAid AI Assistant"
                    )
                    
                    with gr.Row():
                        msg = gr.Textbox(
                            label="Your Message",
                            placeholder="Type your question here... (e.g., 'I need emergency shelter', 'How to purify flood water?')",
                            lines=2
                        )
                    
                    with gr.Row():
                        submit_btn = gr.Button("📤 Send Message", variant="primary")
                        clear_btn = gr.Button("🗑️ Clear Chat")
                        sos_btn = gr.Button("🚨 SEND SOS ALERT", variant="stop")
                    
                    gr.Markdown("""
                    ---
                    **💡 Quick Questions You Can Ask:**
                    - "Where is the nearest emergency shelter?"
                    - "How can I purify flood water for drinking?"
                    - "What should I do if someone is injured?"
                    - "Where can I get food and supplies?"
                    - "How to evacuate safely during floods?"
                    - "What medical supplies do I need?"
                    """)
                
                # Shelters Tab
                with gr.Tab("🏠 Emergency Shelters"):
                    shelters_html = gr.HTML(create_shelter_display())
                    refresh_shelters_btn = gr.Button("🔄 Refresh Shelter Information")
                
                # Medical Tab
                with gr.Tab("⚕️ Medical Assistance"):
                    medical_html = gr.HTML(create_medical_display())
                    
                # Relief Tab
                with gr.Tab("📦 Relief & Donations"):
                    relief_html = gr.HTML(create_relief_display())
                
                # Safety Tab
                with gr.Tab("🛡️ Safety Guidelines"):
                    safety_html = gr.HTML(create_safety_display())
                
                # Emergency Contacts Tab
                with gr.Tab("📞 Emergency Contacts"):
                    contacts_html = gr.HTML(create_contacts_display())
        
        # Right Column - Weather & Alerts
        with gr.Column(scale=2):
            gr.Markdown("### 🌦️ Live Weather & Alerts")
            
            weather_city = gr.Textbox(
                label="Check Weather For",
                value="Lahore",
                placeholder="Enter city name"
            )
            
            weather_html = gr.HTML(create_weather_display("Lahore"))
            
            weather_refresh_btn = gr.Button("🔄 Update Weather")
            
            gr.Markdown("---")
            gr.Markdown("### 📊 Real-Time Updates")
            
            gr.HTML("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                <h3 style="margin: 0 0 10px 0;">⚠️ Active Flood Alerts</h3>
                <p style="margin: 5px 0;">🔴 <strong>Heavy Rainfall Warning</strong></p>
                <p style="margin: 5px 0; font-size: 14px;">Expected in next 24-48 hours across Punjab and Sindh regions</p>
                <p style="margin: 15px 0 5px 0;">🟡 <strong>Flood Risk Areas</strong></p>
                <ul style="margin: 5px 0; font-size: 14px; padding-left: 20px;">
                    <li>Low-lying regions near rivers</li>
                    <li>Old city areas with poor drainage</li>
                    <li>Agricultural lands in flood plains</li>
                </ul>
                <p style="margin: 15px 0 5px 0; font-weight: bold;">⚠️ Stay alert and prepared!</p>
            </div>
            """)
            
            gr.HTML("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                <h3 style="margin: 0 0 10px 0;">📻 Latest Updates</h3>
                <p style="margin: 8px 0; font-size: 14px;">✅ 5 new relief camps opened in Lahore</p>
                <p style="margin: 8px 0; font-size: 14px;">✅ Medical teams dispatched to flood zones</p>
                <p style="margin: 8px 0; font-size: 14px;">✅ Water purification units now active</p>
                <p style="margin: 8px 0; font-size: 14px;">✅ Emergency supplies arriving daily</p>
                <p style="margin: 8px 0; font-size: 14px;">✅ 24/7 helplines operational</p>
            </div>
            """)
            
            gr.HTML("""
            <div style="background: #27ae60; color: white; padding: 15px; border-radius: 10px; margin: 10px 0; text-align: center;">
                <h4 style="margin: 0 0 10px 0;">🆘 Emergency Hotline</h4>
                <a href="tel:1122" style="color: white; text-decoration: none; font-size: 32px; font-weight: bold;">1122</a>
                <p style="margin: 10px 0 0 0; font-size: 14px;">Available 24/7</p>
            </div>
            """)
    
    # Event Handlers
    def respond(message, chat_history, city):
        if not message.strip():
            return chat_history, ""
        
        # Convert chat_history to the format backend expects (list of tuples)
        history_tuples = []
        if chat_history:
            for msg in chat_history:
                if isinstance(msg, dict):
                    # New format: dict with 'role' and 'content'
                    if msg.get('role') == 'user':
                        user_msg = msg.get('content', '')
                        history_tuples.append((user_msg, ''))
                    elif msg.get('role') == 'assistant' and history_tuples:
                        history_tuples[-1] = (history_tuples[-1][0], msg.get('content', ''))
                elif isinstance(msg, tuple):
                    # Old format: tuple
                    history_tuples.append(msg)
        
        bot_response = backend.chat_with_gemini(message, history_tuples, city)
        
        # Return in new dict format
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_response})
        return chat_history, ""
    
    def send_sos(city):
        sos_message = backend.generate_sos_alert(city)
        return [
            {"role": "user", "content": sos_message},
            {"role": "assistant", "content": "🚨 **SOS ALERT PREPARED!**\n\nPlease call emergency services immediately:\n\n🆘 **Rescue 1122: 1122**\n🚑 **Edhi: 115**\n📞 **PDMA: 1129**\n\nStay calm and follow emergency instructions. Help is on the way!"}
        ]
    
    # Button Actions
    submit_btn.click(
        respond,
        inputs=[msg, chatbot, city_input],
        outputs=[chatbot, msg]
    )
    
    msg.submit(
        respond,
        inputs=[msg, chatbot, city_input],
        outputs=[chatbot, msg]
    )
    
    sos_btn.click(
        send_sos,
        inputs=[city_input],
        outputs=[chatbot]
    )
    
    clear_btn.click(
        lambda: None,
        None,
        chatbot,
        queue=False
    )
    
    weather_refresh_btn.click(
        create_weather_display,
        inputs=[weather_city],
        outputs=[weather_html]
    )
    
    city_input.change(
        create_weather_display,
        inputs=[city_input],
        outputs=[weather_html]
    )
    
    refresh_shelters_btn.click(
        lambda: create_shelter_display(),
        outputs=[shelters_html]
    )
    
    # Initial welcome message
    app.load(
        lambda: [
            {"role": "assistant", "content": """🌊 **السلام علیکم! Welcome to FloodAid AI!** 🤖

I'm your intelligent disaster relief assistant, powered by advanced AI technology. I'm here to help you 24/7 with:

✅ **Emergency Shelter Locations** - Find safe places immediately
✅ **Medical Assistance** - First aid tips and emergency care
✅ **Real-Time Weather Updates** - Stay informed about conditions
✅ **Relief Supplies** - Locate food, water, and essential items
✅ **Safety Guidelines** - Learn how to stay safe during floods
✅ **SOS Emergency Alerts** - Get help fast when you need it

**How can I assist you today?** 

Type your question or click the 🚨 SOS button if you need immediate emergency help!

*Stay safe, stay informed. We're here for you.* 💙"""}
        ],
        outputs=[chatbot]
    )

# Launch the application
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )
