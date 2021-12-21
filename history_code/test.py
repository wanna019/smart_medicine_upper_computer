import bluetooth
import datetime
import time

nearby_device = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_device))


list = {'name':[], 'addr:':[]}

for addr, name in nearby_device:
    if name not in list['name']:
        list['name'].append(name)
        list['addr:'].append(addr)
        print("%s - %s" % (addr, name))
# while True:
#
#     for addr, name in nearby_device:
#         if name not in list['name']:
#             print('found a new device')
#             list['name'].append(name)
#             list['addr:'].append(addr)
#             print("%s - %s" % (addr, name))
#     nearby_device = bluetooth.discover_devices(lookup_names=True)

bd_addr = "A4:45:19:75:50:A1"
# uuid='00001101-0000-1000-8000-00805f9b34fb'
# uuid = '1e0ca4ea-299d-4335-93eb-27fcfe7fa848'
uuid = 'ed8e9819-a04e-4c94-bd35-11d772e6a1b8'

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM)
#
sock.bind(("", bluetooth.PORT_ANY))
#
port = sock.getsockname()[1]
print(port)
#
service_match = bluetooth.find_service(address=bd_addr)
print(service_match)
if len(service_match) > 0:
    port = service_match[0]['port']
print(port)

sock.connect((bd_addr,port))
while True:
    curr_time = datetime.datetime.now()
    time_str = curr_time.strftime('%Y-%m-%d %H:%M:%S')
    sock.send(time_str)
    data = sock.recv(10)  # 1024为数据长度
    print("received:", data)
    time.sleep(2)
