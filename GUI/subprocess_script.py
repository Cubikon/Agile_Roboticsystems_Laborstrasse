# subprocess_script.py
import sys

def main():
    print("Starting command processor. Type 'exit' to stop.")
    while True:
        line = sys.stdin.readline().strip()
        if line:
            print(f"Received: {line}")
            if line.lower() == 'exit':
                break

if __name__ == "__main__":
    main()
