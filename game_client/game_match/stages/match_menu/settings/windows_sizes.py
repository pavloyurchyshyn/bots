
from settings.screen.size import scaled_w, scaled_h


class MapRect:
    x = scaled_w(0.15)
    y = scaled_h(0.05)
    h_size = scaled_w(0.65)
    v_size = scaled_h(0.7)
    rect = (x, y, h_size, v_size)


class MechWin:
    x_k = scaled_w(0.8)
    y_k = scaled_h(0.05)
    h_size = scaled_w(0.2)
    v_size = scaled_h(0.7)
    rect = (x_k, y_k, h_size, v_size)


class HPBar:
    x_k = scaled_w(0.2)
    y_k = MapRect.y + MapRect.v_size
    h_size = scaled_w(0.5)
    v_size = (scaled_h(1) - MapRect.y - MapRect.v_size) // 2
    rect = (x_k, y_k, h_size, v_size)


class ManaBar:
    x_k = HPBar.x_k
    y_k = HPBar.y_k + HPBar.v_size
    h_size = HPBar.h_size
    v_size = HPBar.v_size
    rect = (x_k, y_k, h_size, v_size)


class ChatSize:
    x_k = 0.0
    y_k = 0.75
    h_size_k = 0.20
    v_size_k = 0.2

    inp_x_k = x_k
    inp_y_k = y_k + v_size_k
    inp_h_size_k = h_size_k * 0.9
    inp_v_size_k = 0.05

    send_x_k = x_k + inp_h_size_k
    send_y_k = y_k + v_size_k
    send_h_size_k = h_size_k * 0.1
    send_v_size_k = inp_v_size_k
