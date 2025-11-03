import os, time, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size_mb", type=int, default=1024)
    parser.add_argument("--block_mb", type=int, default=5)
    parser.add_argument("--path", type=str, default="stress_file.bin")
    parser.add_argument("--sleep", type=float, default=0.5)
    args = parser.parse_args()

    written = 0
    print(f"💾 Generando {args.size_mb} MB en bloques de {args.block_mb} MB...")
    with open(args.path, "wb") as f:
        while written < args.size_mb:
            f.write(os.urandom(args.block_mb * 1024 * 1024))
            f.flush()
            os.fsync(f.fileno())
            written += args.block_mb
            time.sleep(args.sleep)
    print("✅ Stress de disco completado")
