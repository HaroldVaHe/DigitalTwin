import psutil

# Uso del CPU (%)
print("CPU usage:", psutil.cpu_percent(interval=1), "%")

# Memoria RAM
ram = psutil.virtual_memory()
print("RAM total:", ram.total / (1024 ** 3), "GB")
print("RAM usada:", ram.percent, "%")

# Disco
disk = psutil.disk_usage('/')
print("Uso del disco:", disk.percent, "%")

# Red
net = psutil.net_io_counters()
print("Bytes enviados:", net.bytes_sent)
print("Bytes recibidos:", net.bytes_recv)
