#!/bin/bash

WPATH=$(cd $(dirname $0) && pwd)
SCRIPTS=$WPATH/hotspot_scripts

sudo apt update
sudo apt upgrade

sudo apt install -y hostapd dnsmasq

sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
