import gatt
import threading
from argparse import ArgumentParser

class AnyDeviceManager(gatt.DeviceManager):
    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))

    def loop_start(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True
        self._thread.start()

    def loop_stop(self):
        self.stop()


class AnyDevice(gatt.Device):
    Nordic_UART_Service = None
    Nordic_UART_RX = None

    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()

        print("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            for characteristic in service.characteristics:
                print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))

        try:
            global Nordic_UART_Service
            Nordic_UART_Service = next(
                s for s in self.services
                if s.uuid == '6e400001-b5a3-f393-e0a9-e50e24dcca9e'.lower())

        except StopIteration:
            pass
        try:
            global Nordic_UART_RX
            Nordic_UART_RX = next(
                c for c in Nordic_UART_Service.characteristics
                if c.uuid == '6e400003-b5a3-f393-e0a9-e50e24dcca9e'.lower())
        except StopIteration:
            pass

        Nordic_UART_RX.read_value()



    def characteristic_value_updated(self, characteristic, value):
        print("notify :", value.decode('utf-8'))


print("Connecting...")


if __name__ == "__main__":
    manager = AnyDeviceManager(adapter_name='hci0')
    # mac_address = "D7:ED:FB:2C:F6:7E"
    mac_address = "F3:84:D3:A5:87:B4"
    device = AnyDevice(manager=manager, mac_address=mac_address)
    device.connect()
    manager.loop_start()

    manager.run()