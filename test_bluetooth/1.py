import gatt
import threading
import time


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
    def __init__(self, mac_address, manager):
        self.lzchar = None
        super().__init__(mac_address, manager, managed=True)

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
        service = next(
            s for s in self.services
            if s.uuid == 'A254565F-DBA6-49A6-8CB6-5FD260A37F7B'.lower())

        self.lzchar = next(
            c for c in service.characteristics
            if c.uuid == 'E4A02648-4366-4FA4-A212-21B3A040947B'.lower())

        lzchar2 = next(
            c for c in service.characteristics
            if c.uuid == '2AA6068E-9981-4B3B-BC8F-E6F1A6D5EAE8'.lower())

        lzchar2.enable_notifications()

    def characteristic_enable_notifications_succeeded(self, characteristic):
        super().characteristic_enable_notifications_succeeded(characteristic)
        print("[%s] notify ok" % (self.mac_address))

    def characteristic_enable_notifications_failed(self, characteristic, error):
        super().characteristic_enable_notifications_failed(characteristic, error)
        print("[%s] notify err. %s" % (self.mac_address, error))

    def characteristic_write_value_succeeded(self, characteristic):
        super().characteristic_write_value_succeeded(characteristic)
        print("[%s] wr ok" % (self.mac_address))

    def characteristic_write_value_failed(self, characteristic, error):
        super().characteristic_write_value_failed(characteristic, error)
        print("[%s] wr err %s" % (self.mac_address, error))

    def characteristic_value_updated(self, characteristic, value):
        print("[%s] noty: %s" % (self.mac_address, value))


manager = AnyDeviceManager(adapter_name='hci0')
device = AnyDevice(mac_address='F3:84:D3:A5:87:B4', manager=manager)
device.connect()
time.sleep(1)

manager.loop_start()
while True:
    cmd = input("input a command...(press Enter to stop ble connect.)\n")
    if len(cmd) < 1:
        break
    device.lzchar.write_value(cmd.encode())
manager.loop_stop()
