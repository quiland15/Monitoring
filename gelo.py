import google.generativeai as genai
import datetime
import requests
import subprocess
import schedule
import time

# Konfigurasi API Gemini
genai.configure(api_key="AIzaSyDtrfAYjWpExBmhlm1KHy29eMSWlVwSpLE")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_ssh_attempts():
    result = subprocess.check_output("grep 'Failed password' /var/log/auth.log | tail -n 10", shell=True)
    return result.decode()

def get_gemini_analysis(log_text):
    try:
        response = model.generate_content(f"Ada percobaan login brute force:\n{log_text}\nApa yang sebaiknya saya lakukan?.responnya jangan terlalu panjang")
        return response.text
    except Exception as e:
        return f"⚠️ Gagal mendapatkan analisis dari Gemini: {e}"

def send_whatsapp(message):
    token = "RZoMxPyb1m8gadg2C9cG"
    payload = {
        "target": "085397303080",
        "message": message,
    }
    headers = {"Authorization": token}
    r = requests.post("https://api.fonnte.com/send", data=payload, headers=headers)
    return r.status_code

# Fungsi kirim ucapan cinta
def send_morning_greeting():
    send_whatsapp("🌅 Selamat pagi sayang, semoga harimu indah ❤️")

def send_afternoon_greeting():
    send_whatsapp("🌞 Selamat siang sayang, jangan lupa makan ya 😘")

def send_night_greeting():
    send_whatsapp("🌙 Selamat malam sayang, mimpi indah dan tidur nyenyak ya 💕")

# Fungsi keamanan (opsional)
def run_security_check():
    log = get_ssh_attempts()
    ai_response = get_gemini_analysis(log)
    full_message = f"[{datetime.datetime.now()}] ⚠️ Percobaan Login Detected!\n\n{log}\n\n🧠 Gemini says:\n{ai_response}"
    send_whatsapp(full_message)

# Jadwal ucapan harian
schedule.every().day.at("06:30").do(send_morning_greeting)
schedule.every().day.at("11:30").do(send_afternoon_greeting)
schedule.every().day.at("21:00").do(send_night_greeting)

# Jadwal pengecekan keamanan (opsional)
# schedule.every(1).hours.do(run_security_check)

# Loop untuk terus jalanin jadwal
while True:
    schedule.run_pending()
    time.sleep(30)
