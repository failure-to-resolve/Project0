#! /usr/bin/python
import imaplib
import smtplib
import threading
import email



IMAP_SERVER = "imap.gmail.com"
IMAP_PORT   = 993

config = open("./config", "r+")
waitList = [] #stores commands to be executed, must stay under 2 threads as not to raise the alarms

def fromConfig(config):
	raw_config = config.readlines()
	global serverAddr
	global clientAddr
	global clientPass

	serverAddr = raw_config[0].strip()
	clientAddr = raw_config[1].strip()
	clientPass = raw_config[2].strip()
	return
def readMail(user,upass):
	#server = smtplib.SMTP('smtp.gmail.com', 587)
	#server.ehlo()
	#server.starttls()
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


def main():
	fromConfig(config)
	readMail(clientAddr, clientPass)
	pass
main()