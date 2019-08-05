#! /usr/bin/python

from obfuscator import *

#the client should only ever recieve a server username as a config, encoded as base64

def read_conf(file):
    return decode(file)