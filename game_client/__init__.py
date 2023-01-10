import os
if os.environ.get('VisualPygameOn', 'off') == 'on':
    from game_client.game_body import GameBody
