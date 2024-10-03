from RPi import GPIO


class Output:
    def __init__(self, pin: int, initial_state: bool = False):
        self.pin = pin
        self.state = initial_state
        GPIO.setup(self.pin, GPIO.OUT)
        self.write(initial_state)

    def write(self, value: bool):
        GPIO.output(self.pin, value)
        self.state = value

    def writeByte(self, value: bytes):
        if value == 0x00:
            self.write(False)
        else:
            self.write(True)

    def toggle(self):
        self.write(not self.state)

    def setHIGH(self):
        self.write(True)

    def setLOW(self):
        self.write(False)
