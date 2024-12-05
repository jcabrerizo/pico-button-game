from game.status import GameStatus
from .ssd1306 import SSD1306_I2C
from machine import Pin, I2C

LINE_HEIGHT_PIXELS = 8
LINE_WIDTH_CHAR = 16

SCREEN_WIDTH_PIXELS = 128
SCREEN_HEIGHT_PIXELS = 64


class DisplayController:

    def __init__(self, id=1, sda_pin=14, scl_pin=15) -> None:
        # For the default values, the address is 60/0x3c
        self._i2c = I2C(
            id=id,
            sda=Pin(sda_pin),
            scl=Pin(scl_pin),
            freq=400_000
        )
        # 0.96 inch oled IIC Serial White OLED Display Module 128X64
        # 16 char x 8 lines (2 yellow and 6 blue)
        self._display = SSD1306_I2C(128, 64, self._i2c)

    def print_line(self, msg, line_num, center=False, show_immediately=True, clear=True):
        if clear:
            self.clear_line(line_num, False)
        y = (line_num-1)*LINE_HEIGHT_PIXELS
        self._display.text(msg.center(LINE_WIDTH_CHAR)
                           if center else msg, 0, y)
        if show_immediately:
            self._display.show()

    def print_devices_info(self):
        devices = self._i2c.scan()
        if len(devices) == 0:
            print("No I2C devices !")
        else:
            print('I2C devices found:', len(devices))
        for device in devices:
            print("Address: ", device, "(", hex(device), ")")

    def show(self):
        self._display.show()

    def clear_all(self):
        self._display.fill(0)
        self._display.show()

    def clear_line(self, line, immediate_show=True):
        self._display.rect(0, (line-1) * LINE_HEIGHT_PIXELS, SCREEN_WIDTH_PIXELS,
                           LINE_HEIGHT_PIXELS, 0, True)
        if immediate_show:
            self._display.show()

    def clear_top(self):
        self._display.rect(0, 0, SCREEN_WIDTH_PIXELS,
                           LINE_HEIGHT_PIXELS * 2, 0, True)
        self._display.show()

    def clear_bottom(self):
        self._display.rect(0, LINE_HEIGHT_PIXELS * 2, SCREEN_WIDTH_PIXELS,
                           LINE_HEIGHT_PIXELS * 6, 0, True)
        self._display.show()

    def time_and_score(self, time, score):
        self.print_line(f"Time: {time:.1f}", 1,
                        center=True, show_immediately=False)
        self.print_line(f"{score}", 2, center=True, show_immediately=False)
        self.show()

    def welcome(self, game_status: GameStatus):
        self.print_line(
            f'Time: {game_status.game_duration:.1f}', 1, True)

    def update_target_button(self, button_name):
        self.print_line(f"> {button_name} <", 8, True)

    def start_game(self, game_status: GameStatus):
        self.clear_line(5, False)
        self.clear_line(6, False)
        self.update_status(game_status)

    def update_status(self, game_status: GameStatus):
        self._display.invert(False)
        self.time_and_score(game_status.get_remaining_time(),
                            game_status.get_correct_counter())

    def show_round_results(self, game_status: GameStatus):
        self._display.invert(True)
        self.time_and_score(
            game_status.game_duration, game_status.get_correct_counter())
        self.print_line(
            f"{game_status.get_correct_percentage():.1f}%", 5, show_immediately=False)
        self.print_line(f"x {game_status.get_incorrect_counter()}", 6)

    def game_over(self):
        self.clear_all()
        self._display.invert(True)
        self.print_line('GAME OVER', 4, center=True)
        print("-GAME OVER-")
