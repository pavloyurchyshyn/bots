from global_obj.main import Global
from visual.UI.base.text import Text
from visual.UI.constants.colors import simple_colors


class Timer(Text):
    emergency_time = -20

    def __init__(self, uid, x_k, y_k, h_size_k, v_size_k, **kwargs):
        super(Timer, self).__init__(uid=uid,
                                    text='00:00',
                                    x_k=x_k, y_k=y_k,
                                    h_size_k=h_size_k, v_size_k=v_size_k,
                                    **kwargs)

    def update(self):
        self.change_text(Global.real_time_clock.str_time)
        if Global.real_time_clock.time > self.emergency_time:
            self.change_color(simple_colors.red)
        else:
            self.change_color(simple_colors.white)
