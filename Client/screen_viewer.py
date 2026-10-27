
import socket
import struct
import cv2
import numpy as np

HOST = "127.0.0.1"
PORT = 9001

MAX_IMAGE_SIZE = 10 * 1024 * 1024


# 정확한 크기만큼 수신하는 함수
def recv_exact(sock, size):
    data = b""

    while len(data) < size:
        remaining = size - len(data)

        chunk = sock.recv(remaining)

        if not chunk:
            raise ConnectionError("연결이 종료되었습니다.")

        data += chunk

    return data


# Viewer 소켓 생성
viewer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Host 연결
    viewer.connect((HOST, PORT))

    print("[VIEWER] 서버 연결 성공")

    while True:
        # 1. 헤더 수신
        header = recv_exact(viewer, 4)

        # 2. 이미지 크기 해석
        image_size = struct.unpack("!I", header)[0]

        # 3. 크기 검사
        if image_size == 0 or image_size > MAX_IMAGE_SIZE:
            raise ValueError("잘못된 이미지 크기")

        # 4. JPEG 데이터 수신
        image_data = recv_exact(viewer, image_size)

        # 5. NumPy 배열 변환
        image_array = np.frombuffer(
            image_data,
            dtype=np.uint8
        )

        # 6. JPEG 이미지 복원
        decoded_frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if decoded_frame is None:
            print("[ERROR] 이미지 복원 실패")
            continue

        # 7. 실시간 화면 출력
        cv2.imshow("Remote Screen", decoded_frame)

        # 8. ESC 키로 종료
        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            print("[VIEWER] ESC 종료")
            break

except KeyboardInterrupt:
    print("[VIEWER] 사용자 중지")

except (ConnectionError, OSError, ValueError, cv2.error) as e:
    print("[VIEWER ERROR]", e)

finally:
    viewer.close()
    cv2.destroyAllWindows()
    print("[VIEWER] 프로그램 종료")

