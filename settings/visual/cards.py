from settings.screen.size import scaled_w, scaled_h


class DetailCardSize:
    X = 0
    Y = 0
    X_SIZE = scaled_w(0.043)
    Y_SIZE = scaled_h(0.11)


class SkillCardSize:
    X = 0
    Y = 0
    Y_SIZE = int(scaled_h(0.16))
    X_SIZE = int(Y_SIZE * 0.7143)
    SIZE = X_SIZE, Y_SIZE
