import time
import usb_finder_win
from src.tacho_rotator.tacho_reader import TachoReader

class TachoRotator:
    def __init__(self):
        self._port = None
        self._tacho = None
        self._last_rps = 0.0

    def start(self):
        port = usb_finder_win.pick_com_ports()
        print("Device and port:", port)
        self._tacho = TachoReader(port.name)
        self._tacho.start()
        try:
            while self._tacho.is_running():
                self.loop()
        except KeyboardInterrupt:
            print("Interrupted.  Stopping...")
            self._tacho.stop()

    def loop(self):
        rps = self._tacho.get_rps()
        if rps != self._last_rps:
            self._last_rps = rps
            print("RPS updated:", rps)

        ## Tell "rotator class" new RPS

        return None

if __name__ == '__main__':
    port = None
    usb = None
    buff = None
    rotator = TachoRotator()
    rotator.start()

