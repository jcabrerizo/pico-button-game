from time import sleep


class GameControl:

    TIMEOUT = 5
    TIMER_DELTA = 0.1

    def __init__(self, display_control, button_control) -> None:
        self._display_control = display_control
        self._button_control = button_control
        self.reset()

    def reset(self):
        self.correct_pressed_counter = -1  # first press is for starting
        self.incorrect_pressed_counter = 0
        self.button_time_counter = 0
        self.timeout_status = False
        self.reset_request = False
        self.all_released = True

    def timer(self):
        while True:
            if self.reset_request:
                self.reset()
                print("New game")
            else:
                if self.correct_pressed_counter == 0 and self.button_time_counter == 0:
                    print("Starting game")
                    self._display_control.time_and_score(
                        GameControl.TIMEOUT, 0)
                    self.target_button.on()
                if self.correct_pressed_counter >= 0:
                    self.button_time_counter += GameControl.TIMER_DELTA
                    self._display_control.time_and_score(
                        GameControl.TIMEOUT-self.button_time_counter, self.correct_pressed_counter)
                if self.button_time_counter >= GameControl.TIMEOUT:
                    print("Round timeout")
                    self.block_keys = True
                    percentage = self.correct_pressed_counter * 100 / \
                        (self.correct_pressed_counter + self.incorrect_pressed_counter) if (
                            self.correct_pressed_counter + self.incorrect_pressed_counter) > 0 else 0
                    print(f"{self.correct_pressed_counter} | {
                        self.incorrect_pressed_counter} -> {percentage}%")
                    # show next round time and current round points
                    self._display_control.time_and_score(
                        GameControl.TIMEOUT, self.correct_pressed_counter)
                    self._display_control.print_line(
                        f"{percentage}%", 5, show_immediately=False)
                    self._display_control.print_line(f"x {self.incorrect_pressed_counter}", 6)
                    self.reset()
                    self.block_keys = False
                sleep(GameControl.TIMER_DELTA)

    def game_loop(self):
        pressed_buttons = self._button_control.get_pressed()
        if len(pressed_buttons) == 0:
            self.all_released = True
        else:
            if len(pressed_buttons) > 1:
                print(f"Too many buttons {len(pressed_buttons)}")
            # TODO: add reset control
            else:
                pressed = pressed_buttons[0]
                if self.all_released: # ignore buttons until all button released has been detected
                    self.all_released = False
                    if self.is_correct_press(pressed):
                        print(f"+ {pressed.name}")
                        self.correct_press()
                    else:
                        print(f"- {pressed.name}")
                        self.incorrect_press()

    def is_correct_press(self, pressed_button) -> bool:
        return self.target_button == pressed_button

    def correct_press(self) -> None:
        self.correct_pressed_counter += 1
        self.target_button = self._button_control.switch_random_led()

    def incorrect_press(self) -> None:
        self.incorrect_pressed_counter += 1
