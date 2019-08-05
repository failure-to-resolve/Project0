#! /usr/bin/python
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#from email.mime.base import MIMEBase
#from email.encoders import encode_base64

def run(clientusers, serveruser, serverpass, subject, text, filenames):
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
