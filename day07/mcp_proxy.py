"""记录并转发 Codex 与本地 MCP 服务之间的 stdio 消息。

Codex 启动本文件，本文件再启动同目录的 mcp.py。
stdout 只转发协议消息；日志写入 mcp_logs/，提示写入 stderr。
"""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import threading


def main() -> int:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", type=Path, default=base / "mcp.py")
    parser.add_argument("--log-dir", type=Path, default=base / "mcp_logs")
    args = parser.parse_args()
    server = args.server.resolve()
    if not server.is_file():
        parser.error(f"MCP 服务文件不存在: {server}")

    # Windows 文本模式可能转换换行符；转发时使用二进制模式保留原始字节。
    if os.name == "nt":
        import msvcrt

        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    args.log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_path = args.log_dir / f"mcp_io_{stamp}_{os.getpid()}.log"
    lock = threading.Lock()

    with log_path.open("a", encoding="utf-8", buffering=1) as log:
        def record(direction: str, data: bytes) -> None:
            # 仅格式化日志副本；管道中的原始消息不会被重新编码或修改。
            body = data.decode("utf-8", errors="replace").rstrip("\r\n")
            try:
                body = json.dumps(json.loads(body), ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                pass
            with lock:
                log.write(f"\n[{datetime.now().astimezone().isoformat(timespec='milliseconds')}] {direction}\n{body}\n")

        command = [sys.executable, "-u", str(server)]
        record("PROXY START", subprocess.list2cmdline(command).encode("utf-8"))
        print(f"[MCP proxy] Log: {log_path}", file=sys.stderr, flush=True)
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUNBUFFERED"] = "1"
        child = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
        finished = threading.Event()

        def from_client() -> None:
            try:
                for line in iter(sys.stdin.buffer.readline, b""):
                    if finished.is_set():
                        break
                    record("Codex -> MCP Server", line)
                    child.stdin.write(line)
                    child.stdin.flush()
            except (BrokenPipeError, OSError, ValueError):
                pass
            finally:
                try:
                    child.stdin.close()
                except (BrokenPipeError, OSError, ValueError):
                    pass

        def from_stderr() -> None:
            for line in iter(child.stderr.readline, b""):
                record("MCP Server stderr (日志，不是协议消息)", line)
                try:
                    sys.stderr.buffer.write(line)
                    sys.stderr.buffer.flush()
                except (BrokenPipeError, OSError):
                    pass

        threading.Thread(target=from_client, daemon=True).start()
        error_thread = threading.Thread(target=from_stderr, daemon=True)
        error_thread.start()
        try:
            for line in iter(child.stdout.readline, b""):
                record("MCP Server -> Codex", line)
                sys.stdout.buffer.write(line)
                sys.stdout.buffer.flush()
        except (BrokenPipeError, KeyboardInterrupt):
            pass
        finally:
            finished.set()
            if child.poll() is None:
                try:
                    child.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    child.terminate()
                    try:
                        child.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        child.wait()
            error_thread.join(timeout=3)
            record("PROXY STOP", f"Server exit code: {child.returncode}".encode())
        return child.returncode or 0


if __name__ == "__main__":
    raise SystemExit(main())
