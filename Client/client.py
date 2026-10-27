import socket
import json
import struct

HOST = "127.0.0.1"
PORT = 9000

MAX_SIZE = 1024 * 1024


# 지정한 크기만큼 데이터 수신
def recv_exact(sock, size):
    data = b""

    while len(data) < size:
        remaining = size - len(data)
        chunk = sock.recv(remaining)

        if not chunk:
            raise ConnectionError("연결이 종료되었습니다.")

        data += chunk

    return data


# JSON 메시지 전송
def send_json(sock, message):
    json_data = json.dumps(message).encode("utf-8")

    data_size = len(json_data)

    header = struct.pack("!I", data_size)

    sock.sendall(header + json_data)


# JSON 메시지 수신
def recv_json(sock):
    header = recv_exact(sock, 4)

    response_size = struct.unpack("!I", header)[0]

    if response_size > MAX_SIZE:
        raise ValueError("메시지 크기 초과")

    json_data = recv_exact(sock, response_size)

    message = json_data.decode("utf-8")

    response = json.loads(message)

    return response


# 클라이언트 생성
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))

    print("[CLIENT] 서버 연결 성공")

    while True:
        user_input = input(
            "명령어(PING/TIME/EXIT): "
        ).strip().upper()

        if not user_input:
            continue

        message = {
            "type": user_input,
            "data": "Hello Server!"
        }

        send_json(client, message)

        response = recv_json(client)

        print("[SERVER]", response)

        if user_input == "EXIT":
            break

except (ConnectionError, OSError, ValueError) as e:
    print("[ERROR]", e)

finally:
    client.close()
    print("[CLIENT] 종료")