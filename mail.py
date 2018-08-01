import imaplib
import re

class Mail:
    IHOSTS={'gmail':['imap.gmail.com',993], 'outlook':['imap-mail.outlook.com',993], 'yahoo':['imap.mail.yahoo.com',993], 'naver':['imap.naver.com',993]}
    SHOSTS={'gmail':['smtp.gmail.com',587], 'outlook':['smtp-mail.outlook.com',587], 'yahoo':['smtp.mail.yahoo.com',465], 'naver':['smtp.naver.com',587]}
    def __init__(self,host):
        self.user=None
        self.pw=None
        self.token=None

        self.imap=None
        self.smtp=None
        self.login=None
        self.mailboxes={}
        self.current_mailbox=None

        self.IMAP_HOST=self.IHOSTS[host][0]
        self.IMAP_PORT=self.IHOSTS[host][1]
        self.SMTP_HOST=self.SHOSTS[host][0]
        self.SMTP_PORT=self.SHOSTS[host][1]

    def setting_hosts(self,host,port):
        self.IMAP_HOST=0

    def connect(self):
        self.imap=imaplib.IMAP4_SSL(self.IMAP_HOST,self.IMAP_PORT)