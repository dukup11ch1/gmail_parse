import socket
import imaplib

def gmail_login(username, password):
    IMAP_SERVER = imaplib.IMAP4_SSL(str(socket.gethostbyname('imap.gmail.com')),993)
    IMAP_SERVER.login(username, password)
    print 'login success'
    return IMAP_SERVER

def yahoo_login(username, password):
    IMAP_SERVER = imaplib.IMAP4_SSL(str(socket.gethostbyname('imap.mail.yahoo.com')),993)
    IMAP_SERVER.login(username, password)
    print 'login success'
    return IMAP_SERVER

def aol_login(username, password):
    IMAP_SERVER = imaplib.IMAP4_SSL(str(socket.gethostbyname('imap.aol.com')),993)
    IMAP_SERVER.login(username, password)
    print 'login success'
    return IMAP_SERVER
