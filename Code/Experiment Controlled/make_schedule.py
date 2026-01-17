# make_schedule.py
import json, random
from datetime import datetime, timedelta

START_ISO = "2025-10-11T02:30:00"
TOTAL_HOURS = 18
TARGET_EVENTS = 66  # ajusta a 50–80 si quieres

def mk_cpu(duration):
    procs = random.choice([4,6,8,10])
    return {
        "type":"cpu_spike",
        "duration_s": duration,
        "cmd": f"python stressors\\cpu_stress.py --procs {procs} --duration {duration}"
    }

def mk_mem(duration):
    step = random.choice([300,400,500,600])
    steps = max(3, min(12, duration // random.choice([20,30,40])))
    sleep = max(3, min(10, duration // max(steps,1)))
    return {
        "type":"memory_load",
        "duration_s": duration,
        "cmd": f"python stressors\\mem_stress.py --step_mb {step} --steps {steps} --sleep {sleep}"
    }

def mk_disk(duration):
    size_mb = random.choice([600,800,1000,1500,2000])
    block = random.choice([5,10,20])
    # mantener al menos size/duración ~ sostenido
    return {
        "type":"disk_io",
        "duration_s": duration,
        "cmd": f"python stressors\\disk_stress.py --size_mb {size_mb} --block_mb {block}"
    }

def pick_event(duration):
    kind = random.choices(
        ["cpu","mem","disk"],
        weights=[0.4,0.3,0.3],
        k=1
    )[0]
    if kind=="cpu": return mk_cpu(duration)
    if kind=="mem": return mk_mem(duration)
    return mk_disk(duration)

def main():
    random.seed(42)
    start = datetime.fromisoformat(START_ISO)
    end   = start + timedelta(hours=TOTAL_HOURS)

    # estrategia: ir proponiendo slots con gaps pequeños y duraciones variadas; forzar solapes en ~40%
    t = start
    events = []
    while t < end and len(events) < TARGET_EVENTS:
        # duración base del evento (5–20 min; algún pico corto 3 min)
        duration = random.choice([180,300,600,900,1200])
        evt = pick_event(duration)
        evt["start"] = t.isoformat(timespec="seconds")
        events.append(evt)

        # decidir gap antes del siguiente evento (0–30 min)
        gap = random.choice([0,60,120,180,300,600,900,1200,1800])
        # 40% prob de solape: gap menor al 60% de duración
        if random.random() < 0.4:
            gap = max(0, int(duration * random.uniform(0.1, 0.6)))
        t = t + timedelta(seconds=gap)

        # ocasional evento “mix”: crear segunda tarea con mismo start para solapar explícito
        if random.random() < 0.25:
            duration2 = random.choice([300,600,900])
            evt2 = pick_event(duration2)
            evt2["start"] = evt["start"]  # mismo inicio
            events.append(evt2)

    # clamp al final de ventana
    events = [e for e in events if datetime.fromisoformat(e["start"]) < end]

    # ordenar por start
    events.sort(key=lambda x: x["start"])

    with open("schedule.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)
    print(f"✅ schedule.json generado con {len(events)} eventos entre {start} y {end}")

if __name__ == "__main__":
    main()
