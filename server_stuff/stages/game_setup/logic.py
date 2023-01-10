from global_obj import Global
from server_stuff.stages.abs import LogicStageAbs
from server_stuff.constants.stages import ServerStages
from game_client.server_interactions.network.connection_wrapper import ConnectionWrapperAbs


class GameSetup(LogicStageAbs):

    def __init__(self, game_server, server):
        super().__init__(game_server, server)

    def update(self):
        pass

    def process_request(self, request: dict, connection: ConnectionWrapperAbs):
        response = {'ok': 'process_request ok'}
        Global.logger.info(f'Response to {connection.token}: {response}')
        connection.send_json(response)

    def connect(self, response: dict, connection: ConnectionWrapperAbs):
        response['ok'] = 'ok'
        response[ServerStages.SERVER_STAGE] = ServerStages.GameSetup
