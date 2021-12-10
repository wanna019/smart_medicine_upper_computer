import pexpect
import re
import signal

scan = pexpect.spawn('hcitool lescan', timeout=3)

try:
    scan.expect('foooo')
except pexpect.EOF:
    before_eof = scan.before.decode('utf-8', 'replace')
    if "No such device" in before_eof:
        message = "No BLE adapter found"
    elif "Set scan parameters failed: Input/output errer" in before_eof:
        message = ("BLE adapter requires reset after a scan as root""- call adapter.reset()")
    else:
        message = "Unexpected error when scanning %s" % before_eof
    raise Exception(message)
except pexpect.TIMEOUT:
    devices = {}
    for line in scan.before.decode('utf-8', 'replace').split('\r\n'):
        match = re.match(r'(([0-9A-Fa-f][0-9A-Fa-f]:?){6}) (\(?.+\)?)', line)
        if match is not None:
            address = match.group(1)
            name = match.group(3)
            # print(match.group(3))
            if name == "(unknown)":
                name = None

            if address in devices:

                if (name is not None) and (address not in devices.keys()):
                    pass
            else:
                if (name is not None) and (address not in devices.keys()):
                    print("Discovered %s (%s)" % (address, name))
                    devices[address] = {
                        'address': address,
                        'name': name
                    }
    print('Found %d BLE devices' % len(devices))
finally:
    try:
        scan.kill(signal.SIGINT)

        while True:
            try:
                scan.read_nonblocking(size=100)
            except (pexpect.TIMEOUT, pexpect.EOF):
                break

        if scan.isalive():
            scan.wait()
    except OSError:
        print("Unable to gracefully stop the scan - "
              "BLE adapter may need to be reset")
