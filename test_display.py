from time import sleep
from display import DisplayController

def line(line_num):
    y = (line_num-1) * 8
    print(f"y:{y}")
    return y

STR = "String"
SLEEP_STEP = 0.2
t = DisplayController()

t._display.text(STR + "1", 0, line(1), 1)
t._display.text(STR + "2", 0, line(2), 1)
t._display.text(STR + "3", 0, line(3), 1)
t._display.text(STR + "4", 0, line(4), 1)
t._display.text(STR + "5", 0, line(5), 1)
t._display.text(STR + "6", 0, line(6), 1)
t._display.text(STR + "7", 0, line(7), 1)
t._display.text(STR + "8", 0, line(8), 1)
t._display.text(STR + "9", 0, line(9), 1)
t._display.show()
sleep(SLEEP_STEP)

t.clear_line(2)
sleep(SLEEP_STEP)

t.clear_line(4)
sleep(SLEEP_STEP)

t.clear_line(5)
sleep(SLEEP_STEP)

t._display.text(STR + "4", 0, line(4), 1)
sleep(SLEEP_STEP)

t._display.text(STR + "5", 0, line(5), 1)
sleep(SLEEP_STEP)

t._display.text(STR + "6", 0, line(6), 1)
sleep(SLEEP_STEP)

t.clear_line(5)
sleep(SLEEP_STEP)

t._display.text(STR + "4", 0, line(4), 1)
sleep(SLEEP_STEP)
