class StartArgs:
    Address = 'address'
    Port = 'port'
    DefaultPort = 8002
    RecvSize = 'recv_size'
    DefaultRecvSize = 2048

    Password = 'password'

    Solo = 'solo'
    DefaultSolo = True


class LoginArgs:
    Token = 'token'
    Password = 'password'
    Connected = 'connected'
    Msg = 'msg'
    BadPassword = 'bad_password'
    SuccLogin = 'succ_login'

# class ActionsToPlayer:
#     MessagesToAll = 'global_messages'
#     Disconnect = 'disconnect'
#     Message = 'message'
#     ReadyStatus = 'ready_status'
#
#     # SetAction = 'set_action'
#     # ActionPos = 'action_pos'
#     # CancelAction = 'cancel_action'
#     # DropAllActions = 'drop_all_actions'
#
#     PopUp = 'popup'
#     PopUpMsg = 'popup_msg'
