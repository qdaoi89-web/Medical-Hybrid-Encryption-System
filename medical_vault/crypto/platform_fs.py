import sys


def hide_file_if_windows(path: str) -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes

        ctypes.windll.kernel32.SetFileAttributesW(path, 0x02)
    except Exception:
        pass
