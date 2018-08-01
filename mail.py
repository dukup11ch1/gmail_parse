import imaplib
import re

class Mail:
    #imap setting
    IHOSTS={'gmail':['imap.gmail.com',993], 'outlook':['imap-mail.outlook.com',993], 'yahoo':['imap.mail.yahoo.com',993], 'naver':['imap.naver.com',993]}
    IMAP_HOST=''
    IMAP_PORT=0
    
    #smtp setting
    SMTP_HOST=''
    SMTP_PORT=0
    def __init__(self):
        self.user=None
        self.pw=None
        self.token=None

        self.imap=None
        self.smtp=None
        self.login=None
        self.mailboxes={}
        self.current_mailbox=None
    
    def setting_hosts(self,host,port):
        self.IMAP_HOST=0

    def connect(self):
        self.imap=imaplib.IMAP4_SSL(self.IMAP_HOST,self.IMAP_PORT)