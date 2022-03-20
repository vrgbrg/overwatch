#!/bin/bash

#keyboard settings
sed -ie '/^XKBLAYOUT=/s/".*"/"hu"/' /etc/default/keyboard && udevadm trigger --subsystem-match=input --action=change
echo "ttyS0::askfirst:/bin/sh" >> /sbin/init

#update and upgrade
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
apt autoremove -y
