import machine
import utime
led_red = machine.Pin(15, machine.Pin.OUT)

while True:
    for i in range(10):
        led_red.toggle()
        utime.sleep(0.1)
    led_red.value(0)
    utime.sleep(2)