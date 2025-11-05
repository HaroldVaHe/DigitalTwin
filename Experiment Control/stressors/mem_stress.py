import time, argparse

MB = 1024 * 1024

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--step_mb", type=int, default=500)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--sleep", type=int, default=10)
    args = parser.parse_args()

    blocks = []
    print(f"💡 Iniciando stress de memoria: {args.steps * args.step_mb} MB totales")
    for i in range(args.steps):
        blocks.append(bytearray(args.step_mb * MB))
        print(f"🧠 Reservados {args.step_mb*(i+1)} MB")
        time.sleep(args.sleep)
    print("✅ Stress de memoria completado")
    time.sleep(60)  # mantener uso antes de liberar
