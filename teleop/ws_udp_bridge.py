import asyncio
import json
import socket
import websockets

UDP_HOST = "127.0.0.1"
UDP_PORT = 5005
WS_HOST = "0.0.0.0"
WS_PORT = 8765

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

async def handle_client(websocket):
    print("Quest/WebSocket-Client verbunden")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)

                # Nur erwartete Tracking-Daten weiterleiten
                if not isinstance(data, dict):
                    continue

                allowed = ("head", "left_hand", "right_hand")
                packet = {
                    key: data[key]
                    for key in allowed
                    if key in data
                }

                if packet:
                    udp.sendto(
                        json.dumps(packet).encode("utf-8"),
                        (UDP_HOST, UDP_PORT),
                    )
                    print("Tracking:", packet)

            except (json.JSONDecodeError, TypeError, ValueError) as exc:
                print("Ungültige Nachricht:", exc)
    except websockets.ConnectionClosed:
        print("Client getrennt")

async def main():
    print(f"WebSocket-Bridge auf ws://0.0.0.0:{WS_PORT}")
    async with websockets.serve(handle_client, WS_HOST, WS_PORT):
        await asyncio.Future()

asyncio.run(main())
