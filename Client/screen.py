
import mss
import mss.tools
import time
import cv2
import numpy as np

# 화면 캡처 객체 생성
sct = mss.MSS()

# 첫 번째 모니터 선택
monitor = sct.monitors[1]

try:
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

        # 4. 해상도 축소 (1280x720)
        resized_frame = cv2.resize(
            frame_bgr,
            (1280, 720)
        )

        # 5. JPEG 압축 (품질 70)
        success, encoded = cv2.imencode(
            ".jpg",
            resized_frame,
            [cv2.IMWRITE_JPEG_QUALITY, 70]
        )

        if success:
            # 6. JPEG 바이트 데이터 생성
            jpeg_data = encoded.tobytes()

            print("[JPEG] 크기:", len(jpeg_data), "bytes")

            # 7. JPEG 데이터를 NumPy 배열로 변환
            image_array = np.frombuffer(
                jpeg_data,
                dtype=np.uint8
            )

            # 8. JPEG 이미지 복원
            decoded_frame = cv2.imdecode(
                image_array,
                cv2.IMREAD_COLOR
            )

            # 9. 복원된 이미지 출력
            if decoded_frame is not None:
                cv2.imshow("Screen Viewer", decoded_frame)

                # 10. ESC 또는 Q 키를 누르면 종료
                key = cv2.waitKey(1) & 0xFF

                if key == 27 or key == ord("q"):
                    print("[SCREEN] 사용자 종료")
                    break

        # 11. PNG 이미지 크기 비교
        png_data = mss.tools.to_png(
            screenshot.rgb,
            screenshot.size
        )

        png_size = len(png_data)

        print("[PNG] 크기:", png_size, "bytes")

        # 12. 1초 대기
        time.sleep(1)

except KeyboardInterrupt:
    print("[SCREEN] Ctrl+C 종료")

finally:
    # 13. 화면 캡처 및 OpenCV 자원 정리
    sct.close()
    cv2.destroyAllWindows()

    print("[SCREEN] 프로그램 종료")
