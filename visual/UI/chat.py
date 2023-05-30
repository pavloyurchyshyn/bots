from visual.UI.base.text import Text
from visual.UI.base.container import Container


class Chat(Container):
    def __init__(self, uid, x_k, y_k,
                 h_size_k, v_size_k,
                 text_kwargs: dict = None,
                 **kwargs):
        super(Chat, self).__init__(uid=uid, x_k=x_k, y_k=y_k,
                                   h_size_k=h_size_k, v_size_k=v_size_k,
                                   **kwargs)
        self.text_kwargs: dict = text_kwargs if text_kwargs else {}

    def add_msg(self, msg: str, text_kwargs: dict = None, raw_text: bool = True, capitalize: bool = True):
        if text_kwargs:
            uid = text_kwargs.pop('uid', f'{len(self.elements)}_msg')
        else:
            uid = f'{len(self.elements)}_msg'
        text_kwargs = text_kwargs if text_kwargs else self.text_kwargs
        self.add_element(Text(uid=uid, text=msg,
                              raw_text=raw_text,
                              unlimited_v_size=True,
                              split_lines=True,
                              h_size_k=0.98,
                              parent=self,
                              from_left=True,
                              capitalize=capitalize,
                              **text_kwargs
                              ))

