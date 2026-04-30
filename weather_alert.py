import requests
import os
from datetime import datetime

# 1. Credentials
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def check_weather():
    print("📡 Fetching full 48-hour forecast for Muzaffarpur...")
    # Coordinates for Muzaffarpur: 26.12°N, 85.39°E
    url = "https://api.open-meteo.com/v1/forecast?latitude=26.12&longitude=85.39&hourly=temperature_2m,precipitation_probability,wind_speed_10m&forecast_days=2"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        times = data['hourly']['time']
        temps = data['hourly']['temperature_2m']
        rain_probs = data['hourly']['precipitation_probability']
        wind_speeds = data['hourly']['wind_speed_10m']

        update_list = []

        # Loop through every single hour (no IF condition)
        for i in range(len(times)):
            raw_time = datetime.fromisoformat(times[i])
            clean_time = raw_time.strftime("%d %b, %H:%M")
            
            # Formatting: Time -> Temp | Rain% | Wind
            line = f"⏰ {clean_time}: {temps[i]}°C | 🌧️ {rain_probs[i]}% | 💨 {wind_speeds[i]}km/h"
            update_list.append(line)

        # Telegram has a character limit, so we will send the first 24 hours 
        # in the first message and the next 24 in the second to ensure you see everything.
        header = "📍 *Weather Update: Muzaffarpur (Next 48h)*\n\n"
        
        day1_msg = header + "📅 *Next 24 Hours:*\n" + "\n".join(update_list[:24])
        day2_msg = "📅 *Following 24 Hours:*\n" + "\n".join(update_list[24:])

        send_telegram(day1_msg)
        send_telegram(day2_msg)
        print("Success: Full 48-hour update sent to Muzaffarpur.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    check_weather()
