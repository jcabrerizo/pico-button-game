# not supported on MicroPython. TODO: check https://micropython-stubs.readthedocs.io/en/main/typing_mpy.html
# from typing import List
from button.button import Button
from machine import Pin
import random

class ButtonControl:
    def __init__(self, buttons: tuple[Button, ...]) -> None:
        self._buttons=buttons
    
    # def get_pressed(self) -> List[Button]:
    def get_pressed(self):
        pressed = []
        for b in self._buttons:
            if b.is_pressed():
                pressed.append(b)
        return pressed
    
    def switch_random_led(self):
        self.turn_all_off()
        new_button = self._buttons[random.randrange(0, len(self._buttons))]
        new_button.on()
        print(f'> {new_button.name}')
        return new_button

    def turn_all_off(self) -> None:
        for b in self._buttons:
            b.off()
