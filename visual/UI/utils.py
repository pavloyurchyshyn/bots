import os
from pygame import Surface, SRCALPHA
from pygame import image, error, transform, Color, surface, draw
from global_obj import Global

LOGGER = Global.logger


def get_surface(h_size, v_size=None, transparent: (bool, int) = 0, flags=SRCALPHA, color=None):
    v_size = v_size if v_size else h_size

    if not transparent:
        flags = 0

    surf = Surface((h_size, v_size), flags, 32)

    if color:
        surf.fill(color)

    surf.convert_alpha()
    return surf


try:
    # maybe another pictures will load
    ERROR_PICTURE = image.load('sprites/error.png').convert_alpha()
    ERROR_PICTURE = transform.rotate(ERROR_PICTURE, 90).convert_alpha()
except:
    ERROR_PICTURE = surface.Surface((100, 100))
    ERROR_PICTURE.fill((255, 0, 0))
    LOGGER.warning('Failed to load error img sprites/error.png')


def loaded_images_wrapper(func):
    loaded_ = {}

    def wrapper(path, size=None, angle=90, *args, **kwargs):
        if (path, size) not in loaded_:
            # LOGGER.info(f'Loading {path} {size}')
            loaded_[(path, size)] = func(path, size, *args, angle=angle, **kwargs)

        return loaded_[(path, size)]

    return wrapper


@loaded_images_wrapper
def load_image(path: str, size: (int, int) = None, angle=0, smooth_scale=True) -> surface.Surface:
    try:
        angle = angle if angle is not None else 90
        if not path.startswith('sprites'):
            path = os.path.join('sprites', path)

        pic = image.load(path)  # .convert_alpha()

        if size:
            size = (int(size[0]), int(size[1]))
            if smooth_scale:
                pic = transform.smoothscale(pic, size).convert_alpha()
            else:
                pic = transform.scale(pic, size).convert_alpha()

        pic = transform.rotate(pic, angle).convert_alpha()
        LOGGER.info(f'Loaded {path} {pic.get_size()}')
        return pic
    except (error, FileNotFoundError) as e:
        LOGGER.error(f'Failed to load {path}: {e}')
        if size:
            return transform.smoothscale(ERROR_PICTURE, size).convert_alpha()
        else:
            return ERROR_PICTURE.convert_alpha()


def __normalize_color(color) -> int:
    if color > 255:
        return 255
    elif color < 0:
        return 0
    else:
        return int(color)


def normalize_color(color) -> list:
    return list(map(__normalize_color, color))


# def recolor_picture(picture, color, recolor_key=(10, 10, 10), min_transparent=250):
#     w, h = picture.get_size()
#     transparent_color = Color((0, 0, 0, 0))
#
#     new_color = Color(normalize_color(color))
#     # min_r, min_g, min_b = min_colors
#
#     for x in range(w):
#         for y in range(h):
#             c_at = picture.get_at((x, y))
#             # print(c_at[:2])
#             if c_at == recolor_key:
#                 picture.set_at((x, y), transparent_color)
#             elif c_at[3] > min_transparent:
#                 picture.set_at((x, y), new_color)
#
#     return picture
