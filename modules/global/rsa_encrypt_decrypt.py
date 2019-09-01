#! /usr/bin/python2

import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import os

dir = os.getcwd()


def getRandom():
  return Random.new().read

def generateKey():
  return RSA.generate(1024,getRandom())

def encryptRSA(key, payload):
  publicKey = key.publickey()
  return publicKey.encrypt(payload)

def decryptRSA(key, payload):
  return key.decrypt(payload)

def getKeys(privatePath, publicPath):
  pub = open(dir + publicPath, 'w+')
  pri = open(dir + privatePath, 'w+')

  key = generateKey()

  pub.write(key.publickey().export_key('PEM'))
  pri.write(key.export_key('PEM'))

  pub.close()
  pri.close()

  return key

def test():
  key = getKeys("/privateKey","/publicKey")
  print key

test()

