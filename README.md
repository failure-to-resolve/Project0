PROJECT0:

Features:
Utilizing subject lines to pass encrypted commands to an already set payload
!!!Modular payload that can accept and deploy new functions quickly
!!!Edit your own modules to be sent straight to the payload, get real time feedback on whether they worked and the status
!!!A multi-threaded server capable of handling multiple clients in a handy GUI
!!!Turn your payloads into email proxies (may implement a small smtp/imap server into each payload for forwarding, see smtpd in python docs)
!!!Multi-platform, planned to work on everything that can run python code, and since it's modular you can pick and choose what to enumerate with
!!!Self deleting payloads: Are you compromised? Have you finished your testing? these payloads will take care of everything for a clean getaway...I mean clean report.


How does it work?
1. The client is deployed on the target machine
2. The server is started and populated with many email accounts(must be gmail for now, with imap enabled)
3. You get to pick and choose how you want your client to behave with different modules
4. Send the completed payload using the *fragmented command strings sent in the subject line of emails
5. The client parses the subject lines of the fragmented subject lines and then executes the selected function accordingly, anything from creating a listening
port to deploying a meterpreter payload from a hidden location in an attached image

*fragmented: command strings are first encoded with base64, then split into chunks, then encrypted using RSA 1024 public key encryption. This is then sent to the client using multiple emails and then reconstructed on the target machine

Best part is, since the email AND attachments are read directly into memory and can be acted upon accordingly, the follow-up payloads are COMPLETELY FILELESS


PS. I'm currently a student trying to make my way through college, so any support you can give me (from tips of the trade to straight up bitcoin) is absolutely appreciated.

Hope you enjoy my first tool. Enjoy!

Email:transaction.failed.0@gmail.com
BC: bc1qjcnmr0n6c711cn3emmf4h3wxjqawq5suz4yu6z
