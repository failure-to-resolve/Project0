+------+  +--------------+
|Server|->|Command Server|--------+
+------+  +--------------+        |
   |                              |
   ----------------------------+  |
                               |  V
+------+                    +----------+
|Client|<------------------>|Mail Server|
+------+                    +-----------+

1. Server is started(monitors and updates display with data read from email)
2. Client is deployed(executable, ELF, apk, etc.)
3. Client requests initial config file(base64 encoded)
4. Client requests additional modules
5. Repeat from 2

Client Commands available:
  Shell: Opens local shell on client computer
  Tree: Show full directory tree on host
  Update: Allows the server to send a new configuration file, configuration file must be in the body of the message, base64 encoded
  Isup: Sends a reply to server with the public and private ip addresses
  User [passwords/webcam/screenshot/process]: Grab passwords,take picture through webcam, take screenshot, get process list
  Die: Deletes the clients code and removes all traces from host pc
  Network [time] [interface]: capture traffic on the specified interface for [time] number of seconds
  Fuckyou: Encrypt everything on the host, no decryption phrase available
  Imbroke: Encrypt everything BUT send the decryption phrase back to the server, Display a "Gentle Persuasion" page on host with input box
  Delete [filepath]: Delete file from host pc
  Touch [filepath]: Place the attached file into the specified directory
  Disable [keyboard/mouse/display]: Makes the specified device unavailable#EXTREMELY EXPERIMENTAL, USE AT OWN RISK
  Enable [keyboard/mouse/display]: Makes the unavailable device usable again #EXTREMELY EXPERIMENTAL, USE AT OWN RISK

Server commands:
  Refresh: Send Isup to all clients
  Killall: Sends Die to all clients
  Showme: Display most recent screenshot of specified host
  RIP: Do not use unless you are compromised, irreversibly encrypts everything, on every host, on every server, on every proxy. This is a last resort


Alternatively:

+------+  +--------------+
|Server|->|Command Server|--------+
+------+  +--------------+        V
   |                         +-----+            +-----+
   +------------------------>|Proxy|<---------->|Proxy|
                             +-----+            +-----+
                                                   |
+------+                    +-----------+          |
|Client|<------------------>|Mail Server|<---------+
+------+                    +-----------+

Proxy commands:
  Setdown: set the senders email address
  Setup: set the receivers email address
  Change: Change the proxy email account
**OR**
  SetChain: Creates a chain configuration file
  AddLink: Adds a sender/reciever to the chain file, must include full username and password, encoded before transmit
