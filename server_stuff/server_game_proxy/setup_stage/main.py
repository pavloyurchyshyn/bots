from global_obj.main import Global
from server_stuff.constants.stages import ServerStages
from server_stuff.constants.requests import SetupStageReq as SSR
from server_stuff.abs.server import ServerAbc

from server_stuff.player_client import Client
from server_stuff.constants.requests import CommonReqConst
from game_logic.settings_stage import SettingsStage


class GameSetup:

    def __init__(self, server_game_proxy, server):
        self.actions = {
            CommonReqConst.Chat: self.chat,
            SSR.Player.ChooseMap: self.choose_map,
            SSR.SelectSlot: self.select_slot,
            SSR.SetBot: self.set_bot,
            SSR.DeselectSlot: self.deselect_slot,
            SSR.Player.StartMatch: self.start_match,
            SSR.Player.NewNickname: self.update_nickname,
            CommonReqConst.KickPlayer: self.kick_player,
        }
        self.server: ServerAbc = server
        self.server_game_proxy = server_game_proxy
        self.game_logic: SettingsStage = SettingsStage()

    def update(self):
        pass

    def set_bot(self, request: dict, client: Client, **kwargs):
        if client.is_admin:
            slot = request[SSR.SetBot]
            self.game_logic.set_slot(slot, self.game_logic.BOT_TOKEN)
            self.server.send_player_slots()
        else:
            Global.logger.warning(f'Non admin({client}) trying to set bot for slot')

    def process_request(self, request: dict, client: Client):
        for action, data in request.items():
            self.actions.get(action, self.bad_action)(action=action,
                                                      request=request,
                                                      client=client,
                                                      player_obj=None)

    def bad_action(self, action: str, client: Client, **kwargs):
        Global.logger.warning(f'Bad request from {client.token} with action "{action}"')

    def connect(self, response: dict, client: Client):
        response[SSR.Maps] = [save.get_save_dict() for save in self.game_logic.maps_mngr.maps if save]
        response[SSR.Server.ChosenMap] = self.game_logic.chosen_map
        response[ServerStages.SERVER_STAGE] = ServerStages.GameSetup

    def choose_map(self, request: dict, client: Client, **kwargs):
        Global.logger.info(f'{client} changing map.')
        if client.is_admin:
            map__ = map_ = request.get(SSR.Player.ChooseMap, 0)
            try:
                map_ = int(map_)
            except Exception as e:
                Global.logger.error(f'Wrong map format {map__}. Error {e}')
                return
            if map_ == self.game_logic.chosen_map:
                Global.logger.info(f'This map already chosen')
                return
            if map_ + 1 > len(self.game_logic.maps_mngr.maps):
                Global.logger.warning(f'Player {client} asking for bad map id {map_}')
                return

            # TODO check for maps count
            Global.logger.info(f'{client} changing map to {map_}')

            self.game_logic.chosen_map = map_
            self.game_logic.current_map = self.game_logic.maps_mngr.maps[self.game_logic.chosen_map]
            self.game_logic.recreate_slots()
            self.server.sync_broadcast({SSR.Server.ChosenMap: map_})
            self.server.send_player_slots()
            Global.logger.debug(f'Chosen map {map_}')
        else:
            Global.logger.debug(f'Player {client} is not admin and not allowed to change map!')

    def start_match(self, request: dict, client: Client, **kwargs):
        if client.is_admin:
            if request[SSR.Player.StartMatch] and not self.server_game_proxy.started_match:
                Global.logger.info(f'Game data: {request}')
                # self.game_logic.set_real_players(
                #     len([i for i in self.game_logic.players_slots.values() if type(i) == BotPlayer]))
                # self.game_logic.set_players_num(len([i for i in self.game_logic.players_slots.values() if i]))
                self.server_game_proxy.start_game_match()

        else:
            Global.logger.warning(f'Non admin {client} asking for start')

    def chat(self, request: dict, client: Client, **kwargs):
        msg = request.get(CommonReqConst.Chat, '')
        Global.logger.info(f'{client} send a message {msg}')
        if msg:
            self.server.sync_broadcast({CommonReqConst.Chat: f'{client.nickname}: {msg}'})

    def kick_player(self, request: dict, client: Client, **kwargs):
        Global.logger.debug(f'Kick request from {client.token}(admin={client.is_admin}).')
        if client.is_admin:
            kick_token = request[CommonReqConst.KickPlayer]
            if kick_token in self.server.alive_connections:
                client_to_kick = self.server.alive_connections.pop(kick_token)
                Global.logger.info(f'Kicking {client_to_kick}')
                self.server.sync_send_to_client(client_to_kick,
                                                data={CommonReqConst.Disconnect: 'Kicked'})  # TODO replace by message
                self.server.sync_disconnect_client(client_to_kick)
                self.server.send_updated_connection_list()
            else:
                self.server.send_to_client(client, {CommonReqConst.Error: 'Unknown token'})

    def deselect_slot(self, request: dict, client: Client, **kwargs):
        slot = request[SSR.DeselectSlot]
        try:
            slot = int(slot)
        except ValueError:
            Global.logger.warning(f'Wrong slot number format {slot}')
            return

        if slot in self.game_logic.players_slots and not self.game_logic.slot_is_free(slot):
            player_own_slot = slot == client.slot
            if client.is_admin or (self.game_logic.get_slot(slot) is not None and player_own_slot):
                self.game_logic.players_slots[slot] = None
                Global.logger.info(f'{slot} slot now is free.')
                self.server.send_player_slots()
                self.server.sync_send_to_client(client, {CommonReqConst.SendSlotToPlayer: client.slot})

    def select_slot(self, request: dict, client: Client, **kwargs):
        slot = request[SSR.SelectSlot]
        try:
            slot = int(slot)
        except ValueError:
            Global.logger.warning(f'Wrong slot number format {slot}')
            return

        if slot in self.game_logic.players_slots and self.game_logic.slot_is_free(slot):
            if client.slot is not None and client.slot in self.game_logic.players_slots:
                self.game_logic.free_slot(client.slot)

            client.slot = None
            self.game_logic.set_slot(slot, client.token)
            client.slot = slot
            Global.logger.info(f'Slot {slot} chosen by {client}')
            self.server.send_player_slots()
            self.server.sync_send_to_client(client, {CommonReqConst.SendSlotToPlayer: client.slot})

    def update_nickname(self, request: dict, client: Client, **kwargs):
        nickname = request[SSR.Player.NewNickname]
        if nickname:
            old = client.nickname
            client.nickname = nickname
            Global.logger.info(f'Player {client.token} changed nickname from {old} to {nickname}')
            self.server.send_player_slots()
            self.server.send_updated_connection_list()
