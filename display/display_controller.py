from .ssd1306 import SSD1306_I2C
from machine import Pin, I2C

LINE_HEIGHT = 8
LINE_WIDTH = 8

WIDTH_PIXELS = 128


class DisplayController:

    def __init__(self, id=1, sda_pin=14, scl_pin=15) -> None:
        # For the default values, the address is 60/0x3c
        self._i2c = I2C(
            id=id,
            sda=Pin(sda_pin),
            scl=Pin(scl_pin),
            freq=400000
        )
        # 0.96 inch oled IIC Serial White OLED Display Module 128X64
        # 16 char x 8 lines (2 yellow and 6 blue)
        self._display = SSD1306_I2C(128, 64, self._i2c)

    def print_line(self, msg, line_num, center=False, show_immediately=True, clear = True):
        if clear:
            self.clear_line(line_num, False)
        x = 0
        y = (line_num-1)*LINE_HEIGHT
        # print(f'print line {msg} - {x} , {y}') 
        self._display.text(msg, x, y)
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
        self._display.rect(0, (line-1)*LINE_HEIGHT, WIDTH_PIXELS,
                           LINE_HEIGHT, 0, True)
        if immediate_show:
            self._display.show()

    def clear_top(self):
        self._display.rect(0, 0, WIDTH_PIXELS, LINE_HEIGHT * 2, 0, True)
        self._display.show()

    def clear_bottom(self):
        self._display.rect(0, LINE_HEIGHT * 2, WIDTH_PIXELS,
                           LINE_HEIGHT * 6, 0, True)
        self._display.show()

    def time_and_score(self, time, score):
        self.clear_bottom()
        self.print_line(f"T: {time}", 3, show_immediately=False)
        self.print_line(f"S: {score}", 4, show_immediately=False)
        self.show()
