from gattlib import DiscoveryService

service = DiscoveryService()
print(service)
devices = service.discover(2)
addr_temp = "D7:ED:FB:2C:F6:7E"
addr = None

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))
    if addr_temp == address:
        print("found")
        addr = address

if addr:
    print(addr)
