import time
from rpi_artic_lib.GPIO import output
from rpi_artic_lib.GPIO import port

# Constants
# Oder size
BYTE = 0x01
HALFBYT = 0x00
# Cursor direction
INCREMENT = 0x01
DECREMENT = 0x00
# Scrolling screen
SCROLLING_SCRREN = 0x01
STATIC_SCREEN = 0x00
# Cursor and blink
CURSOR_AND_BLINK = 1
CURSOR_NO_BLINK = 2
NO_CURSOR_NO_BLINK = 3
# LINES and DOTS
LINES1 = 0x00
LINES2 = 0x01
DOTS5x8 = 0x00
DOTS5x10 = 0x01
# Screen status
SCREEN_BUSY: bool = True
SCREEN_READY: bool = False
# Display control
DISPLAY_ON: bytes = 0x01
DISPLAY_OFF: bytes = 0x00

# Instuction code
CLEAR_DISPLAY: bytes = 0x01
RETURN_HOME: bytes = 0x02
ENTRY_MODE_SET: bytes = 0x04
DISPLAY_CONTROL: bytes = 0x08
CURSOR_DISPLAY_SHIFT: bytes = 0x10
FUNCTION_SET: bytes = 0x20
SET_CGRAM_ADDRESS: bytes = 0x40
SET_DDRAM_ADDRESS: bytes = 0x80

# RS and RW values
RS_INSTRUCTION: bool = False
RS_DATA: bool = True
RW_WRITE: bool = False
RW_READ: bool = True


class LCDScreen:
    def __init__(
        self,
        pinNumberRS: int,
        pinNumberRW: int,
        pinNumberEnable: int,
        pinNumbersDatabus: list[int],
    ) -> type[None]:
        self.setPinRS(pinNumberRS)
        self.setPinRW(pinNumberRW)
        self.setPinEnable(pinNumberEnable)
        self.setDatabus(pinNumbersDatabus)

    def screenInit(
            self,
            mode: bytes = BYTE,
            lines: bytes = LINES2,
            dots: bytes = DOTS5x8,
            cursorMode: int = NO_CURSOR_NO_BLINK,
            cursorDirection: bytes = INCREMENT,
            scroll: bytes = STATIC_SCREEN,
            display: bytes = DISPLAY_ON,
            ) -> type[None]:
        self.functionSet(mode, lines, dots)
        self.displayControl(display, cursorMode)
        self.entryModeSet(cursorDirection, scroll)
        self.clearDisplay()
        self.returnHome()

    def setPinEnable(self, pinNumber: int) -> type[None]:
        pin = output.Output(pinNumber, initial_state=False)
        self.pinEnable = pin

    def setPinRS(self, pinNumber: int) -> type[None]:
        pin = output.Output(pinNumber, initial_state=False)
        self.pinRS = pin

    def setPinRW(self, pinNumber: int) -> type[None]:
        pin = output.Output(pinNumber, initial_state=False)
        self.pinRW = pin

    def setDatabus(self, pinNumbers: list[int]) -> type[None]:
        self.databus = port.Port(pinNumbers, port.OUTPUT)

    def sendInstuction(self, instruction: bytes) -> type[None]:
        self.pinRS.write(RS_INSTRUCTION)
        self.pinRW.write(RW_WRITE)
        self.databus.setAsOutput()
        self.databus.write(instruction)
        self.pinEnable.write(True)
        time.sleep(0.0001)
        self.pinEnable.write(False)
        while self.readBusyFlag() == SCREEN_BUSY:
            time.sleep(0.001)

    def sendChar(self, char: str) -> type[None]:
        charByte: int = ord(char)
        self.pinRS.write(RS_DATA)
        self.pinRW.write(RW_WRITE)
        self.databus.setAsOutput()
        self.databus.write(charByte)
        self.pinEnable.write(True)
        time.sleep(0.0001)
        self.pinEnable.write(False)

    def sendString(self, string: str) -> type[None]:
        for char in string:
            self.sendChar(char)

    def readBusyFlag(self) -> bool:
        self.databus.setAsInput()
        self.pinRS.write(RS_INSTRUCTION)
        self.pinRW.write(RW_READ)
        self.pinEnable.write(True)
        time.sleep(0.0001)
        busyFlag = self.databus.read()
        maskedBusyFlag = busyFlag & 0x80
        if maskedBusyFlag == 0:
            return SCREEN_READY
        else:
            return SCREEN_BUSY

    def readChar(self) -> type[None]:
        pass

    def clearDisplay(self) -> type[None]:
        self.sendInstuction(CLEAR_DISPLAY)

    def returnHome(self) -> type[None]:
        self.sendInstuction(RETURN_HOME)

    def entryModeSet(self, direction: bytes, shift: bytes) -> type[None]:
        self.sendInstuction(ENTRY_MODE_SET | (direction << 1) | shift)

    def displayControl(self, display: bytes, cursorMode: int) -> type[None]:
        if cursorMode == CURSOR_AND_BLINK:
            cursor = 0x00
            blink = 0x00
        elif cursorMode == CURSOR_NO_BLINK:
            cursor = 0x01
            blink = 0x00
        else:
            cursor = 0x01
            blink = 0x01

        instruction = DISPLAY_CONTROL | (display << 2) | (cursor << 1) | blink
        self.sendInstuction(instruction)

    def cursorDisplayShift(self, direction: bytes, scroll: bytes) -> type[None]:
        self.sendInstuction(CURSOR_DISPLAY_SHIFT | (direction << 2) | scroll)

    def functionSet(self, DataLength: bytes, lines: bytes, dots: bytes) -> type[None]:
        instruction = FUNCTION_SET | (DataLength << 4) | (lines << 3)
        instruction = instruction | (dots << 2)
        self.sendInstuction(instruction)

    def setCGRAMAddress(self, address) -> type[None]:
        self.sendInstuction(SET_CGRAM_ADDRESS | address)

    def setDDRAMAddress(self, address) -> type[None]:
        self.sendInstuction(SET_DDRAM_ADDRESS | address)
