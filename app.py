import sys
import win32gui
import win32con


def always_on_top(hwnd, *args):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


def main():
    if not sys.argv[1:]:
        print("Please specify a window title")
        sys.exit(1)

    target_window = sys.argv[1]

    win32gui.EnumWindows(always_on_top, target_window)


if __name__ == "__main__":
    main()
