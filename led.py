from machine import PWM


class RgbLed:
    """
    Rgb led. No voltage needed, pwm drive.
    """

    def __init__(self, gpidR: int, gpidG: int, gpidB: int) -> None:
        self.r = PWM(gpidR)
        self.g = PWM(gpidG)
        self.b = PWM(gpidB)
        self.r.freq(2000)  # 2K Hz
        self.g.freq(1999)  # 1999 Hz
        self.b.freq(5000)  # 5K Hz
        self.off()  # off init

    def set_rgb(self, r: int, g: int, b: int):
        assert 0 <= r < 256 and 0 <= g < 256 and 0 <= b < 256
        # x / 256 * 65536 = x * 256
        self.r.duty_u16(r * 256)
        self.g.duty_u16(g * 256)
        self.b.duty_u16(b * 256)

    def off(self):
        self.set_rgb(0, 0, 0)
