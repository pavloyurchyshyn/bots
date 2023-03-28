class CommonReqConst:
    Chat = 'chat'
    ServerMsg = 'server_msg'
    CurrentGameStage = 'current_game_stage'
    ConnectedPlayers = 'conn_players'
    PlayersSlots = 'players_slots'
    KickPlayer = 'kick_player'
    Disconnect = 'disconnect'
    Error = 'error'


class SetupStageReq:
    CurrentSave = 'current_save'
    Maps = 'maps'
    SelectSlot = 'select_slot'
    DeselectSlot = 'deselect_slot'

    class Player:
        ChooseMap = 'choose_map'
        Ready = 'ready'
        StartMatch = 'start_match'

    class Server:
        ChosenMap = 'chosen_map'
        Disconnect = 'disconnect'
        StartMatch = 'start_match'
        ServerMsg = 'server_msg'


class GameStgConst:
    MatchData = 'match_data'
    Time = 'time'
    ReadyPlayersNumber = 'ready_players_number'

    class MatchArgs:
        Map = 'map'
        DetailsPool = 'details_pool'
        PlayersData = 'players_data'

    class Server:
        UpdateMech = 'update_mech'

    class Player:
        ChooseMap = 'choose_map'
        ReadyStatus = 'ready_status'
        StartMatch = 'start_match'

    class SkillM:  # SkillManipulations
        SkillStats = 'skill_stats'
        SelectSkill = 'select_skill'
        UnknownSkill = 'unk_skill'
        ScenarioIsFull = 'scnr_is_full'

        LockSkill = 'lock_skill'

        UseSkill = 'use_skill'
        UseAttrs = 'use_attrs'
        SkillUID = 'skill_uid'
    # SyncPlayerData = 'sync_player_data'
