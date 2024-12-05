import machine
import time

potentiometer = machine.ADC(26)
conversion_factor = 3.3 / (65535)


def map_value(value, in_min, in_max, out_min, out_max, step):
    mapped = (value - in_min) * (out_max - out_min) / \
        (in_max - in_min) + out_min
    return int(round(mapped / step) * step)


min_val = 5
max_val = 60

prev_mapped_value = -1
changes = 0
while True:
    voltage = potentiometer.read_u16() * conversion_factor
    mapped_value = map_value(voltage, 0.0001, 3.3, min_val, max_val, 5)
    if prev_mapped_value != mapped_value:
        changes += 1
        prev_mapped_value=mapped_value
        print(f"{changes} - {voltage}->{mapped_value}")

    time.sleep(0.1)
