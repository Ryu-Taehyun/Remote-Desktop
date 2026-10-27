# Remote Desktop

Python 소켓 통신과 화면 캡처·전송을 연습하는 예제 프로젝트입니다. JSON 명령 통신, 로컬 화면 미리보기, TCP 기반 화면 송수신을 각각 실행할 수 있습니다.

현재 구현된 기능은 화면 보기와 예제 명령 교환입니다. 마우스·키보드 원격 제어는 구현되어 있지 않습니다.

## 파일 구성

| 파일 | 역할 |
| --- | --- |
| `Client/server.py` | TCP 9000 포트에서 JSON 명령을 수신하고 응답 |
| `Client/client.py` | PING, TIME, EXIT 명령을 입력받아 서버에 전송 |
| `Client/screen.py` | 첫 번째 모니터 캡처, JPEG 미리보기 및 JPEG·PNG 크기 출력 |
| `Client/screen_sender.py` | TCP 9001 포트에서 연결을 기다리고 화면을 JPEG로 전송 |
| `Client/screen_viewer.py` | JPEG 프레임을 수신·복원하여 OpenCV 창에 표시 |
| `requirements.md` | 실행 환경과 의존성 설명 |
| `requirements.txt` | pip 설치용 패키지 목록 |
| `.gitignore` | 캐시, 가상환경, 환경변수 파일, 캡처 폴더 등의 업로드 제외 규칙 |

## 한 번에 실행 (Windows)

Python 3와 Git for Windows가 설치된 상태에서 **start.bat를 더블클릭**하세요. 저장소 전체를 다운로드하거나 복제한 폴더에서 실행합니다.

Bash가 가상환경을 만들고 필요한 패키지가 없으면 설치한 뒤, 다음 5개 프로그램을 별도 창으로 실행합니다. 최초 설치에는 인터넷 연결이 필요합니다.

1. JSON 명령 서버 (server.py)
2. 화면 전송 서버 (screen_sender.py)
3. 명령 입력 클라이언트 (client.py)
4. 화면 수신 뷰어 (screen_viewer.py)
5. 로컬 화면 미리보기 (screen.py)

서버가 실제로 연결을 기다리는 상태가 된 후 클라이언트와 뷰어를 시작합니다. 기존 프로그램이 9000 또는 9001 포트를 사용 중이면 중복 실행을 중단합니다.

실행 창을 열어 두세요. **실행 창에서 Ctrl+C를 누르면 이번에 시작한 프로그램을 모두 종료**합니다. 개별 창의 EXIT, Esc, q 등도 기존과 같이 사용할 수 있습니다. 실행 창의 X 버튼으로 닫으면 개별 창이 남을 수 있으므로 Ctrl+C로 종료하세요.

Git Bash에서 직접 실행하려면 저장소 루트에서 다음 명령을 사용합니다.

```bash
bash start.sh
```

자동 실행기는 Windows용입니다. 화면 캡처가 시작되므로 실행 전에 캡처할 모니터의 내용을 확인하세요.

## 설치

Windows PowerShell 기준입니다. Python 3와 pip가 필요하며 화면 예제에는 그래픽 데스크톱 세션이 필요합니다. 패키지 상세는 [requirements.md](requirements.md)를 참고하세요.

```powershell
git clone https://github.com/Ryu-Taehyun/Remote-Desktop.git
cd Remote-Desktop
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

가상환경 활성화 없이 해당 환경의 Python을 직접 실행하는 방식입니다. 아래 명령은 모두 저장소 루트에서 실행합니다.

## 실행

### 1. JSON 명령 통신

첫 번째 터미널에서 서버를 실행합니다.

```powershell
.\.venv\Scripts\python.exe Client\server.py
```

두 번째 터미널에서 클라이언트를 실행합니다.

```powershell
.\.venv\Scripts\python.exe Client\client.py
```

| 명령 | 응답 |
| --- | --- |
| `PING` | PONG 및 성공 상태 |
| `TIME` | 서버 컴퓨터의 현재 시각 (YYYY-MM-DD HH:MM:SS) |
| `EXIT` | 종료 응답 후 양쪽 연결 종료 |

입력은 대문자로 변환됩니다. 그 밖의 명령에는 오류 응답을 반환합니다.

### 2. 로컬 화면 미리보기

```powershell
.\.venv\Scripts\python.exe Client\screen.py
```

첫 번째 모니터를 캡처하여 1280×720, JPEG 품질 70으로 변환한 화면을 표시합니다. JPEG 크기와 원본 캡처의 PNG 크기를 출력하고 반복마다 1초 대기합니다. 두 크기는 해상도도 다르므로 압축 형식만의 공정한 비교는 아닙니다.

화면 창에서 Esc 또는 q를 누르거나 터미널에서 Ctrl+C로 종료합니다.

### 3. 화면 송수신

첫 번째 터미널에서 전송 서버를 실행합니다.

```powershell
.\.venv\Scripts\python.exe Client\screen_sender.py
```

두 번째 터미널에서 뷰어를 실행합니다.

```powershell
.\.venv\Scripts\python.exe Client\screen_viewer.py
```

뷰어 창에서 Esc를 눌러 종료합니다. 전송 서버는 Ctrl+C로 중지할 수 있습니다. 전송 영상은 1280×720, JPEG 품질 70이며 별도 FPS 제한이 없습니다.

## 통신 설정과 형식

- 기본 주소는 모든 소켓 예제에서 `127.0.0.1`이므로 같은 컴퓨터에서 실행합니다.
- JSON 명령 통신은 포트 `9000`, 화면 송수신은 포트 `9001`을 사용합니다.
- 본문 앞에 `struct.pack("!I", 크기)`로 만든 4바이트 unsigned big-endian 길이 헤더를 붙입니다.
- JSON 본문은 UTF-8이며 수신 크기 제한은 1 MiB입니다.
- 화면 본문은 JPEG 바이트이며 뷰어는 0바이트 또는 10 MiB 초과 프레임을 거부합니다.
- 두 서버 모두 연결 한 개를 수락하는 구조입니다. 재접속하려면 서버를 다시 실행해야 합니다.

다른 컴퓨터에서 연결하려면 서버 파일의 바인딩 주소와 클라이언트 파일의 접속 주소를 각각 수정해야 합니다. 현재 인증·암호화가 없으므로 기본 로컬 실습 환경에서 사용하세요.

## 문제 해결

- **연결 거부**: 대응하는 서버를 먼저 실행하고 주소·포트가 일치하는지 확인합니다.
- **포트 사용 중**: 이전 서버 프로세스를 종료하거나 양쪽 파일의 포트를 함께 변경합니다.
- **모듈을 찾을 수 없음**: 실행할 가상환경의 Python으로 `-m pip install -r requirements.txt`를 실행합니다.
- **화면 캡처 또는 창 표시 실패**: 첫 번째 모니터가 있는 데스크톱 세션인지, opencv-python GUI 패키지가 설치되어 있는지 확인합니다.

## 검증 범위

문서는 현재 소스의 동작을 기준으로 작성했습니다. 패키지 버전은 원본에 명시되지 않아 고정하지 않았으며, 실제 화면 캡처·송수신 동작과 플랫폼별 호환성은 별도 실행 검증이 필요합니다.

