#! /usr/bin/python2

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

import PySimpleGUI27 as sg
#import threading as th #may cause problems
import time #timing the checkup so that a client isnt flooded with checkups
import sys
import os

currentDir = os.getcwd()

def populateAccounts(): #returns a dictionary of lists of accounts
  #example format returned: {0: ['account1@mail.com', 'password1'], 1: ['account2@mail.com', 'password2'], 2: ['account3@mail.com', 'password3']}
  dirtyaccountList = open(currentDir + "/config/accountList", 'r+b').readlines()
  accounts= {}
  counter = 0
  for account in dirtyaccountList[:-1]:
    accounts[counter] = account.strip().split(':')
    counter = counter + 1
  return accounts
def populateClients():
  dirtyClientList = open(currentDir + "/config/clientList", 'r+b').readlines()
  clients = {}
  counter = 0
  for client in dirtyClientList[:-1]:
    clients[counter] = client.strip().split(":")
    counter = counter + 1
  return clients


def startup():
  layout = [[sg.Text('Please enter the name of your server:')],[sg.InputText()],[sg.Submit(), sg.Cancel()]]
  window = sg.Window('Project0', layout)
  event, values = window.Read()
  window.Close()
  ServerName = values[0]
  return ServerName

def main(ServerName): #main window layout for managing clients
  accounts = populateAccounts()
  clients = populateClients()

  menu_def = [['&File',['Edit Modules','Edit ProxyList',]],
            ['&Edit', ['Config', ['Proxy', 'Module', ]]],
            ['&Help', '&About']]
  layout = [[sg.Menu(menu_def, tearoff=True)],
    [sg.Combo(["Create Payload", "Launch Payload", "Open shell", "Check Status of Clients", "Check Status of ProxyChains"],size=(100,10),enable_events=True,readonly=True),sg.Listbox(values=(accounts.values()), size=(50, 20))],
#    [sg.Radio("Command String", "Create your own command to send", default=True, size=(30,2)),sg.Radio("Activate Module", "Use a predifined module on client", default=True, size=(30,2))],
    [sg.Button("Execute", size=(20,2),button_color=["red","black"])],
    [sg.Text("Notes")],
    [sg.Multiline(autoscroll=True,size=(100,10),do_not_clear=True),sg.Listbox(values=(clients.values()), size=(50, 10))],
    [sg.Button("Save", tooltip='Click to save notes for client',button_color=["black","white"]),sg.Button('Add Client',button_color=["black","white"]),sg.Button('Add Module',button_color=["black","white"]), sg.Button('Add Account',button_color=["black","white"]), sg.Button("Clear",button_color=["black","white"])]]
  window = sg.Window(ServerName, layout)
  while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
      break
    elif event == "Open Config":
      fileName = openFileBox()
    elif event == "Add Account":
      addAccount()
    elif event == "Add Client":
      addClient()
    elif event == "Add Module":
      addModule()
    elif event == "About":
      help = open(currentDir + "/../../README.md", "r").read()
      
    else:
      print(event, values)

  window.Close()
  pass

def parseWindow(windowType): #parses all buttons,checkboxes, etc. for the selected window
  pass
def createConfig(): #create a config to bundle into payload to be loaded by the client
  pass
def launchPayload(): #send the obfuscated and encrypted command payload, module, or config update to the client
  pass
def createPayload(): #create a command payload to be saved somewhere
  pass
def status(): #keeps a live running update of whether the client is live or dead
  pass
def checkup(): #module used to essentially "ping" the client to check if it is alive or dead
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
def processEmail(accountDetails): #logs in to account, makes sure the address is valid, if not red out in the select account list
  pass

def openFileBox():
  layout = [[sg.T('Source Folder')],
              [sg.In()],
              [sg.FileBrowse(target=(-1, 0)), sg.OK()]]
  window = sg.Window("Choose File", layout)
  event, values = window.Read()
  return values
def popUpError(ErrorMessage):
  sg.PopupError('PopupError')
  pass

main(startup())
#addAccount()
#openFileBox()
