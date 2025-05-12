from json import JSONDecodeError

import serial.tools.list_ports
import json
from serial.tools.list_ports_common import ListPortInfo

def get_com_ports() -> list[ListPortInfo]:
    return serial.tools.list_ports.comports()

def pick_com_ports() -> ListPortInfo:
    ports = get_com_ports()
    if len(ports) == 0:
        raise IOError("No connected devices found")

    device = get_saved_device()

    if device:
        for i, port in enumerate(ports):
            if port.hwid == device.hwid:
                print("Saved device found.")
                return ports[i]

        print("Saved device not found: ", device.hwid)

    if len(ports) == 1:
        print("Saving only device found:", ports[0].hwid)
        save_com_port_device(ports[0])
        return ports[0]

    options = []
    accepted_vals = []
    for i, port in enumerate(ports):
        options.append({'name': port.name, 'desc': port.description})
        accepted_vals.append(i + 1)

    print("Select available devices:")
    choice = None
    while choice not in accepted_vals:
        for i, option in enumerate(options):
            print(f"{i}:", f"{option['name']} {option['desc']}")
        choice = int(input("-->"))
    port = ports[choice - 1]
    save_com_port_device(port)
    return port

def save_com_port_device(port: ListPortInfo) -> bool:
    device = SavedDevice.from_port_info(port)
    try:
        with open("device.json", "w") as file:
            json.dump(device.__dict__, file)
            file.close()
            return True

    except OSError as err:
        print("Failed to save device:", err.strerror)
        return False
    except TypeError as err:
        print("Failed to save device JSON:", err)
        return False

def get_saved_device():
    try:
        with open("device.json", "r") as file:
            data = json.load(file)
            device = SavedDevice(data['hwid'], data['name'], data['desc'], data['version'])
            return device

    except OSError as err:
        print("Failed to load device:", err.strerror)
        return False
    except JSONDecodeError as err:
        print("Failed to read saved JSON:", err.msg)
        return False

def debug_print_port(port: ListPortInfo):
    for key, value in port.__dict__.items():
        print([key, value])

class SavedDevice:
    """Info about the previously used device."""

    CURRENT_VERSION = 1

    def __init__(self, hwid, name, desc, version):
        self.hwid = hwid
        self.name = name
        self.desc = desc
        self.version = version

    @classmethod
    def from_port_info(cls, port: ListPortInfo):
        data = {
            'version': cls.CURRENT_VERSION,
            'hwid': port.hwid,
            'name': port.name,
            'desc': port.description,
        }
        return cls(port.hwid, port.name, port.description, cls.CURRENT_VERSION)


if __name__ == '__main__':
    pick_com_ports()