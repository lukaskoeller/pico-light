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
    light_color = (random.randint(252, 255), random.randint(0, 190), 0)
    light_variety = (0, random.randint(0, 50), 0)
    lights.append((i, light_color, light_variety))

def get_sin_color(idx, color, variety):
    return (math.sin(idx) * variety[0] + color[0], math.sin(idx) * variety[1] + color[1], math.sin(idx) * variety[2] + color[2])

iteration = 0

while True:
    try:
        for light in lights:
            idx, color, variety = light
            new_color = get_sin_color(iteration, color, variety)
            pixels.set_pixel(idx, new_color)
            pixels.show()
        iteration += 0.1
    except KeyboardInterrupt:
        pixels.clear()
        break