# 🖥️ Server Digital Twin

A lightweight **Digital Twin** designed to **simulate workloads** (CPU, memory, disk) and **record real system telemetry** (CPU%, RAM%, I/O, network, processes, etc.) into a reproducible dataset.

---

## 📂 Project Structure

```
Data/
  ├─ psutil_logger.py
  └─ system_metrics_dataset.csv
Experiment Control/
  ├─ stressors/
  │   ├─ cpu_stress.py
  │   ├─ disk_stress.py
  │   └─ mem_stress.py
  ├─ annotations.csv
  ├─ basic.py
  ├─ make_schedule.py
  ├─ runner_parallel.py
  ├─ runner.py
  └─ schedule.json
System_Metrics_Analysis.ipynb
Project Definition – Server Digital Twin.pdf
.gitattributes
```

---

## ⚙️ Requirements

- **Python 3.9+**
- **Package:** `psutil`

Quick install:
```bash
# (Optional) create virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install psutil
```

---

## 🧩 Step 0 — Quick System Check (`basic.py`)

Before running the full project, verify that `psutil` works correctly on your OS:

```bash
cd "Experiment Control"
python basic.py
```

You should see console output with **CPU usage**, **RAM**, **disk usage**, and **network bytes**.  
If this works, your environment is correctly set up.

---

## 🛰️ System Telemetry Logger — `psutil_logger.py`

Location: `Data/psutil_logger.py`  
This script acts as the **system sensor**, collecting metrics every `INTERVAL` seconds for `DURATION` time and saving them to `Data/system_metrics_dataset.csv`.

Configure it inside the file (example: 10 minutes):
```python
INTERVAL = 1
DURATION = 60 * 10
```

Run:
```bash
cd Data
python psutil_logger.py
```

> You can run it **alone** (while a real app runs on the server) or **in parallel** with the stressors to create controlled experiments.

---

## 🗓️ Generate Experiment Schedule — `make_schedule.py`

Location: `Experiment Control/make_schedule.py`  
Generates or updates `schedule.json` with a list of stress events (CPU, memory, disk) and their start times.

```bash
cd "Experiment Control"
python make_schedule.py
```

> **Note:** On Windows, JSON paths may use `\\`; on Linux/macOS use `/`.

---

## ▶️ Experiment Runners

### Sequential — `runner.py`
Runs all events **in series**:
```bash
cd "Experiment Control"
python runner.py
```
Records experiment logs into `annotations.csv`.

### Parallel — `runner_parallel.py`
Runs multiple stressors **simultaneously** (e.g., CPU + disk + memory):
```bash
cd "Experiment Control"
python runner_parallel.py
```

---

## 💥 Stressor Scripts

Location: `Experiment Control/stressors/`  
> ⚠️ These scripts generate **real system load** — do not use on production servers.

**CPU Stress**
```bash
python stressors/cpu_stress.py --procs 8 --duration 180
```

**Memory Stress**
```bash
python stressors/mem_stress.py --step_mb 500 --steps 10 --sleep 10
```

**Disk Stress**
```bash
python stressors/disk_stress.py --size_mb 1500 --block_mb 10 --path stress_file.bin --sleep 0.5

# Clean up the generated file:
# Windows:
del stress_file.bin
# macOS/Linux:
rm stress_file.bin
```

---

## 🔄 Typical Workflows

### A) Monitor a Real Server
1. `python Experiment Control/basic.py`  
2. `python Data/psutil_logger.py`  
3. Analyze results in `Data/system_metrics_dataset.csv`  
   (see `System_Metrics_Analysis.ipynb` for example analysis).

### B) Run a Controlled Digital Twin Experiment
1. `python Experiment Control/make_schedule.py`
2. In Terminal 1 → `python Data/psutil_logger.py`
3. In Terminal 2 → `python Experiment Control/runner_parallel.py` (or `runner.py`)
4. Analyze:
   - `Data/system_metrics_dataset.csv` → system metrics
   - `Experiment Control/annotations.csv` → event logs

---

## 📊 Data Outputs

| File | Description |
|------|--------------|
| **`Data/system_metrics_dataset.csv`** | Real-time system metrics per sample (timestamp, CPU%, RAM%, I/O, network, processes, battery, etc.) |
| **`Experiment Control/annotations.csv`** | Event log: start/end times, command, type |
| **`Experiment Control/schedule.json`** | Automatically generated experiment schedule |

---

## 🖥️ OS Compatibility

- ✅ **Windows 10/11**
- ✅ **Linux** (Ubuntu/Debian/Fedora, etc.)
- ✅ **macOS** (Intel & Apple Silicon)

> **Notes:**
> - Battery metrics may appear as `None` on desktop or server systems (normal).  
> - For Linux, some sensors may require elevated permissions.  
> - Path separators differ between Windows (`\\`) and Unix (`/`).

---

## 🧯 Troubleshooting

- **“No module named psutil”** → Run `pip install psutil` inside your environment.  
- **Path issues** → Always execute runners from `Experiment Control/`.  
- **Disk stress** → `disk_stress.py` writes large files — ensure enough free space.  
- **Long logging duration** → Adjust `DURATION` in `psutil_logger.py`.  
- **Battery columns empty** → Normal for servers; can safely drop those columns.

---


## 🌱 Future Improvements

- Add `fingerprint.py` to capture host hardware/software info.  
- Central configuration file (`config.yaml`).  
- Validation script (`validate.py`) to measure twin fidelity.  
- Optional integration with Prometheus exporter or Grafana dashboard.

---
