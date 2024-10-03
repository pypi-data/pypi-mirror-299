from RPi import GPIO


def initGPIO(mode=GPIO.BCM, warnings: bool = False) -> type[None]:
    GPIO.setmode(mode)
    GPIO.setwarnings(warnings)
