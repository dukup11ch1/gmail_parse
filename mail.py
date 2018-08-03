import imaplib
import smtplib
#import email
from message import Message
import re

class Mail:
    IHOSTS={'gmail':['imap.gmail.com',993], 'outlook':['imap-mail.outlook.com',993], 'yahoo':['imap.mail.yahoo.com',993], 'naver':['imap.naver.com',993]}
    SHOSTS={'gmail':['smtp.gmail.com',587], 'outlook':['smtp-mail.outlook.com',587], 'yahoo':['smtp.mail.yahoo.com',465], 'naver':['smtp.naver.com',587]}
    def __init__(self,host,proto):
        self.user=None
        self.pw=None
        self.token=None

        self.proto=proto
        self.login_suc=None
        self.mailboxes={}
        self.current_mailbox=None

        #seting host and port
        self.host=host
        if self.proto=='imap':
            self.IMAP_HOST=self.IHOSTS[host][0]
            self.IMAP_PORT=self.IHOSTS[host][1]
        elif self.proto=='smtp':
            self.SMTP_HOST=self.SHOSTS[host][0]
            self.SMTP_PORT=self.SHOSTS[host][1]
        self.messages={}
        return

    def connect(self):
        if self.proto=='imap':
            self.proto=imaplib.IMAP4_SSL(self.IMAP_HOST,self.IMAP_PORT)
        elif self.proto=='smtp':
            self.proto=smtplib.SMTP_SSL(self.SMTP_HOST,self.SMTP_PORT)
        return
    
    def login(self,username,password):
        self.user=username
        self.pw=password
        self.connect()
        try:
            login=self.proto.login(self.user,self.pw)
        except Exception as e:
            print e
            exit()
        return login
    
    def logout(self):
        self.proto.logout()
    
    def inbox(self):
        self.proto.list()
        inb=self.proto.select('inbox')
        return inb

    def search(self,prefetch=False,**kwargs):
        search = ['ALL']

        kwargs.get('read')   and search.append('SEEN')
        kwargs.get('unread') and search.append('UNSEEN')

        kwargs.get('starred')   and search.append('FLAGGED')
        kwargs.get('unstarred') and search.append('UNFLAGGED')

        kwargs.get('deleted')   and search.append('DELETED')
        kwargs.get('undeleted') and search.append('UNDELETED')

        kwargs.get('draft')   and search.append('DRAFT')
        kwargs.get('undraft') and search.append('UNDRAFT')

        kwargs.get('header') and search.extend(['HEADER', kwargs.get('header')[0], kwargs.get('header')[1]])

        kwargs.get('sender') and search.extend(['FROM', kwargs.get('sender')])
        kwargs.get('fr') and search.extend(['FROM', kwargs.get('fr')])
        kwargs.get('to') and search.extend(['TO', kwargs.get('to')])
        kwargs.get('cc') and search.extend(['CC', kwargs.get('cc')])

        kwargs.get('subject') and search.extend(['SUBJECT', kwargs.get('subject')])
        kwargs.get('body') and search.extend(['BODY', kwargs.get('body')])

        kwargs.get('label') and search.extend(['X-GM-LABELS', kwargs.get('label')])
        kwargs.get('attachment') and search.extend(['HAS', 'attachment'])

        kwargs.get('query') and search.extend([kwargs.get('query')])
        #print search
        emails = []
        response, data = self.proto.uid('SEARCH', *search)
        if response=='OK':
            uids = filter(None, data[0].split(' '))

            if self.host=='gmail':
                for uid in uids:
                    if not self.messages.get(uid):
                        self.messages[uid] = Message(self, uid)
                    emails.append(self.messages[uid])
                #print emails
            else :
                for num in data[0].split():
                    _, data = self.proto.fetch(num, '(RFC2045)')
                    #print 'Message %s\n%s\n' % (num, data[0][1])
        else:
            print 'Find Email fail...'
            exit()
        return emails
