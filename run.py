from button import ButtonControl
from button import Button
from game import GameControl
from machine import Pin, Timer
from utime import sleep
import _thread
from display import DisplayController
board_led = Pin("LED", Pin.OUT)

display_ctr = DisplayController()

BLUE = Button("BLUE", led_pin=22, button_pin=11)
RED = Button("RED", led_pin=28, button_pin=5)

buttons = (BLUE, RED)

button_ctr = ButtonControl(buttons)
game = GameControl(
    button_control=button_ctr,
    display_control=display_ctr
)

board_led_blinker = Timer(period=1000, mode=Timer.PERIODIC,
                          callback=lambda t: board_led.toggle())

timer_thread = _thread.start_new_thread(game.timer, ())

while True:
    try:
        game.game_loop()
        sleep(0.1)
    except KeyboardInterrupt:
        break

board_led_blinker.deinit()
board_led.off()
display_ctr.clear_all()
display_ctr.print_line('GAME OVER', 4, center=True)
print("-GAME OVER-")
# todo loop though the buttons
button_ctr.turn_all_off()
