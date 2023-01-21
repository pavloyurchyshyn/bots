class SetupStgConst:
    CurrentSave = 'current_save'
    Maps = 'maps'

    class Player:
        ChooseMap = 'choose_map'
        Ready = 'ready'
        StartMatch = 'start_match'

    class Server:
        ChosenMap = 'chosen_map'
        Disconnect = 'disconnect'
        StartMatch = 'start_match'
        ServerMsg = 'server_msg'

        class MatchArgs:
            Map = 'map'
