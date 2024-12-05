from io.io_controller import IoControl
from display.display_controller import DisplayController
from .status import GameStatus
from time import sleep


class GameControl:

    GAME_DURATION = 5.0
    GAME_DURATION_MIN = 5
    GAME_DURATION_MAX = 60
    GAME_DURATION_STEP = 5
    TIMER_DELTA = 0.1
    NUM_BAITS = 1

    def __init__(self, display_control: DisplayController, io_control: IoControl) -> None:
        self._display_control = display_control
        self._io_control = io_control
        self._game = GameStatus()
        self._game_time = self.get_time()
        self.reset()

    def reset(self, reset_leds=True):
        self._game.reset(self._game_time)
        self.reset_request = False
        self.block_keys = False
        self.all_released = True

        self._display_control.welcome(self._game)
        if reset_leds:
            self.turn_on_leds()

    def timer_control(self):
        """ Method running in an independent thread to control the game time"""
        if self.reset_request:
            self.reset()
            print("New game")
        else:
            if self._game.is_waiting_for_new_game():
                # Updating the time is only permitted when no game is currently in progress.
                new_time = self.get_time()
                if (new_time != self._game_time):
                    print(f"Updated game_time from {
                          self._game_time} to {new_time}")
                    self._game_time = new_time
                    self.reset(False)

            if self._game.is_starting_new_game():
                print("Starting game")
                self._display_control.start_game(self._game)
                self.target_button.on()

            if self._game.is_started():
                self._game.step_timer(GameControl.TIMER_DELTA)
                self._display_control.update_status(self._game)

            if self._game.timeout_reached():
                print("Round timeout")
                self.block_keys = True
                percentage = self._game.get_correct_percentage()
                print(f"{self._game.get_correct_counter()} | {
                    self._game.get_incorrect_counter()} -> {percentage}%")
                self._display_control.show_round_results(self._game)
                self.reset()
                self.block_keys = False

            sleep(GameControl.TIMER_DELTA)

    def game_loop(self) -> None:
        """ Method running in an infinite loop to handle the game events"""
        self.timer_control()
        pressed_buttons = self._io_control.get_pressed()
        if len(pressed_buttons) == 0:
            self.all_released = True
        else:
            if self.block_keys:
                return
            if len(pressed_buttons) > 1:
                print(f"Too many buttons {len(pressed_buttons)}")
            # TODO: add reset control
            else:
                pressed = pressed_buttons[0]
                if self.all_released:  # ignore buttons until all button released has been detected
                    self.all_released = False
                    if self.is_correct_press(pressed):
                        print(f"+ {pressed.name}")
                        self.correct_press()
                    elif pressed in self.bait_leds:
                        self.swallow_bait()
                    else:
                        print(f"- {pressed.name}")
                        self.incorrect_press()

    def is_correct_press(self, pressed_button) -> bool:
        return self.target_button == pressed_button

    def turn_on_leds(self) -> None:
        self.target_button = self._io_control.switch_random_led()
        self._display_control.update_target_button(self.target_button.name)
        self.bait_leds = self._io_control.get_baits(
            self.target_button, GameControl.NUM_BAITS)

    def correct_press(self) -> None:
        self._game.correct_press()
        self.turn_on_leds()

    def incorrect_press(self) -> None:
        self._game.incorrect_press()

    def swallow_bait(self) -> None:
        self._game.swallow_bait()

    def get_time(self):
        return self.calculate_time(self._io_control.get_time_selector_value())

    def calculate_time(self, input, in_min=0.001, in_max=3.3, out_min: int = GAME_DURATION_MIN, out_max: int = GAME_DURATION_MAX, step: int = GAME_DURATION_STEP) -> int:
        mapped_input = (input - in_min) * (out_max - out_min) / \
            (in_max - in_min) + out_min
        return int(round(mapped_input / step) * step)
