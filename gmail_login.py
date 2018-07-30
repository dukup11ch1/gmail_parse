import socket
import imaplib
def gmail_login(username, password):
    IMAP_SERVER = imaplib.IMAP4_SSL(str(socket.gethostbyname('imap.gmail.com')),993)
    IMAP_SERVER.login(username, password)
    return IMAP_SERVER