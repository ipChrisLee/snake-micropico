from machine import Pin, enable_irq, disable_irq
from led import RgbLed
from utime import sleep, sleep_ms, sleep_us

restartButton = Pin(13, Pin.IN)  # press=>0 release=>1
rgb = RgbLed(10, 11, 12)

cnt = 0


def cb(pin: Pin):
    global cnt
    cnt = cnt + 1
    print(f"Handle {cnt}")
    rgb.set_rgb(0, 255, 0)


restartButton.irq(handler=cb, trigger=Pin.IRQ_FALLING)  # hard=True?

print("Start")
rgb.set_rgb(0, 0, 255)
sleep_ms(1000)

while True:
    try:
        # irqState = disable_irq()
        # rgb.set_rgb(255, 0, 0)
        # sleep_ms(1000)
        # rgb.set_rgb(0, 255, 0)
        # sleep_ms(1000)
        # if cnt == 10:
        #     break
        # enable_irq(irqState)
        # sleep_ms(1000)
        sleep(2)
        rgb.set_rgb(255, 0, 0)
    except KeyboardInterrupt:
        break

print("End")
