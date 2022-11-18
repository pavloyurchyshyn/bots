from pygame import Surface, SRCALPHA


def get_surface(h_size, v_size=None, transparent: (bool, int) = 0, flags=SRCALPHA, color=None):
    v_size = v_size if v_size else h_size

    if not transparent:
        flags = 0

    surface = Surface((h_size, v_size), flags, 32)

    if color:
        surface.fill(color)

    surface.convert_alpha()
    return surface
