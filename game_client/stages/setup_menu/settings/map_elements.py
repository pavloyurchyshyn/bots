from settings.screen.size import scaled_w, scaled_h


class MapRect:
    H_size = scaled_w(0.7)
    V_size = scaled_h(0.7)
    X = 0
    Y = scaled_h(0.05)
    rect = (X, Y, H_size, V_size)
