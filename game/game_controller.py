from .status import GameStatus
from time import sleep


class GameControl:

    GAME_DURATION = 5.0
    TIMER_DELTA = 0.1
    BAITS = 1

    def __init__(self, display_control, button_control) -> None:
        self._display_control = display_control
        self._button_control = button_control
        self._game = GameStatus(GameControl.GAME_DURATION)
        self.reset()

    def reset(self):
        self._game.reset()
        self.reset_request = False
        self.block_keys = False
        self.all_released = True
        
        self._display_control.welcome(self._game)
        self.turn_on_leds()

    def timer_control(self):
        """ Method running in an independent thread to control the game time"""
        if self.reset_request:
            self.reset()
            print("New game")
        else:
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
        pressed_buttons = self._button_control.get_pressed()
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

    def turn_on_leds(self)-> None:
        self.target_button = self._button_control.switch_random_led()
        self._display_control.update_target_button(self.target_button.name)
        self.bait_leds = self._button_control.get_baits(
            self.target_button, GameControl.BAITS)

    def correct_press(self) -> None:
        self._game.correct_press()
        self.turn_on_leds()

    def incorrect_press(self) -> None:
        self._game.incorrect_press()

    def swallow_bait(self) -> None:
        self._game.swallow_bait()
