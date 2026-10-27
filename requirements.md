# 실행 환경 및 의존성

이 목록은 `Client/` 안의 파이썬 파일 5개의 import를 기준으로 작성했습니다.

## 환경

Python 3와 pip가 필요합니다. 원본에 지원 버전 정보가 없어 특정 최소 버전이나 패키지 버전을 보장하지 않습니다. 화면 예제는 모니터가 있는 그래픽 데스크톱 세션에서 실행해야 합니다.

## 외부 패키지

| 설치 이름 | import 이름 | 용도 |
| --- | --- | --- |
| `mss` | `mss`, `mss.tools` | screen.py, screen_sender.py: 모니터 캡처 및 PNG 변환 |
| `opencv-python` | `cv2` | 화면 관련 파일 3개: 색상·크기 변환, JPEG 인코딩·디코딩, 창 표시 |
| `numpy` | `numpy` | 화면 관련 파일 3개: 이미지 배열 변환 |

`cv2.imshow()`를 사용하므로 GUI 기능이 없는 `opencv-python-headless`로 대체하면 창 표시가 동작하지 않습니다.

## 표준 라이브러리

`socket`, `json`, `struct`, `datetime`, `time`은 Python에 포함되어 별도 설치가 필요하지 않습니다. client.py와 server.py만 실행한다면 외부 패키지가 필요하지 않습니다.

## 설치

저장소 루트에서 실행합니다.

```powershell
python -m pip install -r requirements.txt
python -m pip check
```

`requirements.txt`는 pip 설치용이고, 이 문서는 의존성 설명용입니다. 원본에 버전 정보가 없어 버전을 고정하지 않았습니다. 특정 조합의 설치 및 실제 화면 송수신 호환성은 별도 검증이 필요합니다.
