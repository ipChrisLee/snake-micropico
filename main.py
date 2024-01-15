from machine import Pin, ADC, PWM, I2C, enable_irq, disable_irq
from utime import sleep, sleep_ms, sleep_us
from led import RgbLed
from mpu6050_impl import MPU6050
from ssd1306_impl import SSD1306_I2C
from ds1302_impl import DS1302
import random


# hardwares
sysLed = Pin(25, Pin.OUT)
rgb = RgbLed(10, 11, 12)
mpu = MPU6050()
restartButton = Pin(13, Pin.IN)  # press=>0 release=>1
oled = SSD1306_I2C(128, 64, I2C(0, sda=Pin(0), scl=Pin(1), freq=400000))
knob = ADC(26)
timer = DS1302(Pin(2), Pin(3), Pin(4))
needRestart = True
random.seed(timer.Second() * timer.Minute() * 60 + timer.Hour() * 3600)


# prog info
ROW = 64
COL = 128
MXLEN = 64
INIT_LEN = 15
DIR_NONE = 0
DIR_L = 1
DIR_D = 2
DIR_U = 3
DIR_R = 4
DELTA_ROW = [0, 0, 1, -1, 0]
DELTA_COL = [0, -1, 0, 0, 1]


class Snake:
    # info class
    def __init__(self, row: int, col: int, prev, next) -> None:
        self.row = row
        self.col = col
        self.prev: Snake | None = prev
        self.next: Snake | None = next

    def pin(self, screen: SSD1306_I2C):
        screen.pixel(self.col, self.row, 1)

    def unpin(self, screen: SSD1306_I2C):
        screen.pixel(self.col, self.row, 0)

    def next_pos(self, dir: int):
        return (self.row + DELTA_ROW[dir], self.col + DELTA_COL[dir])

    def set_pos(self, row: int, col: int):
        self.row = row
        self.col = col


def pin(row, col):
    oled.pixel(col, row, 1)


def unpin(row, col):
    oled.pixel(col, row, 0)


def get_dir():
    g = mpu.readData()
    # print("X:{:.2f}  Y:{:.2f}  Z:{:.2f}".format(g.Gx, g.Gy, g.Gz))
    if g.Gx > 0.3:
        return DIR_U
    elif g.Gx < -0.3:
        return DIR_D
    elif g.Gy > 0.3:
        return DIR_L
    elif g.Gy < -0.3:
        return DIR_R
    else:
        return 0


# init
occur = None
dir = None
snakeLen = None
snakeHead = None
snakeTail = None
food = None


def game_init():
    global occur, dir, snakeLen, snakeHead, snakeTail, food
    irqState = disable_irq()
    occur = [[False for c in range(COL)] for r in range(ROW)]
    dir = DIR_NONE
    snakeLen = 0

    snakeHead = Snake(ROW//2, COL//2, None, None)
    snakeTail = snakeHead
    food = Snake(ROW//2, COL//3 * 2, None, None)
    # boarder
    oled.fill(0)
    for r in range(ROW):
        occur[r][0] = True
        occur[r][COL-1] = True
        pin(r, 0)
        pin(r, COL-1)
    for c in range(COL):
        occur[0][c] = True
        occur[ROW-1][c] = True
        pin(0, c)
        pin(ROW-1, c)

    # snake init
    snakeLen = 1
    occur[snakeHead.row][snakeHead.col] = True
    for _ in range(INIT_LEN-1):
        newTail = Snake(snakeTail.row, snakeTail.col - 1, None, snakeTail)
        snakeTail.prev = newTail
        snakeTail = newTail
        occur[snakeTail.row][snakeTail.col] = True
        snakeLen = snakeLen + 1
    s = snakeHead
    while s is not None:
        s.pin(oled)
        s = s.prev
    food.pin(oled)
    enable_irq(irqState)


def game_step() -> int:  # return how many ms to sleep
    global snakeHead, snakeTail, snakeLen, food, dir
    irqState = disable_irq()
    dir = get_dir()
    nxtR, nxtC = snakeHead.next_pos(dir)
    # print(f"{nxtR} {nxtC}")
    walking = True
    if food.row == nxtR and food.col == nxtC:
        # EAT
        walking = True
        if snakeLen < MXLEN:
            newHead = Snake(nxtR, nxtC, snakeHead, None)
            occur[newHead.row][newHead.col] = True
            snakeHead.next = newHead
            snakeHead = newHead
        else:
            # do nothing
            pass
        ri = random.randint(0, (ROW-2)*(COL-2))  # random int
        food.set_pos(ri//(COL-2) + 1, ri % (COL-2) + 1)
        food.pin(oled)
    elif occur[nxtR][nxtC]:
        # DEAD(or just do nothing), TODO
        walking = False
    elif dir == DIR_NONE:
        walking = False
    else:
        # CONTINUE walking
        walking = True
        if snakeHead is snakeTail:
            snakeHead.unpin(oled)
            snakeHead.set_pos(nxtR, nxtC)
            snakeHead.pin(oled)
        else:
            snakeTail.unpin(oled)
            occur[snakeTail.row][snakeTail.col] = False
            newTail = snakeTail.next
            newTail.prev = None
            snakeTail.prev = snakeHead
            snakeTail.next = None
            snakeHead.next = snakeTail
            snakeHead = snakeTail
            snakeTail = newTail
            snakeHead.set_pos(nxtR, nxtC)
            snakeHead.pin(oled)
            occur[snakeHead.row][snakeHead.col] = True
    oled.show()
    if walking:
        rgb.set_rgb(0, 128, 0) # green
    else:
        rgb.set_rgb(0, 0, 128) # blue
    t = 100000 - 2*knob.read_u16()
    enable_irq(irqState)
    return t


def set_restart(pin: Pin):
    global needRestart
    irqState = disable_irq()
    needRestart = True
    enable_irq(irqState)


restartButton.irq(handler=set_restart, trigger=Pin.IRQ_FALLING)


print("Started")
sysLed.on()
rgb.set_rgb(0, 0, 128) # blue
oled.show()  # no oled.fill(0)!


globalIrqState = disable_irq()
while True:
    try:
        if needRestart:
            game_init()
            needRestart = False
        enable_irq(globalIrqState)
        t = game_step()
        # print(f"sleep {t}us.")
        sleep_us(t)
        globalIrqState = disable_irq()
    except KeyboardInterrupt:
        break
enable_irq(globalIrqState)
print("Finished.")
sysLed.off()
rgb.off()
oled.fill(0)
oled.show()
