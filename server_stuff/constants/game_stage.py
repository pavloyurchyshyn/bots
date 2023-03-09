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
