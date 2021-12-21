import os
import platform

if platform.system() == 'Linux':
    print(os.environ.get('LINUX_WITHOUT_DBUS', '0'))