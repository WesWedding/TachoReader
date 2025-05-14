import asyncio
import threading

import serial
import re

class TachoReader:

    RPS_PREFIX = 'RPS'
    RPS_SUFFIX = ';'

    def __init__(self, port_name: str):
        self._debug = None
        self._port_name = port_name
        self._last_rps = 0
        self._task: asyncio.Task|None = None
        self._loop: asyncio.EventLoop|None = None
        self._usb = serial.Serial(self._port_name, 9600, timeout=5)
        self._running = False

        self._thread: threading.Thread|None= None
        self._runlock = threading.Lock()
        self._rpslock = threading.Lock()

        pfx = self.RPS_PREFIX
        sfx = self.RPS_SUFFIX
        print(rf"{re.escape(pfx)}([0-9].[0-9]){re.escape(sfx)}")
        self._regex = re.compile(rf"{re.escape(pfx)}([0-9].[0-9]*){re.escape(sfx)}")

    def start(self, debug=False):
        if self._running:
            return None
        print("TachoReader: Starting...")
        with self._runlock:
            self._debug = debug
            self._running = True
            self._thread = threading.Thread(target=self.listen)
            self._thread.start()

        return None

    def listen(self):
        while self._running:
            rps = self._read_rps()
            if self._debug:
                print(f"RPS: {self._last_rps}")
            with self._rpslock:
                self._last_rps = rps

    def stop(self):
        print("TachoReader: Stopping...")
        with self._runlock:
            self._running = False
            if self._thread.is_alive():
                self._thread.join()

    def get_rps(self):
        with self._rpslock:
            return self._last_rps

    def is_running(self):
        return self._running

    def _read_rps(self) -> float:
        buffer = self._usb.read_until(self.RPS_SUFFIX.encode('ascii'))
        decoded = buffer.decode('ascii')
        match = self._regex.search(decoded)
        if not match:
            print("Warning: No RPS parsed from last update.")
            return 0
        rps_match = match.group(1)
        return float(rps_match)






