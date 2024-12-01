# not supported on MicroPython. TODO: check https://micropython-stubs.readthedocs.io/en/main/typing_mpy.html
# from typing import List
from button.button import Button
from machine import Pin
import random


class ButtonControl:
    def __init__(self, buttons: tuple[Button, ...]) -> None:
        self._buttons = buttons

    # def get_pressed(self) -> List[Button]:
    def get_pressed(self):
        pressed = []
        for b in self._buttons:
            if b.is_pressed():
                pressed.append(b)
        return pressed

    def getRandomButton(self):
        return self._buttons[random.randrange(0, len(self._buttons))]

    def switch_random_led(self):
        self.turn_all_off()
        new_button = self.getRandomButton()
        new_button.on()
        print(f'> {new_button.name}')
        return new_button

    def get_baits(self, target_button, num_baits):
        if len(self._buttons) -1 < num_baits:
            raise Exception(f"not enough buttons ({ len(self._buttons)}) for generate {num_baits} baits")
        baits = []
        while len(baits) < num_baits:
            random_button = self.getRandomButton()
            if target_button != random_button and random_button not in baits:
                random_button.on()
                baits.append(random_button)
        print(f'>< {baits}')

        return baits        

    def turn_all_off(self) -> None:
        for b in self._buttons:
            b.off()
