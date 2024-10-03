from RPi import GPIO


class Input:
    def __init__(self, pin: int, pull_up_down: int = GPIO.PUD_UP):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=pull_up_down)

    def read(self) -> bool:
        return GPIO.input(self.pin)

    def isHIGH(self) -> bool:
        return GPIO.input(self.pin)

    def isLOW(self) -> bool:
        return not GPIO.input(self.pin)

    def readByte(self) -> bytes:
        if self.isHIGH():
            return 0x01
        else:
            return 0x00
