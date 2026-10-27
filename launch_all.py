"""Launch all five examples in separate Windows consoles."""
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def check_ports():
    # Binding does not consume the examples' single accepted connection.
    for port in (9000, 9001):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            try:
                probe.bind(("127.0.0.1", port))
            except OSError as exc:
                raise RuntimeError(
                    f"Port {port} is already in use. Close the previous examples first."
                ) from exc


def listening(pid, port):
    result = subprocess.run(
        ["netstat", "-ano", "-p", "tcp"], capture_output=True, text=True,
        creationflags=subprocess.CREATE_NO_WINDOW, check=True, timeout=5,
    )
    for line in result.stdout.splitlines():
        fields = line.split()
        if (len(fields) == 5 and fields[0] == "TCP"
                and fields[1] == f"127.0.0.1:{port}"
                and fields[3] == "LISTENING" and fields[4] == str(pid)):
            return True
    return False


def wait_for_server(process, port):
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Server for port {port} exited during startup.")
        if listening(process.pid, port):
            return
        time.sleep(0.2)
    raise RuntimeError(f"Server for port {port} did not become ready.")


def stop_all(processes):
    for process in reversed(processes):
        if process.poll() is None:
            process.terminate()
    for process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def main():
    if os.name != "nt":
        print("This launcher requires Windows.", file=sys.stderr)
        return 1
    processes = []
    environment = os.environ.copy()
    environment["PYTHONUNBUFFERED"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"

    def start(filename):
        print(f"Starting {filename}...")
        process = subprocess.Popen(
            [sys.executable, "-u", str(ROOT / "Client" / filename)],
            cwd=ROOT, env=environment,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
        processes.append(process)
        return process

    try:
        check_ports()
        server = start("server.py")
        sender = start("screen_sender.py")
        wait_for_server(server, 9000)
        wait_for_server(sender, 9001)
        start("client.py")
        start("screen_viewer.py")
        start("screen.py")
        print("All five examples started in separate windows.")
        print("Keep this launcher open. Press Ctrl+C here to stop all examples.")
        while any(process.poll() is None for process in processes):
            time.sleep(0.5)
        failed = [process.returncode for process in processes if process.returncode]
        if failed:
            raise RuntimeError(f"Some examples exited with errors: {failed}")
        return 0
    except KeyboardInterrupt:
        print("\nStopping all examples...")
        return 0
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"Startup/runtime error: {exc}", file=sys.stderr)
        return 1
    finally:
        stop_all(processes)


if __name__ == "__main__":
    raise SystemExit(main())
