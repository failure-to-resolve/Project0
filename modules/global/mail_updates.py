#! /usr/bin/python2


import sys,os,re,glob,pwd,itertools
import smtplib

from requests import get

f = open("update_number.txt", 'rw+')
number = f.readlines()
number = number[-1]
new_number = int(number) + 1
f.write(str(new_number) + "\n")
f.close()


external_ip = get('https://api.ipify.org').text

gmail_user = 'PLACEHOLDER'
gmail_password = 'PLACEHOLDER'

sent_from = gmail_user
to = gmail_user
subject = 'Update #%s' % number
process_list = []
connection_list = []



class LinuxProcess:
  def __init__(self,pid):
    fd = open("/proc/"+pid+"/stat","rb")
    self.stat = fd.read().split()
    self.name = self.stat[1].strip("()")
    self.status = self.stat[2]

class LinuxProcList:
  def __init__(self):
    global body

  def proclist(self):
    proc = next(os.walk('/proc/'))[1]
    procNum = []
    for i in proc:
     if i.isdigit():
       procNum.append(i)
    return procNum
  def cmdline(self,pid):
    try:
      fd = open("/proc/"+str(pid)+"/cmdline","rb")
      cmdLine = fd.read()
      return cmdLine.replace("\0"," ")
    except:
      return None
  def children(self,pid):
    kids = []
    for i in self.proclist():
      try:
        if int(open("/proc/"+i+"/stat","rb").read().split()[3]) == int(pid):
          kids.append(i)
      except:
        pass
    return kids
    pass

def printTree(parent,children,depth=0):
  if parent not in printed:
    spaces = 10-len(parent)
    status=LinuxProcess(parent).status
    if len(status)>1:
      status='?'
    if depth==0:
      process_list.append(parent+' '*(spaces+5)+status+' '*7+'|>'+' '+LinuxProcess(parent).name+' '+procList.cmdline(parent)[0:40]+' '+"\n")
    elif depth == 1:
      process_list.append(parent+' '*(spaces+5)+status+' '*7+'|>'+'-'*depth*3+'+ '+LinuxProcess(parent).name+' '+procList.cmdline(parent)[0:40]+"\n")
    elif depth == 2:
      process_list.append(parent+' '*(spaces+5)+status+' '*7+'|'+' '*depth*3+'`-+ '+LinuxProcess(parent).name+' '+procList.cmdline(parent)[0:40]+"\n")
    else:
      process_list.append(parent+' '*(spaces+5)+status+' '*7+'|'+' '*depth*3+'`-'+'-'*3+'+ '+LinuxProcess(parent).name+' '+procList.cmdline(parent)[0:40]+"\n")

    printed.append(parent)
    if children:
      for child in children:
         printTree(child,process[child],depth+1)
    else:
      return
def printHeaders():
  process_list.append("PID"+' '*7+"| STATUS "+"| PROCESS\n")
  process_list.append('-'*28 + "\n")

procList = LinuxProcList()

process = dict(zip(procList.proclist(),(procList.children(x) for x in procList.proclist())))

printed = []
keylist = process.keys()
keylist.sort(key=int)
printHeaders()


for x in keylist:
  printTree(x,process[x])

PROC_TCP = "/proc/net/tcp"
STATE = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        }

def _load():
    ''' Read the table of tcp connections & remove header  '''
    with open(PROC_TCP,'r') as f:
        content = f.readlines()
        content.pop(0)
    return content

def _hex2dec(s):
    return str(int(s,16))

def _ip(s):
    ip = [(_hex2dec(s[6:8])),(_hex2dec(s[4:6])),(_hex2dec(s[2:4])),(_hex2dec(s[0:2]))]
    return '.'.join(ip)

def _remove_empty(array):
    return [x for x in array if x !='']

def _convert_ip_port(array):
    host,port = array.split(':')
    return _ip(host),_hex2dec(port)

def netstat():
    '''
    Function to return a list with status of tcp connections at linux systems
    To get pid of all network process running on system, you must run this script
    as superuser
    '''

    content=_load()
    result = []
    for line in content:
        line_array = _remove_empty(line.split(' '))     # Split lines and remove empty spaces.
        l_host,l_port = _convert_ip_port(line_array[1]) # Convert ipaddress and port from hex to decimal.
        r_host,r_port = _convert_ip_port(line_array[2])
        tcp_id = line_array[0]
        state = STATE[line_array[3]]
        uid = pwd.getpwuid(int(line_array[7]))[0]       # Get user from UID.
        inode = line_array[9]                           # Need the inode to get process pid.
        pid = _get_pid_of_inode(inode)                  # Get pid prom inode.
        try:                                            # try read the process name.
            exe = os.readlink('/proc/'+pid+'/exe')
        except:
            exe = None

        nline = [tcp_id,' ', uid,' ', l_host+':'+l_port,' ', r_host+':'+r_port,' ', state,' ', pid,' ', exe,' ']
        result.append(nline)
    return result

def _get_pid_of_inode(inode):
    '''
    To retrieve the process pid, check every running process and look for one using
    the given inode.
    '''
    for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
        try:
            if re.search(inode,os.readlink(item)):
                return item.split('/')[2]
        except:
            pass
    return None

for conn in netstat():
  connection_list.extend(conn)
  connection_list.append("\n")
print connection_list

#fix this
key = lambda sep: sep == '\n'
con_list = [list(group) for is_key, group in itertools.groupby(connection_list,"\n") if not is_key]

print con_list

try:
  body = external_ip+"\n"+"".join(process_list)+"\n"+"".join(connection_list)
except:
  body = external_ip+"\n"+"".join(process_list)+"\n"+str(connection_list)


email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

server = smtplib.SMTP('smtp.gmail.com', 587)

server.ehlo()
server.starttls()

server.login("transaction.failed.0@gmail.com", "excel4t1t")

server.sendmail(gmail_user,gmail_user,email_text)

