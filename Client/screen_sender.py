
import socket
import struct
import mss
import cv2
import numpy as np

HOST = "127.0.0.1"
PORT = 9001

# TCP 서버 생성
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print("[HOST] 연결 대기 중...")

try:
    # Viewer 연결 수락
    client, address = server.accept()
    print("[CONNECTED]", address)

    with client:
        # 화면 캡처 객체 생성
        with mss.MSS() as sct:
            monitor = sct.monitors[1]

            print("[HOST] 화면 전송 시작")

            while True:
                # 1. 화면 캡처
                screenshot = sct.grab(monitor)

                # 2. NumPy 배열 변환
                frame = np.array(screenshot)

                # 3. BGRA -> BGR 변환
                frame_bgr = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGRA2BGR
                )

                # 4. 1280x720으로 축소
                resized_frame = cv2.resize(
                    frame_bgr,
                    (1280, 720)
                )

                # 5. JPEG 품질 70으로 압축
                success, encoded = cv2.imencode(
                    ".jpg",
                    resized_frame,
                    [cv2.IMWRITE_JPEG_QUALITY, 70]
                )

                if not success:
                    print("[ERROR] JPEG 압축 실패")
                    break

                # 6. bytes 변환
                jpeg_data = encoded.tobytes()

                # 7. 이미지 크기 계산
                image_size = len(jpeg_data)

                # 8. 4바이트 헤더 생성
                header = struct.pack("!I", image_size)

                # 9. 헤더와 이미지 전송
                try:
                    client.sendall(header + jpeg_data)

                except (BrokenPipeError, ConnectionResetError):
                    print("[HOST] Viewer 연결 종료")
                    break

except KeyboardInterrupt:
    print("[HOST] 사용자 중지")

except OSError as e:
    print("[HOST ERROR]", e)

finally:
    server.close()
    print("[HOST] 서버 종료")

