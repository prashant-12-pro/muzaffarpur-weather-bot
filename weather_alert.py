import requests
import os
from datetime import datetime

# Credentials
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def check_weather():
    print("Fetching weather data for Muzaffarpur...")
    url = "https://api.open-meteo.com/v1/forecast?latitude=26.12&longitude=85.39&hourly=precipitation_probability,wind_speed_10m&forecast_days=2"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        times = data['hourly']['time']
        rain_probs = data['hourly']['precipitation_probability']
        wind_speeds = data['hourly']['wind_speed_10m']

        alert_list = []

        for i in range(len(times)):
            rain = rain_probs[i]
            wind = wind_speeds[i]
            
            if rain > 50 or wind > 13:
                raw_time = datetime.fromisoformat(times[i])
                clean_time = raw_time.strftime("%d %b, %H:%M")
                alert_list.append(f"⏰ {clean_time} -> 🌧️ {rain}% | 💨 {wind}km/h")

        if alert_list:
            header = "⚠️ *Weather Alert (Next 48h):*\n\n"
            full_message = header + "\n".join(alert_list[:15]) # Send first 15 alerts
            send_telegram(full_message)
            print(f"Success! Alert sent to Telegram with {len(alert_list)} data points.")
        else:
            print("No alerts found for the next 48 hours.")
            
    except Exception as e:
        print(f"Error occurred: {e}")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    r = requests.post(url, json=payload)
    print(f"Telegram API response: {r.status_code}")

# --- CRITICAL: THE SCRIPT RUNS HERE ---
if __name__ == "__main__":
    check_weather()
