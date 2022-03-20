import os

def check_mount_infos():
    os.system('ls /dev 2>/dev/null | grep -i "sd"')
    os.system('cat /etc/fstab 2>/dev/null | grep -v "^#" | grep -Pv "\W*\#" 2>/dev/null')
    os.system('grep -E "(user|username|login|pass|password|pw|credentials)[=:]" /etc/fstab /etc/mtab 2>/dev/null')