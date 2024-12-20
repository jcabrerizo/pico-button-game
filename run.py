from io import IoControl
from io import Button
from game import GameControl
from machine import Pin, Timer, reset
from utime import sleep
from display import DisplayController

board_led = Pin("LED", Pin.OUT)

display_ctr = DisplayController()

BLUE = Button("BLUE", led_pin=22, button_pin=8)
RED = Button("RED", led_pin=28, button_pin=5)
WHITE = Button("WHITE", led_pin=21, button_pin=11)

buttons = (BLUE, RED, WHITE)

io_ctr = IoControl(buttons, 26)
game_controller = GameControl(
    io_control=io_ctr,
    display_control=display_ctr
)

board_led_blinker = Timer(period=1000, mode=Timer.PERIODIC,
                          callback=lambda t: board_led.toggle())

while True:
    try:
        game_controller.game_loop()
        sleep(0.1)
    except KeyboardInterrupt:
        break

board_led_blinker.deinit()
board_led.off()
display_ctr.game_over()
io_ctr.turn_all_off()
reset()
