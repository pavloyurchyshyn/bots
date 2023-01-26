from settings.screen.size import scaled_w, scaled_h


class MapRect:
    x = scaled_w(0.)
    y = scaled_h(0.025)
    h_size = scaled_w(0.80)
    v_size = scaled_h(0.7)
    rect = (x, y, h_size, v_size)


class MechWin:
    x = scaled_w(0.8)
    y = scaled_h(0.225)
    h_size = scaled_w(0.2)
    v_size = scaled_h(0.5)
    rect = (x, y, h_size, v_size)


class Tasks:
    x = scaled_w(0.8)
    y = scaled_h(0.025)
    h_size = scaled_w(0.20)
    v_size = scaled_h(0.2)
    rect = (x, y, h_size, v_size)


class TileInfo:
    x = scaled_w(0.8)
    y = scaled_h(0.725)
    h_size = scaled_w(0.2)
    v_size = scaled_h(0.275)
    rect = (x, y, h_size, v_size)


_CARDS_V_SIZE = (scaled_h(1) - MapRect.y - MapRect.v_size) // 2
_CARDS_H_SIZE = scaled_w(0.5)


class UsedCards:
    x = scaled_w(0.2)
    y = scaled_h(0.725)
    h_size = _CARDS_H_SIZE
    v_size = _CARDS_V_SIZE
    rect = (x, y, h_size, v_size)


class CardsDeck:
    x = scaled_w(0.2)
    y = scaled_h(0.725) + _CARDS_V_SIZE
    h_size = _CARDS_H_SIZE
    v_size = _CARDS_V_SIZE
    rect = (x, y, h_size, v_size)


class ReadyWindow:
    x = scaled_w(0.2) + _CARDS_H_SIZE
    y = MapRect.y + MapRect.v_size
    h_size = scaled_w(0.1)
    v_size = scaled_h(1) - MapRect.y - MapRect.v_size
    rect = (x, y, h_size, v_size)

    RBtn_x_k = 0.725
    RBtn_y_k = 0.975
    RBtn_h_size = 0.05
    RBtn_v_size = 0.02

    Timer_x_k = 0.725
    Timer_y_k = 0.95
    Timer_h_size = 0.05
    Timer_v_size = 0.02


class ChatSize:
    x_k = 0.0
    y_k = 0.725
    h_size_k = 0.20
    v_size_k = 0.225

    inp_x_k = x_k
    inp_y_k = y_k + v_size_k
    inp_h_size_k = h_size_k * 0.9
    inp_v_size_k = 0.05

    send_x_k = x_k + inp_h_size_k
    send_y_k = y_k + v_size_k
    send_h_size_k = h_size_k * 0.1
    send_v_size_k = inp_v_size_k
