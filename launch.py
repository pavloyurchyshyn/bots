from os import environ
environ['VisualPygameOn'] = 'on'
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

from time import time

import pygame.image
from pygame import init
init()
from pygame import display, event as EVENT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN, TEXTINPUT
from pygame.time import Clock

display.set_icon(pygame.image.load('game.ico'))
from global_obj.main import Global
from visual.UI.constants.colors import WHITE
from global_obj.display import MAIN_DISPLAY
from visual.UI.base.font import DEFAULT_FONT
from settings.common import get_fps


class GameRunner:
    def __init__(self, game_body=None):
        if game_body:
            self.game_body = game_body
        else:
            from game_client.game_body import GameBody

            self.game_body = GameBody(self)

        self.main_screen = MAIN_DISPLAY
        self.font = DEFAULT_FONT

        self.draw_max_fps = self.draw_max_fps()
        self.draw_avg_fps = self.draw_avg_fps()
        self.draw_min_fps = self.draw_min_fps()

    def run(self):
        pygame_clock = Clock()

        display.update()

        global_clock = Global.clock
        global_mouse = Global.mouse
        global_keyboard = Global.keyboard

        GAME_BODY = self.game_body
        start = time()

        while 1:
            events = EVENT.get()
            finish = time()

            pygame_clock.tick(get_fps())
            dt = finish - start
            start = finish
            # update time
            global_clock.update(dt)
            Global.round_clock.update(dt)

            global_mouse.update()
            global_keyboard.update()
            # scroll up and scroll down update
            for event in events:
                self.check_for_mouse_event(event)
                self.check_for_keyboard_event(event)

            GAME_BODY.game_loop()

            fps = pygame_clock.get_fps()
            self.draw_fps(fps)
            self.draw_max_fps(fps, dt)
            self.draw_avg_fps(fps, dt)
            self.draw_min_fps(fps, dt)

            # global_mouse.test()
            # Global.keyboard.test()
            if global_keyboard.alt_and_f4:
                self.close_game()

            display.update()

    @staticmethod
    def check_for_mouse_event(event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                Global.mouse.l_down = 1

            elif event.button == 3:
                Global.mouse.r_down = 1

            elif event.button == 4:
                Global.mouse.scroll = 1

            elif event.button == 5:
                Global.mouse.scroll = -1

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                Global.mouse.l_up = 1
            elif event.button == 3:
                Global.mouse.r_up = 1

    @staticmethod
    def check_for_keyboard_event(event):
        if event.type == KEYDOWN:
            Global.keyboard.process_event(event)
            # self.add_command(event)

        # elif event.type == KEYUP:
        #     self.delete_command(event)
        #     self.check_for_special_keys(event)
        elif event.type == TEXTINPUT:
            Global.keyboard.text.append(event.text)

    def draw_fps(self, fps):
        fps_text = self.font.render(str(int(fps)), 1, WHITE, (0, 0, 0))
        self.main_screen.blit(fps_text, (0, 0))

    def draw_max_fps(self):
        data = {'i': 0, 'max': '0'}

        def calc(fps, dt):
            if data['i'] > 3:
                data['i'] = 0
                data['max'] = '0'
            data['i'] += dt
            if int(data['max']) < fps:
                data['max'] = str(int(fps))
            fps_text = self.font.render(f"Max:{data['max']}", 1, WHITE, (0, 0, 0))
            self.main_screen.blit(fps_text, (0, 30))

        return calc

    def draw_min_fps(self):
        data = {'i': 0, 'min': '999999'}

        def calc(fps, dt):
            if data['i'] > 3:
                data['i'] = 0
                data['min'] = '999999'
            data['i'] += dt
            if int(data['min']) > fps:
                data['min'] = str(int(fps))
            fps_text = self.font.render(f"Min:{data['min']}", 1, WHITE, (0, 0, 0))
            self.main_screen.blit(fps_text, (0, 120))

        return calc

    def draw_avg_fps(self):
        data = {'i': 0, 'avg': [], 'all_avg': []}

        def calc(fps, dt):
            if data['i'] > 5:
                data['i'] = 0
                data['avg'].clear()
            data['i'] += dt
            data['avg'].append(fps)
            data['all_avg'].append(fps)
            avg = sum(data['avg']) // len(data['avg'])
            fps_text = self.font.render(f"AVG:{str(avg)}", 1, WHITE, (0, 0, 0))
            self.main_screen.blit(fps_text, (0, 60))

            avg = sum(data['all_avg']) // len(data['all_avg'])
            fps_text = self.font.render(f"ALL AVG:{str(avg)}", 1, WHITE, (0, 0, 0))
            self.main_screen.blit(fps_text, (0, 90))

        return calc

    def close_game(self):
        from pygame import quit as close_program_pygame
        import sys

        close_program_pygame()
        sys.exit()


if __name__ == '__main__':
    try:
        game = GameRunner()
        game.run()
    except KeyboardInterrupt:
        try:
            game.game_body.close_game()
        except Exception as e:
            print(e)
        exit(1)
