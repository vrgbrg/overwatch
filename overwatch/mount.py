import os
import reports.report as report

def check_mount_infos():
    output = os.popen('ls /dev 2>/dev/null | grep -i "sd"').read().split("\n")
    output += os.popen('cat /etc/fstab 2>/dev/null | grep -v "^#" | grep -Pv "\W*\#" 2>/dev/null').read().split("\n")
    output += os.popen('grep -E "(user|username|login|pass|password|pw|credentials)[=:]" /etc/fstab /etc/mtab 2>/dev/null').read().split("\n")

    report.storeMessage("title", "Mounted Devices")
    report.storeMessage("mounted_devices", output)
    for o in output:
        if o:
            print(o)