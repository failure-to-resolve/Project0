#! /usr/bin/python2

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import easyimap

def recieve(serveruser, serverpass, function):
  server = easyimap.connect('imap.gmail.com'. serveruser, serverpass)
  i=0
  update = []
  command = []

  for each in server.listids(limit=10):
    mail = server.mail(each)
    update.append[mail.body]
    command.append[mail.title]
  return command, update

def send(clientusers, serveruser, serverpass, subject, text, filenames):
  #Clientusers is a list containing each username to send to

  msg = MIMEMultipart()
  msg['From'] = serveruser
  msg['To'] = ", ".join(clientusers)
  msg['Subject'] = subject

  msg.attach(MIMEText(text))

  for file in filenames:
    part = MIMEBase('application', 'octet-stream')

    part.set_payload(open(file, 'rb').read())
    encode(part)

    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))

    msg.attach(part)

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.login(serveruser,serverpass)

  server.ehlo()
  server.starttls()

  server.sendmail(serveruser, clientusers, msg.as_string())

def read_conf(filename):
  file = open(filename, "rb").readlines()
  
