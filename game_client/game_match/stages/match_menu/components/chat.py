from game_client.game_match.stages.common.chat import ChatPart
from game_client.game_match.stages.match_menu.settings.windows_sizes import ChatSize


class ChatC(ChatPart):
    def __init__(self):
        super(ChatC, self).__init__(
            x_k=ChatSize.x_k, y_k=ChatSize.y_k,
            h_size_k=ChatSize.h_size_k, v_size_k=ChatSize.v_size_k,

            inp_x_k=ChatSize.inp_x_k, inp_y_k=ChatSize.inp_y_k,
            inp_h_size_k=ChatSize.inp_h_size_k, inp_v_size_k=ChatSize.inp_v_size_k,

            send_x_k=ChatSize.send_x_k, send_y_k=ChatSize.send_y_k,
            send_h_size_k=ChatSize.send_h_size_k, send_v_size_k=ChatSize.send_v_size_k,
        )
