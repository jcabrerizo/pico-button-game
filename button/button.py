from machine import Pin


class Button:
    def __init__(self, name, button_pin, led_pin) -> None:
        self._button_pin = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
        self._led_pin = Pin(led_pin, Pin.OUT)
        self._is_correct=False
        self.name= name
        self.off()  # default off

    def is_pressed(self) -> bool:
        return self._button_pin.value() == 1

    def on(self) -> None:
        self._led_pin.value(1)

    def off(self) -> None:
        self._led_pin.value(0)

    def toggle(self) -> None:
        self._led_pin.toggle()

    