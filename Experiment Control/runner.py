import json
import subprocess
import time
from datetime import datetime

ANNOTATIONS_FILE = "annotations.csv"

def log_event(event_type, start, end, cmd):
    with open(ANNOTATIONS_FILE, "a") as f:
        f.write(f"{start},{end},{event_type},{cmd}\n")

def run_scheduled_stressors(schedule_file="schedule.json"):
    with open(schedule_file, "r") as f:
        schedule = json.load(f)

    print("🚀 Runner iniciado. Esperando ejecuciones planificadas...")
    for task in schedule:
        start_ts = datetime.fromisoformat(task["start"])
        delay = (start_ts - datetime.now()).total_seconds()
        if delay > 0:
            print(f"⏳ Esperando {round(delay)}s para iniciar {task['type']}")
            time.sleep(delay)

        duration = task["duration_s"]
        cmd = task["cmd"]
        print(f"▶️ Ejecutando: {cmd} ({duration}s)")

        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        proc = subprocess.Popen(cmd, shell=True)
        time.sleep(duration)
        proc.terminate()
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_event(task["type"], start_time, end_time, cmd)
        print(f"✅ Finalizado: {task['type']} ({duration}s)\n")

    print("🏁 Simulación completa. Anotaciones guardadas en annotations.csv")

if __name__ == "__main__":
    run_scheduled_stressors()
