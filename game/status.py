class GameStatus:

    def __init__(self, game_duration:float) -> None:
        self.game_duration = game_duration

    def reset(self):
        self.correct_pressed_counter = -1  # first press is for starting
        self.incorrect_pressed_counter = 0
        self.bait_pressed_counter = 0
        self.button_time_counter = 0

    def correct_press(self) -> None:
        self.correct_pressed_counter += 1

    def incorrect_press(self) -> None:
        self.incorrect_pressed_counter += 1

    def swallow_bait(self) -> None:
        self.bait_pressed_counter += 1

    def get_remaining_time(self) -> float:
        return self.game_duration - self.button_time_counter
    def is_starting_new_game(self) -> bool:
        return self.correct_pressed_counter == 0 and self.button_time_counter == 0

    def is_started(self) -> bool:
        return self.correct_pressed_counter >= 0

    def timeout_reached(self) -> bool:
        return self.button_time_counter >= self.game_duration

    def step_timer(self, delta) -> None:
        self.button_time_counter += delta

    def get_correct_counter(self) -> int:
        return self.correct_pressed_counter

    def get_incorrect_counter(self) -> int:
        return self.incorrect_pressed_counter

    def get_correct_percentage(self) -> float:
        return self.correct_pressed_counter * 100 / \
            (self.correct_pressed_counter + self.incorrect_pressed_counter) if (
                self.correct_pressed_counter + self.incorrect_pressed_counter) > 0 else 0
