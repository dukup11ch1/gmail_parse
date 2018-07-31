import os
import sys
import gmail_login
import email
import imaplib
import time
import base64
from email.parser import HeaderParser

user = 'Secret'
passwd = 'Secret'

def getMessages(server):
    server.select()
    _, data = server.search(None, 'All')
    return data[0].split()

try :
    myserver=gmail_login.gmail_login(user,passwd)
except:
    print 'fail'

print myserver

PARSER = HeaderParser()
read=set()
while True:
        ids = getMessages(myserver)
        for email_id in ids:
            resp, data = myserver.fetch(email_id, '(RFC822)')
            mail = email.message_from_string(data[0][1])
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                if part.get_content_subtype() != 'plain':
                    continue

                payload = part.get_payload()
                if not payload in read:
                    print "New message"
                    read.add(payload)
                    msg = PARSER.parsestr(data[0][1])
                    print payload
                    payload=payload.replace('\r\n','')
                    print '======================================================='
                    print payload
                    print '======================================================='
                    print payload.decode('base64')
                time.sleep(2)

        time.sleep(1)