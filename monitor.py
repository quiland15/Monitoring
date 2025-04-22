import google.generativeai as genai
import datetime
import requests
import subprocess

# ✅ Konfigurasi API Gemini Flash
genai.configure(api_key="AIzaSyDtrfAYjWpExBmhlm1KHy29eMSWlVwSpLE")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ✅ Ambil 10 baris terakhir brute force log
def get_ssh_attempts():
    try:
        result = subprocess.check_output("grep 'Failed password' /var/log/auth.log | tail -n 10", shell=True)
        return result.decode()
    except subprocess.CalledProcessError:
        return "⚠️ Tidak ada data brute force ditemukan di log."

# ✅ Analisa dengan Gemini
def get_gemini_analysis(log_text):
    try:
        response = model.generate_content(
            f"Ada percobaan login brute force:\n{log_text}\nApa yang sebaiknya saya lakukan?"
        )
        return response.text
    except Exception as e:
        return f"⚠️ Gagal mendapatkan analisis dari Gemini: {e}"

# ✅ Kirim WhatsApp ke banyak device/token
def send_whatsapp_multi(message):
    devices = [
        {"token": "dfJ23QcRYVbSSa5sjnLJ", "target": "082192987104"},
        {"token": "pvNpLpP2Z9uDcGHwkrWa", "target": "085397303080"},
        # ➕ Tambahkan device/token lainnya di sini jika perlu
    ]

    for device in devices:
        payload = {
            "target": device["target"],
            "message": message,
        }
        headers = {
            "Authorization": device["token"]
        }

        try:
            r = requests.post("https://api.fonnte.com/send", data=payload, headers=headers)
            if r.status_code == 200:
                print(f"✅ Berhasil kirim ke {device['target']}")
            else:
                print(f"⚠️ Gagal kirim ke {device['target']} - Status: {r.status_code} - Response: {r.text}")
        except Exception as e:
            print(f"❌ Error kirim ke {device['target']}: {e}")

# ✅ Eksekusi utama
def main():
    log = get_ssh_attempts()
    ai_response = get_gemini_analysis(log)
    full_message = f"[{datetime.datetime.now()}] ⚠️ Percobaan Login Detected!\n\n{log}\n\n🧠 Gemini says:\n{ai_response}\n\n> _Sent via fonnte.com_"
    
    send_whatsapp_multi(full_message)

    # ➕ Simpan juga ke file log lokal (opsional)
    with open("/var/log/ssh_brute_force.log", "a") as f:
        f.write(full_message + "\n\n")

# ✅ Jalankan
if __name__ == "__main__":
    main()
