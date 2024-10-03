from RPi import GPIO
from rpi_artic_lib.GPIO import input
from rpi_artic_lib.GPIO import output


INPUT = 1
OUTPUT = 2


class InOut(input.Input, output.Output):
    def __init__(
        self,
        pin: int,
        direction: int,
        initial_state: bool = False,
        pull_up_down: int = GPIO.PUD_UP,
    ) -> None:
        self.pin = pin
        self.direction = direction
        self.pull_up_down = pull_up_down
        self.state = initial_state
        if self.direction == INPUT:
            self.setAsInput(pull_up_down=self.pull_up_down)
        else:
            self.setAsOutput(initial_state=initial_state)

    def setAsInput(self, pull_up_down: int = GPIO.PUD_UP) -> None:
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=pull_up_down)

    def setAsOutput(self, initial_state: bool = False) -> None:
        GPIO.setup(self.pin, GPIO.OUT)
        self.write(initial_state)
