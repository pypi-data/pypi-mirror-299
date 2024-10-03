from RPi import GPIO
from rpi_artic_lib.GPIO import inout


OUTPUT = inout.OUTPUT
INPUT = inout.INPUT


class Port:
    def __init__(
        self,
        pins: list[int],
        mode: int,
        initial_value: bytes = 0x00,
        pull_up_down: int = GPIO.PUD_UP,
    ):
        self.pins: list[inout.InOut] = []
        for pin in pins:
            pinInstance: inout.InOut = inout.InOut(pin, mode, False)
            self.pins.append(pinInstance)
        if mode == inout.OUTPUT:
            self.setAsOutput(initial_value)
        else:
            self.setAsInput(pull_up_down)

    def write(self, value: int) -> type[None]:
        for i in range(len(self.pins)):
            mask: int = int(0x01 << i)
            self.pins[i].writeByte(value & mask)

    def read(self) -> bytes:
        value = 0x00
        for i in range(len(self.pins)):
            value |= self.pins[i].readByte() << i
        return value

    def writeBit(self, bit: int, value: bool) -> type[None]:
        self.pins[bit].write(value)

    def readBit(self, bit: int) -> bool:
        return self.pins[bit].read()

    def setAsInput(self, pull_up_down: int = GPIO.PUD_UP) -> type[None]:
        for pin in self.pins:
            pin.setAsInput(pull_up_down=pull_up_down)

    def setAsOutput(self, initial_value: bytes = 0x00) -> type[None]:
        for pin in self.pins:
            pin.setAsOutput(initial_state=initial_value)
