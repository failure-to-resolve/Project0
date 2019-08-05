#! /usr/bin/python

from requests import get
import os

def run():
  raw_ips = []

  raw_ips.append(get('https://api.ipify.org').text)
  if os.name == "nt":
    data = os.popen("ipconfig").readlines()
    for ip in data:
      if "IPv4 Address" in ip:
        raw_ip = ip
        break
    raw_ip = raw_ip.split(':')
    raw_ip = raw_ip[1]
    raw_ips.append(raw_ip[1:])

  else:
    data = os.popen("ip addr").readlines()
    for ip in data:
      if ip[:9] == "    inet " and ip[9:12] != "127":
        raw_ip = ip[9:]
        break
    raw_ip = raw_ip.split(' ')
    raw_ip = raw_ip[0]
    raw_ips.append(raw_ip[:len(raw_ip)-3])

  ips = []

  for ip in raw_ips:
    ips.append(ip.encode('ascii', 'ignore'))
  return ips