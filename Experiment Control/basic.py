import psutil

# Uso del CPU (%)
print("CPU usage:", psutil.cpu_percent(interval=1), "%")

# Memoria RAM
ram = psutil.virtual_memory()
print("RAM total:", ram.total / (1024 ** 3), "GB")
print("RAM usage:", ram.percent, "%")

# Disco
disk = psutil.disk_usage('/')
print("disk usage:", disk.percent, "%")

# Red
net = psutil.net_io_counters()
print("sent Bytes:", net.bytes_sent)
print("received Bytes:", net.bytes_recv)
