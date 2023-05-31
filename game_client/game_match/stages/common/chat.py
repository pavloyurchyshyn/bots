from visual.UI.chat import Chat
from global_obj.main import Global
from visual.UI.base.button import Button
from visual.UI.base.input import InputBase
from server_stuff.constants.requests import CommonReqConst


class ChatPart:
    def __init__(self,
                 x_k=0.425, y_k=0.65, h_size_k=0.25, v_size_k=0.3,
                 inp_x_k=0.425, inp_y_k=0.95, inp_h_size_k=0.23, inp_v_size_k=0.05,
                 send_x_k=0.655, send_y_k=0.95, send_h_size_k=0.02, send_v_size_k=0.05,
                 ):
        self.chat = Chat('chat', x_k=x_k, y_k=y_k, h_size_k=h_size_k, v_size_k=v_size_k, parent=self).build()
        self.send_btn = Button('send_btn', '->',
                               x_k=send_x_k, y_k=send_y_k,
                               h_size_k=send_h_size_k, v_size_k=send_v_size_k,
                               on_click_action=self.send,
                               )
        self.input = InputBase('chat_input',
                               x_k=inp_x_k, y_k=inp_y_k,
                               h_size_k=inp_h_size_k, v_size_k=inp_v_size_k,
                               on_enter_action=self.send,
                               )

    def update_chat(self):
        if self.chat.collide_point(Global.mouse.pos):
            if Global.mouse.scroll:
                self.chat.change_dx(Global.mouse.scroll)

        self.chat.draw()
        self.upd_draw_input()
        if self.send_btn.collide_point(Global.mouse.pos):
            self.draw_border_around_element(self.send_btn)
            if Global.mouse.l_up:
                self.send_btn.do_action()
        self.send_btn.draw()

    def send(self, b: Button = None):
        if self.input.text.str_text:
            Global.connection.send_json({CommonReqConst.Chat: self.input.text.str_text})
            self.input.change_text('')

    def upd_draw_input(self):
        self.input.draw()
        self.input.update()

        if self.input.input_is_active and Global.keyboard.ESC:
            self.input.unfocus()

        elif Global.keyboard.activate_input:
            self.input.focus()

        elif self.input.collide_point(Global.mouse.pos):
            self.draw_border_around_element(self.input)
            if Global.mouse.l_up:
                self.input.focus()

        elif Global.mouse.l_up:
            self.input.unfocus()
