
import gatt



list_ble = {"name": [], "addr": []}  # 显示蓝牙设备的列表

class AnyDeviceManager(gatt.DeviceManager):
    """获取BLE的"""
    def device_discovered(self, device):
        if (device.alias()!=None)&(str(device.mac_address)[0:2] != str(device.alias().lower())[0:2]):
            if device.mac_address not in list_ble["addr"]:
                print("Discovered [%s] %s" % (device.mac_address, device.alias()))
                list_ble["addr"].append(device.mac_address)
                list_ble["name"].append(device.alias())


class BLE_CTL:
    """读取端口信息，连接端口，关闭端口"""
    def __init__(self):
        self.ble_manager = AnyDeviceManager(adapter_name='hci0')

    # def connect_device(self, addr):
    #     """实例化蓝牙类，建立连接。"""
    #     self.device = AnyDevice(manager=self.ble_manager, mac_address=addr)
    #     self.device.connect()

    def disconnect_device(self):
        """断开连接。"""
        self.device.disconnect()

    def thread_ctl(self):
        self.ble_manager.start_discovery()
        self.ble_manager.run()

