from machine import Pin, ADC, PWM


class DirectionKeys:
    """
    Direction keys (i.e. four button).
    TOOD: Consider to use interrupt to handle key press event.
    """

    def __init__(self, gpidL: int, gpidD: int, gpidU: int, gpidR: int) -> None:
        self.l = Pin(gpidL, Pin.IN, Pin.PULL_UP)
        self.d = Pin(gpidD, Pin.IN, Pin.PULL_UP)
        self.u = Pin(gpidU, Pin.IN, Pin.PULL_UP)
        self.r = Pin(gpidR, Pin.IN, Pin.PULL_UP)

    def get_l(self) -> bool:
        return self.l.value() > 0

    def get_d(self) -> bool:
        return self.d.value() > 0

    def get_u(self) -> bool:
        return self.u.value() > 0

    def get_r(self) -> bool:
        return self.r.value() > 0

    # def get_rc_dir(self) -> tuple:
    #     row = 0
    #     col = 0
    #     if self.l.value() > 0:
    #         col = col - 1
    #     if self.r.value() > 0:
    #         col = col + 1
    #     if self.u.value() > 0:
    #         row = row - 1
    #     if self.d.value() > 0:
    #         row = row + 1
    #     return (row, col)

    def get_key_val(self) -> tuple:
        return (self.l, self.d, self.u, self.r)
