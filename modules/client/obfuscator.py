#! /usr/bin/python

import base64

def encode(filepath):
  file = open(filepath, "rb").read()
  encoded = base64.b64encode(file)
  return encoded

def decode(filepath):
   file = open(filepath, "rb").read()
   decoded = base64.b64decode(file)
   return decoded
