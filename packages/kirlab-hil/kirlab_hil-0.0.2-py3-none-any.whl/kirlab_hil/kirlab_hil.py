import os
import ctypes

# Get the directory of the current file (this ensures the path is portable)
dll_path = os.path.join(os.path.dirname(__file__), 'lib', 'libkirlab_hil_api.dll')

# Load the DLL
kirlab_dll = ctypes.CDLL(dll_path)



# Define the return types and argument types of the C functions
kirlab_dll.listDevices.restype = POINTER(ctypes.c_char_p)
kirlab_dll.openDevice.argtypes = [ctypes.c_char_p]
kirlab_dll.closeDevice.argtypes = [ctypes.c_char_p]
kirlab_dll.getDeviceState.argtypes = [ctypes.c_char_p]
kirlab_dll.getDeviceState.restype = ctypes.c_int
kirlab_dll.listProjectSignals.argtypes = [ctypes.c_char_p]
kirlab_dll.listProjectSignals.restype = POINTER(ctypes.c_char_p)
kirlab_dll.loadProject.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
kirlab_dll.readSignal.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
kirlab_dll.readSignal.restype = ctypes.c_double
kirlab_dll.writeSignal.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double]
kirlab_dll.start.argtypes = [ctypes.c_char_p]
kirlab_dll.pause.argtypes = [cttes.c_char_p]
kirlab_dll.resume.argtypes = [ctypes.c_char_p]
kirlab_dll.stop.argtypes = [ctypes.c_char_p]


def list_devices():
    devices = kirlab_dll.listDevices()
    return [device.decode('utf-8') for device in devices if device]


class Device:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.project = ""

    def open(self):
        kirlab_dll.openDevice(self.serial_number.encode('utf-8'))

    def close(self):
        kirlab_dll.closeDevice(self.serial_number.encode('utf-8'))

    def get_state(self):
        state = kirlab_dll.getDeviceState(self.serial_number.encode('utf-8'))
        return state

    def load_project(self, project_url):
        kirlab_dll.loadProject(self.serial_number.encode('utf-8'), project_url.encode('utf-8'))
        self.project = project_url

    def read_signal(self, signal_name):
        value = kirlab_dll.readSignal(self.serial_number.encode('utf-8'), signal_name.encode('utf-8'))
        return value

    def write_signal(self, signal_name, value):
        kirlab_dll.writeSignal(self.serial_number.encode('utf-8'), signal_name.encode('utf-8'), c_double(value))

    def start(self):
        kirlab_dll.start(self.serial_number.encode('utf-8'))

    def pause(self):
        kirlab_dll.pause(self.serial_number.encode('utf-8'))

    def resume(self):
        kirlab_dll.resume(self.serial_number.encode('utf-8'))

    def stop(self):
        kirlab_dll.stop(self.serial_number.encode('utf-8'))

    def list_available_signals(self):
        signals = kirlab_dll.listProjectSignals(self.project.encode('utf-8'))
        return [signal.decode('utf-8') for signal in signals if signal]


# Example usage
if __name__ == "__main__":
    devices = list_devices()
    print("Devices: ", devices)

    if devices:
        device = Device(devices[0])
        device.open()
        device.load_project("/path/to/project")
        print("Device state: ", device.get_state())
        print("Signals: ", device.list_available_signals())
        print("Read signal: ", device.read_signal("signal_name"))
        device.write_signal("signal_name", 1.23)
        device.start()
        device.stop()
        device.close()
