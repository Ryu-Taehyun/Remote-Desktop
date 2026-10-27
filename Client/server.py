import socket
import json
import struct
from datetime import datetime

# Target Host
HOST = "127.0.0.1"
PORT = 9000

# Size Limiter
MAX_SIZE = 1024 * 1024

# Send Correct Size
def recv_exact(sock, size):
    data = b""

    while len(data) < size:
        remaining = size - len(data)
        chunk = sock.recv(remaining)

        if not chunk:
            raise ConnectionError("연결이 종료되었습니다.")

        data += chunk

    return data

# JSON Encoding
def recv_json(sock):
    header = recv_exact(sock, 4)

    data_size = struct.unpack("!I", header)[0]

    if data_size > MAX_SIZE:
        raise ValueError("메시지 크기 초과")

    json_data = recv_exact(sock, data_size)

    message = json_data.decode("utf-8")
    parsed = json.loads(message)

    return parsed

# Send JSON Message
def send_json(sock, response):
    json_response = json.dumps(response).encode("utf-8")

    response_size = len(json_response)

    header = struct.pack("!I", response_size)

    sock.sendall(header + json_response)

# Create Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print("[SERVER] 연결 대기 중...")

# Server INFO
try:
    client, address = server.accept()

    print("[CONNECTED]", address)

    with client:
        while True:
            try:
                parsed = recv_json(client)

                command = parsed["type"]
                content = parsed.get("data", "")

                print("[RECEIVED]", command, content)

                if command == "PING":
                    response = {
                        "type": "PONG",
                        "status": "success"
                    }

                elif command == "TIME":
                    response = {
                        "type": "TIME",
                        "data": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    }

                elif command == "EXIT":
                    response = {
                        "type": "EXIT",
                        "status": "success"
                    }

                    send_json(client, response)
                    break

                else:
                    response = {
                        "type": "ERROR",
                        "message": "알 수 없는 명령어"
                    }

                send_json(client, response)

            except (ConnectionError, OSError, ValueError,
                    KeyError, TypeError) as e:
                print("[ERROR]", e)
                break

finally:
    server.close()
    print("[SERVER] 종료")