#!/usr/bin/env python3
"""将已经整理好的会议总结保存为 UTF-8 Markdown，不覆盖同名文件。"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path(r"D:\Develop-project3\summeryConferance")


def validate_filename(filename: str) -> str:
    """仅接受安全的单个 Markdown 文件名，不接受目录路径。"""
    if not filename or filename in (".", ".."):
        raise ValueError("文件名不能为空。")
    if re.search(r'[<>:"/\\|?*\x00-\x1f]', filename):
        raise ValueError("文件名不能包含路径、控制字符或 Windows 非法字符。")
    if filename.endswith((" ", ".")):
        raise ValueError("文件名不能以空格或句点结尾。")
    reserved = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
    reserved.update(f"{prefix}{number}" for prefix in ("COM", "LPT") for number in range(1, 10))
    if filename.split(".", 1)[0].rstrip().upper() in reserved:
        raise ValueError("文件名不能使用 Windows 保留名称。")
    suffix = Path(filename).suffix
    if not suffix:
        filename += ".md"
    elif suffix.lower() != ".md":
        raise ValueError("输出文件必须使用 .md 扩展名。")
    return filename


def save_meeting_minutes(
    content: str,
    filename: str | None = None,
    output_dir: Path | None = None,
) -> Path:
    if not content.strip():
        raise ValueError("会议总结内容不能为空。")
    if "\x00" in content:
        raise ValueError("会议总结不能包含空字符，请提供 UTF-8 文本。")
    if filename is None:
        timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"会议纪要_{timestamp}.md"
    filename = validate_filename(filename)
    directory = DEFAULT_OUTPUT_DIR if output_dir is None else Path(output_dir).expanduser()
    if not directory.is_dir():
        raise NotADirectoryError(f"输出目录不存在或不是目录：{directory}")
    target = directory.resolve() / filename
    try:
        with target.open("x", encoding="utf-8", newline="\n") as output:
            output.write(content.rstrip() + "\n")
    except FileExistsError as error:
        raise FileExistsError(f"文件已存在，未覆盖；请更换文件名：{target}") from error
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="已整理好的 UTF-8 文本文件；使用 - 从标准输入读取")
    parser.add_argument("--filename", help="输出文件名，默认使用带时间戳的会议纪要文件名")
    parser.add_argument("--output-dir", type=Path, help=f"可选：指定其他已有目录；默认：{DEFAULT_OUTPUT_DIR}")
    args = parser.parse_args()
    try:
        if args.input == "-":
            content = sys.stdin.buffer.read().decode("utf-8-sig")
        else:
            content = Path(args.input).read_text(encoding="utf-8-sig")
        target = save_meeting_minutes(content, args.filename, args.output_dir)
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, f"保存失败：{error}\n")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
