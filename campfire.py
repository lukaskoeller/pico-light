from machine import Pin
from utime import sleep
from neopixel import Neopixel
import random
import math

num_pixels = 60

pin_led = Pin("LED", Pin.OUT)

pixels = Neopixel(num_pixels, 0, 0, "GRB")
# pixels.brightness = 0.5

lights = []
for i in range(num_pixels):
    amplitude = (
        random.randint(0, 10),  # red
        random.randint(0, 40),  # green
        0                       # blue
    )
    light_color = (
        max(0, (random.randint(252, 255) - amplitude[0])),  # red
        max(0, (random.randint(0, 100) - amplitude[1])),    # green
        max(0, (0 - amplitude[2]))                          # blue
    )
    iteration_start = random.choice([0, math.pi / 2])
    frequency = random.randint(1, 42)
    lights.append((i, light_color, amplitude, iteration_start, frequency))



def get_sin_color(idx, color, amplitude, iteration_start, frequency):
    return (
        max(0, math.sin(idx + iteration_start * frequency) * amplitude[0] + color[0]),
        max(0, math.sin(idx + iteration_start * frequency) * amplitude[1] + color[1]),
        max(0, math.sin(idx + iteration_start * frequency) * amplitude[2] + color[2])
    )

iteration = 0

while True:
    try:
        is_flashing = False
        turn_on_flash = random.random() > 0.8
        turn_off_flash = random.random() > 0.3
        if not is_flashing and turn_on_flash:
            is_flashing = True
        if is_flashing and turn_off_flash:
            is_flashing = False
        
        for light in lights:
            idx, color, amplitude, iteration_start, frequency = light
            new_color = get_sin_color(iteration, color, amplitude, iteration_start, frequency)
            pixels.set_pixel(idx, new_color)
            pixels.show()
        # if is_flashing:
        #     flash_length = 3
        #     flash_position = random.randint(0, num_pixels - 1 - flash_length)
        #     pixels.set_pixel_line_gradient(flash_position, flash_position + flash_length, (255, 50, 0), (255, 100, 0))
        iteration += 0.2
    except KeyboardInterrupt:
        pixels.clear()
        break