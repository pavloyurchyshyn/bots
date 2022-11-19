import ctypes


user32 = ctypes.windll.user32
SCREEN_W, SCREEN_H = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SCREEN_W = 1870
SCREEN_H = 980


def scaled_w(k) -> int:
    return int(SCREEN_W * k)


def scaled_h(k) -> int:
    return int(SCREEN_H * k)
