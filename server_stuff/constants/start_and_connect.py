class StartArgs:
    Port = '--port'
    DefaultPort = 8000
    Password = '--password'
    AdminToken = '--admin_token'


class LoginArgs:
    Solo = 'solo'
    Token = 'token'
    Password = 'password'
    Msg = 'msg'

    PlayerData = 'player_data'

    class ClientAttrs:
        ClientData = 'client_data'
        NickName = 'nickname'
        IsAdmin = 'is_admin'
        Number = 'player_number'

    class Result:
        Status = 'status'
        Connected = 'connected'
        BadPassword = 'bad_password'
        Prohibited: str = 'prohibited'
