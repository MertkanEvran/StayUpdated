import subprocess
import time
import os
import signal

def start_ollama():
    print("🧠 Ollama başlatılıyor...")
    # Ollama process'i arka planda başlatılır
    process = subprocess.Popen(["ollama", "run", "gemma3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)  # Modelin ayağa kalkması için bekleme süresi
    return process


def run_command(command, wait=True):
    project_dir = os.getenv("PROJECT_DIR")
    print(f"▶️ Komut çalıştırılıyor: {' '.join(command)}")
    result = subprocess.run(command, cwd=project_dir)
    if result.returncode != 0:
        print("❌ Komut başarısız:", ' '.join(command))
        exit(1)

def main():
    ollama_proc = start_ollama()

    try:
        run_command(["docker", "compose", "up", "-d", "mongo"])
        run_command(["docker", "compose", "run", "--rm", "scraper"])
        run_command(["docker", "compose", "run", "--rm", "llm_client"])
        run_command(["docker", "compose", "run", "--rm", "mailer"])
        print("✅ Tüm işlemler tamamlandı.")
    finally:
        print("🧹 Ollama process'i sonlandırılıyor...")
        # Ollama terminalde sonsuza kadar açık kalır, manuel kapatmamız gerek
        ollama_proc.send_signal(signal.SIGTERM)
        ollama_proc.wait()
        print("🛑 Ollama durduruldu.")


        run_command(["docker", "compose", "stop", "mongo"], wait=False)
        print("🛑 MongoDB durduruldu.")

if __name__ == "__main__":
    main()
