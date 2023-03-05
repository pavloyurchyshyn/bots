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
    class Title:
        x = 0.0
        y = 0.725
        h_size = 0.20
        v_size = 0.02

    x = scaled_w(0.0)
    y = scaled_h(0.745)
    h_size = scaled_w(0.20)
    v_size = scaled_h(0.255)
    rect = (x, y, h_size, v_size)


class ChatSize:
    x_k = 0.8
    y_k = 0.025
    h_size_k = 0.20
    v_size_k = 0.175

    inp_x_k = x_k
    inp_y_k = y_k + v_size_k
    inp_h_size_k = h_size_k * 0.9
    inp_v_size_k = 0.025

    send_x_k = x_k + inp_h_size_k
    send_y_k = y_k + v_size_k
    send_h_size_k = h_size_k * 0.1
    send_v_size_k = inp_v_size_k


class TileInfo:
    x = scaled_w(0.8)
    y = scaled_h(0.725)
    h_size = scaled_w(0.2)
    v_size = scaled_h(0.275)
    rect = (x, y, h_size, v_size)


CARDS_V_SIZE = scaled_h(0.17)


class UsedCards:
    x = scaled_w(0.2)
    y = scaled_h(0.725)
    h_size = scaled_w(0.5)
    v_size = CARDS_V_SIZE  # scaled_h(0.1355)
    size = h_size, v_size
    rect = (x, y, h_size, v_size)


class HpBar:
    x = scaled_w(0.2)
    y = scaled_h(0.725 + 0.1375 - 0.02)
    h_size = scaled_w(0.5)
    v_size = scaled_h(0.02)
    rect = (x, y, h_size, v_size)


class ManaBar:
    x = scaled_w(0.2)
    y = scaled_h(0.725 + 0.1375)
    h_size = scaled_w(0.5)
    v_size = scaled_h(0.02)
    rect = (x, y, h_size, v_size)


class CardsDeck:
    x = scaled_w(0.2)
    y = scaled_h(0.725 + 0.1375 + 0.02)
    h_size = scaled_w(0.5)
    v_size = CARDS_V_SIZE  # scaled_h(0.1175)
    size = h_size, v_size
    rect = (x, y, h_size, v_size)


class ReadyWindow:
    x = scaled_w(0.7)
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

    ReadyPlayers_x = 0.725
    ReadyPlayers_y = 0.725
    ReadyPlayers_h_size = 0.05
    ReadyPlayers_v_size = 0.02
