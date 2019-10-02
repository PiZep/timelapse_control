#!/usr/bin/python
# show hosts on network - this script is limited to x.x.x.x/24 networks
# by Johannes Kinzig - johanneskinzig.de
# call: script.py <networkaddress> <fromhost> <tohost> <hosttypes>

import sys
from datetime import datetime
import socket

if len(sys.argv) != 5:
    print 'Script takes exactly 5 parameters, given: ', len(sys.argv)
    sys.exit(0)
else:
    pass

############################################
#           Function definition            #
############################################

def scanport(addr, port):
    '''Check wether port is open on host'''
    socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = socket_obj.connect_ex((addr,port))
    socket_obj.close()

    if result == 0:
        machine_hostname = socket.gethostbyaddr(addr)[0]
        print "open port detected: " + str(addr) + " \t-- Port: " + str(port) + " \t-- Hostname: " + str(machine_hostname)
        return addr, port, machine_hostname #, macaddr
    else:
        return None

def scaniprange_24(ipaddress_nw, sth, enh, portlist):
    '''Scan ip address range for x.x.x.x/24 network'''
    # split network address to allow last byte to "iterate over it"
    host_prefix_pre = ipaddress_nw.split(".")
    host_prefix = host_prefix_pre[0] + "." + host_prefix_pre[1] + "." + host_prefix_pre[2] + "."

    print "Scanning network: ", ipaddress_nw, "\n"
    print "Scanning from ", sth, "to" , enh, "\n"


    # store detected ports in list
    detected_hosts = []
    
    for ip in range(sth, enh):
        '''Try to connect to each host'''
        # iterate through last byte -- 24 network

        # define dictionary to store open 
        open_port = {"ip":None, "hostname":None, "first_port":None}
        
        host = host_prefix + str(ip)
        for port in portlist:
            '''For each host try ports based on hosts in networks'''
            detected_host = scanport(host, port)
            if detected_host is None:
                continue
            else:
                open_port["ip"], open_port["first_port"], open_port["hostname"] = detected_host
                # append hosts/ports to list
                detected_hosts.append(open_port)
                break
                    
    return detected_hosts

############################################
#   networkscanner specific properties     #
############################################


# host types and ports which probably be open (common ports)
mac = [22, 445, 548, 631]
linux = [20, 21, 22, 23, 25, 80, 111, 443, 445, 631, 993, 995]
windows = [135, 137, 138, 139, 445]
aios = [49152, 62078]
unspecified = list(set(mac)|set(linux)|set(windows)|set(aios))

ipaddress_nw = sys.argv[1]
sth = int(sys.argv[2]) & 0xff         # start with host, strip off last 8 bits
enh = int(sys.argv[3]) & 0xff         # stop at this host, strip off last 8 bits
portlist_ident = sys.argv[4]

if portlist_ident == "mac":
    portlist = mac
elif portlist_ident == "linux":
    portlist = linux
elif portlist_ident == "windows":
    portlist = windows
elif portlist_ident == "aios":
    portlist = aios
else:
    print "Unkonwn portlist specified, using all available ports for host detection"
    portlist = unspecified
  

scan_start_time = datetime.now()
print "Starting Scan: ", scan_start_time
hostlist = scaniprange_24(ipaddress_nw, sth, enh, portlist)
scan_stop_time = datetime.now()

print "Stopping Scan, time consumed: ", scan_stop_time - scan_start_time
