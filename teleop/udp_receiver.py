import json
import socket
import time

HOST = "0.0.0.0"
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"Teleop UDP receiver listening on {HOST}:{PORT}", flush=True)

while True:
    data, addr = sock.recvfrom(65535)
    try:
        msg = json.loads(data.decode("utf-8"))
        print(f"\rFrom {addr}: {msg}", end="", flush=True)
    except (UnicodeDecodeError, json.JSONDecodeError):
        print(f"\nInvalid JSON from {addr}: {data[:100]!r}", flush=True)
