# runner_parallel.py
import json, subprocess, time, os, signal
from datetime import datetime

ANNOTATIONS_FILE = "annotations.csv"
SCHEDULE_FILE = "schedule.json"
POLL_SEC = 0.5  # frecuencia de chequeo

def now():
    return datetime.now()

def ts(dt=None):
    return (dt or now()).strftime("%Y-%m-%d %H:%M:%S")

def log_event(kind, when, extra):
    hdr_needed = not os.path.exists(ANNOTATIONS_FILE)
    with open(ANNOTATIONS_FILE, "a", encoding="utf-8") as f:
        if hdr_needed:
            f.write("timestamp,event,detail\n")
        f.write(f"{when},{kind},{extra}\n")

def main():
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    # normaliza y ordena
    for t in tasks:
        t["_start_dt"] = datetime.fromisoformat(t["start"])
        t["_end_dt"] = None
        t["_proc"] = None
    tasks.sort(key=lambda x: x["_start_dt"])

    i = 0
    running = []
    print("🚀 Runner paralelo iniciado. Controlando agenda y procesos…")

    while i < len(tasks) or running:
        now_dt = now()

        # lanzar todos los que “ya toca” (pueden ser varios a la misma hora)
        while i < len(tasks) and tasks[i]["_start_dt"] <= now_dt:
            t = tasks[i]
            cmd = t["cmd"]
            # En Windows, asegúrate de no usar '&' si buscas concurrencia; cada task es un proceso independiente.
            proc = subprocess.Popen(cmd, shell=True)
            t["_proc"] = proc
            t["_end_dt"] = now_dt + timedelta(seconds=t["duration_s"])
            running.append(t)
            log_event("start", ts(now_dt), f'{t["type"]} | PID={proc.pid} | {cmd}')
            print(f'▶️ {ts(now_dt)} START {t["type"]} (pid={proc.pid}) for {t["duration_s"]}s')
            i += 1

        # revisar cuáles deben terminar
        still_running = []
        for t in running:
            if now_dt >= t["_end_dt"]:
                try:
                    # pedir terminación amable
                    t["_proc"].terminate()
                    # si sigue vivo, matar
                    try:
                        t["_proc"].wait(timeout=3)
                    except Exception:
                        if os.name == "nt":
                            subprocess.call(f"taskkill /PID {t['_proc'].pid} /F /T", shell=True)
                        else:
                            os.kill(t["_proc"].pid, signal.SIGKILL)
                finally:
                    log_event("end", ts(now_dt), f'{t["type"]} | PID={t["_proc"].pid}')
                    print(f'✅ {ts(now_dt)} END   {t["type"]} (pid={t["_proc"].pid})')
            else:
                still_running.append(t)
        running = still_running

        time.sleep(POLL_SEC)

    print("🏁 Simulación completada. Anotaciones en annotations.csv")

if __name__ == "__main__":
    from datetime import timedelta
    main()
