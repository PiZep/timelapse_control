#!/bin/bash

WPATH=$(cd $(dirname $0) && pwd)
SCRIPTS=$WPATH/hotspot_scripts
HOST_ID=printf "%02d" $1
IP_ID=printf "%d0" $1

sudo apt update -y
sudo apt upgrade -y

sudo apt install -y hostapd dnsmasq

sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

# Set dnsmasq configuration
printf "# RPi hotspot configurationi
interface=wlan0
bind-dynamic
domain-needed
bogus-priv
dchp-range=192.168.%d.50,192.168.%d.100,255.255.255.0,12h" $IP_ID $IP_ID\
    | sudo tee -a /etc/dnsmasq.conf > /dev/null

# Set dhcpcd.conf file
# Look for the options, add them if not found
DHCPCD="/etc/dhcpcd.conf"
for option in "nohook wpa_supplicant" \
    "interface wlan0" \
    "$(printf "static ip_address=192.168.%d.10/24" $IP_ID)" \
    "$(printf "static routers=192.168.%d.10" $IP_ID)"
do
    grep -q "$option" $DHCPCD && sudo sed -ri 's:^[# ]*('"$option"'):\1:' $DHCPCD || echo $option | sudo tee -a $DHCPCD > /dev/null
done

# Turn ip forwarding in /etc/sysctl.conf
SYSCTL="/etc/sysctl.conf"
pattern="net.ipv4.ip_forward="
grep -q "$pattern" $SYSCTL && sudo sed -ri 's:^[# ]*('"$pattern"')[0-9]:\11:' $SYSCTL || echo $option1 | sudo tee -a $SYSCTL > /dev/null

for f in $(ls $SCRIPTS)
do
    DEST=''
    case $f in
        "hostapd.conf")r
            $DEST="/etc/hostapd/"
            sed -ri 's/HOST_ID/'"$HOST_ID"'/'
            ;;
        "hs-iptables.service")
            $DEST="/etc/systemd/system/"
            ;;
        "iptables-hs")
            $DEST="/etc/hostapd/"
            sudo chmod +x $f
    esac
    sudo cp $SCRIPTS/$f $DEST
done
sudo systemctl enable hs-iptables
