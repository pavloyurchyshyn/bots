class CommonReqConst:
    Chat = 'chat'
    ServerMsg = 'server_msg'
    CurrentGameStage = 'current_game_stage'
    ConnectedPlayers = 'conn_players'
    PlayersSlots = 'players_slots'
    KickPlayer = 'kick_player'
    Disconnect = 'disconnect'
    Error = 'error'

    SendSlotToPlayer = 'your_slot'

    InfoPopUp = 'info_pop_up'


class SetupStageReq:
    CurrentSave = 'current_save'
    Maps = 'maps'
    SelectSlot = 'select_slot'
    DeselectSlot = 'deselect_slot'

    SetBot = 'set_bot'

    class Player:
        ChooseMap = 'choose_map'
        Ready = 'ready'
        StartMatch = 'start_match'
        NewNickname = 'new_nickname'

    class Server:
        ChosenMap = 'chosen_map'
        Disconnect = 'disconnect'
        StartMatch = 'start_match'
        ServerMsg = 'server_msg'


class GameStgConst:
    MatchData = 'match_data'
    Time = 'time'
    ReadyPlayersNumber = 'ready_players_number'

    Map = 'map'
    DetailsPool = 'details_pool'
    PlayersData = 'players_data'

    Settings = 'game_settings'

    class ToPlayer:
        UpdateMech = 'update_mech'
        DeleteDetailFromPool = 'delete_detail_from_pool'

    class Player:
        ReadyStatus = 'ready_status'
        Ready = 'ready'

    class SkillM:  # SkillManipulations
        ActionID = 'action_id'

        SkillStats = 'skill_stats'
        SelectSkill = 'select_skill'
        UnknownSkill = 'unk_skill'
        ScenarioIsFull = 'scnr_is_full'

        LockSkill = 'lock_skill'

        UseSkill = 'use_skill'
        InvalidUse = 'inv_use'
        UseAttrs = 'use_attrs'
        SkillUID = 'skill_uid'
        SkillValid = 'skill_valid'
        CancelSkillUse = 'cancel_skill_use'

        SkipCommand = 'skip_action'
        SetAction = 'set_action'
        SetActions = 'set_actions'

    # SyncPlayerData = 'sync_player_data'
