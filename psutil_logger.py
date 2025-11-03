import psutil
import csv
import time
import os
from datetime import datetime

# === CONFIGURACIÓN ===
OUTPUT_FILE = "system_metrics_dataset.csv"
INTERVAL = 1  # segundos entre muestras
DURATION = 60 * 60 * 18 # segundos totales (10 minutos)

FIELDS = [
    "timestamp",
    "cpu_percent",
    "cpu_count_logical",
    "cpu_count_physical",
    "ram_total_GB",
    "ram_used_percent",
    "ram_available_GB",
    "swap_used_percent",
    "disk_total_GB",
    "disk_used_percent",
    "disk_read_MB",
    "disk_write_MB",
    "net_sent_MB",
    "net_recv_MB",
    "battery_percent",
    "battery_plugged",
    "process_count",
]

# === SOLO ESCRIBIR CABECERA SI EL ARCHIVO NO EXISTE ===
file_exists = os.path.exists(OUTPUT_FILE)
if not file_exists:
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS)
    print(f"🆕 Archivo creado: {OUTPUT_FILE}")
else:
    print(f"📂 Archivo existente detectado: se agregarán nuevos datos...")

# === VARIABLES DE REFERENCIA PARA CÁLCULOS DE I/O ===
prev_disk = psutil.disk_io_counters()
prev_net = psutil.net_io_counters()

print(f"Iniciando registro cada {INTERVAL}s durante {DURATION//60} minutos...")
start_time = time.time()

while (time.time() - start_time) < DURATION:
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # CPU
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)

        # RAM
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Disco
        disk = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        disk_read_MB = (disk_io.read_bytes - prev_disk.read_bytes) / (1024 ** 2)
        disk_write_MB = (disk_io.write_bytes - prev_disk.write_bytes) / (1024 ** 2)
        prev_disk = disk_io

        # Red
        net = psutil.net_io_counters()
        net_sent_MB = (net.bytes_sent - prev_net.bytes_sent) / (1024 ** 2)
        net_recv_MB = (net.bytes_recv - prev_net.bytes_recv) / (1024 ** 2)
        prev_net = net

        # Batería
        try:
            battery = psutil.sensors_battery()
            battery_percent = battery.percent if battery else None
            battery_plugged = battery.power_plugged if battery else None
        except Exception:
            battery_percent = None
            battery_plugged = None

        # Número de procesos
        process_count = len(psutil.pids())

        # Registro final
        row = [
            timestamp,
            cpu_percent,
            cpu_count_logical,
            cpu_count_physical,
            round(ram.total / (1024 ** 3), 2),
            ram.percent,
            round(ram.available / (1024 ** 3), 2),
            swap.percent,
            round(disk.total / (1024 ** 3), 2),
            disk.percent,
            round(disk_read_MB, 3),
            round(disk_write_MB, 3),
            round(net_sent_MB, 3),
            round(net_recv_MB, 3),
            battery_percent,
            battery_plugged,
            process_count,
        ]

        # Guardar en modo "append"
        with open(OUTPUT_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        print(f"[{timestamp}] CPU={cpu_percent}%  RAM={ram.percent}%  DISK={disk.percent}%  PROCESOS={process_count}")

        time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\n⛔ Registro detenido por el usuario.")
        break
    except Exception as e:
        print(f"⚠️ Error: {e}")
        time.sleep(INTERVAL)

print(f"\n✅ Datos agregados en '{OUTPUT_FILE}'")
# === FIN DEL PROGRAMA ===