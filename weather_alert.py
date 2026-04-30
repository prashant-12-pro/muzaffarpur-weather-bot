import requests
import os
from datetime import datetime

# 1. Credentials
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def check_weather():
    # Muzaffarpur Coordinates (26.12, 85.39)
    # Fetching 2 days (48 hours) of data
    url = "https://api.open-meteo.com/v1/forecast?latitude=26.12&longitude=85.39&hourly=precipitation_probability,wind_speed_10m&forecast_days=2"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        times = data['hourly']['time']
        rain_probs = data['hourly']['precipitation_probability']
        wind_speeds = data['hourly']['wind_speed_10m']

        alert_list = []

        # Loop through all 48 hours
        for i in range(len(times)):
            rain = rain_probs[i]
            wind = wind_speeds[i]
            
            # Check your new thresholds: Rain > 50% OR Wind > 13 km/h
            if rain > 50 or wind > 13:
                # Format time: "2026-04-30T14:00" -> "30 Apr, 14:00"
                raw_time = datetime.fromisoformat(times[i])
                clean_time = raw_time.strftime("%d %b, %H:%M")
                
                alert_list.append(f"⏰ {clean_time} -> 🌧️ {rain}% | 💨 {wind}km/h")

        if alert_list:
            # Create a header and join all hourly alerts
            header = "⚠️ *Weather Alert (Next 48h):*\n\n"
            full_message = header + "\n".join(alert_list)
            
            # Telegram has a 4096 character limit; if the list is too long, we'll send the first 15 alerts
            if len(full_message) > 4000:
                full_message = header + "\n".join(alert_list[:15]) + "\n...and more."
                
            send_telegram(full_message)
            print(f"Alert sent with {len(alert_list)} hours of data.")
        else:
            print("No alerts found for the next 48 hours.")
            
    except Exception as e:
        print(f"Error: {e}")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": text,
        "parse_mode": "Markdown" # This makes the header bold
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    check_weather()
