import serial
from serial import SerialException
from serial.rfc2217 import Serial

import usb_finder_win

port = usb_finder_win.pick_com_ports()
print("Device and port:", port)

usb = serial.Serial(port.name, 9600, timeout=5)

try:
    while True:
        buff = usb.read_until(';'.encode('ascii'))
        print(buff.decode('ascii'))

except SerialException as e:
    print(e)