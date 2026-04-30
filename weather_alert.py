import requests
import os

# Credentials from GitHub Secrets
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def check_weather():
    # Fetch data for Muzaffarpur (26.12, 85.39)
    url = "https://api.open-meteo.com/v1/forecast?latitude=26.12&longitude=85.39&hourly=precipitation_probability,wind_speed_10m&forecast_days=1"
    
    try:
        data = requests.get(url).json()
        # Current hour is index 0
        rain_chance = data['hourly']['precipitation_probability'][0]
        wind_speed = data['hourly']['wind_speed_10m'][0]

        message = ""
        if rain_chance >= 70:
            message = f"🌧️ Weather Alert: {rain_chance}% chance of rain in Muzaffarpur!"
        elif wind_speed > 13:
            message = f"💨 Wind Alert: Speed is {wind_speed} km/h. Watch out!"

        if message:
            send_telegram(message)
            
    except Exception as e:
        print(f"Error: {e}")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    check_weather()
