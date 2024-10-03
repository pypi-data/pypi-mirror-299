import subprocess
import re


class Board:
    def __init__(self):
        pass

    def getTemperature(self) -> float:
        temp = None
        err, msg = subprocess.getstatusoutput("vcgencmd measure_temp")
        if not err:
            m = re.search(r"-?\d\.?\d*", msg)  # a solution with a  regex
            try:
                temp = float(m.group())
            except ValueError:
                temp = None
        return temp
