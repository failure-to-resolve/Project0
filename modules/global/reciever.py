#! /usr/bin/python
import easyimap

def run(serveruser, serverpass, function):
  server = easyimap.connect('imap.gmail.com'. serveruser, serverpass)
  i=0
  update = []
  command = []

  for each in server.listids(limit=10):
    mail = server.mail(each)
    update.append[mail.body]
    command.append[mail.title]
  return command, update