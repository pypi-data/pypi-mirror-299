import time

if __name__ == "__main__":
    for step in range(5):
        print(f"Step {step}", flush=True)
        time.sleep(1)
    print("Now, I will hang forever", flush=True)
    while True:
        time.sleep(3600)
