import multiprocessing, time, argparse

def worker(t):
    end = time.time() + t
    while time.time() < end:
        x = 0
        for i in range(50000):
            x += i*i

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--procs", type=int, default=4)
    parser.add_argument("--duration", type=int, default=60)
    args = parser.parse_args()

    print(f"🔥 CPU Stress iniciado ({args.procs} procesos, {args.duration}s)")
    procs = []
    for _ in range(args.procs):
        p = multiprocessing.Process(target=worker, args=(args.duration,))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()
    print("✅ CPU Stress finalizado")
