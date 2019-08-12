#! /usr/bin/python2

a = open("test" ,"rb").read().strip()


#Takes a single string, without newlines and uses a homebrewed encryption(Simple Xor), to prepare the string for network travel
def encrypt(inString,sequenceNum):
  interim = []
  output = []
  inputArray = list(inString)
  inputArray.insert(0,str(len(inString)))
  for eachChar in inputArray:
    interim.append((ord(eachChar)))
  for eachAscii in interim:
    output.append(str(eachAscii^sequenceNum)+'X')
    print eachAscii^sequenceNum
  output.append(str(sequenceNum)+'S')
  return ''.join(output[::-1])

#reverses the above encryption
def decrypt(inString):
  sequenceNum = inString.split('S')[0]
  print sequenceNum
  interimArray = []
  formattedArray = inString.split('S').pop(1).split('X')
  del formattedArray[-1]
  for eachAscii in formattedArray:
     interimArray.append(chr(int(eachAscii)^int(sequenceNum)))
  return ''.join(interimArray[::-1])[1:]


