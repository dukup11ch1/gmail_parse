import datetime
import email
import re
import time
import os
from email.header import decode_header, make_header
from imaplib import ParseFlags

class Message():
    def __init__(self, mailbox, uid):
        self.uid = uid
        self.mailbox = mailbox if mailbox else None

        self.message = None
        self.headers = {}

        self.subject = None
        self.body = None
        self.html = None

        self.to = None
        self.fr = None
        self.cc = None
        self.delivered_to = None

        self.sent_at = None

        self.flags = []
        self.labels = []

        self.thread_id = None
        self.thread = []
        self.message_id = None
 
        self.attachments = None

    def parse_headers(self, message):
        hdrs = {}
        for hdr in message.keys():
            hdrs[hdr] = message[hdr]
        return hdrs

    def parse_flags(self, headers):
        return list(ParseFlags(headers))

    def parse_labels(self, headers):
        if re.search(r'X-GM-LABELS \(([^\)]+)\)', headers):
            labels = re.search(r'X-GM-LABELS \(([^\)]+)\)', headers).groups(1)[0].split(' ')
            return map(lambda l: l.replace('"', '').decode("string_escape"), labels)
        else:
            return list()

    def parse_subject(self, encoded_subject):
        dh = decode_header(encoded_subject)
        default_charset = 'ASCII'
        return ''.join([ unicode(t[0], t[1] or default_charset) for t in dh ])

    def parse(self, raw_message):
        raw_headers = raw_message[0]
        raw_email = raw_message[1]

        self.message = email.message_from_string(raw_email)
        self.headers = self.parse_headers(self.message)

        self.to = self.message['to']
        self.fr = self.message['from']
        self.delivered_to = self.message['delivered_to']

        self.subject = self.parse_subject(self.message['subject'])

        if self.message.get_content_maintype() == "multipart":
            for content in self.message.walk():
                if content.get_content_type() == "text/plain":
                    self.body = content.get_payload(decode=True)
                elif content.get_content_type() == "text/html":
                    self.html = content.get_payload(decode=True)
        elif self.message.get_content_maintype() == "text":
            self.body = self.message.get_payload()

        self.sent_at = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate_tz(self.message['date'])[:9]))

        self.flags = self.parse_flags(raw_headers)

        self.labels = self.parse_labels(raw_headers)

        if re.search(r'X-GM-THRID (\d+)', raw_headers):
            self.thread_id = re.search(r'X-GM-THRID (\d+)', raw_headers).groups(1)[0]
        if re.search(r'X-GM-MSGID (\d+)', raw_headers):
            self.message_id = re.search(r'X-GM-MSGID (\d+)', raw_headers).groups(1)[0]

        self.attachments = [
            Attachment(attachment) for attachment in self.message._payload
                if not isinstance(attachment, basestring) and attachment.get('Content-Disposition') is not None
        ]
        

    def fetch(self):
        if not self.message:
            _, results = self.mailbox.proto.uid('FETCH', self.uid, '(BODY.PEEK[] FLAGS X-GM-THRID X-GM-MSGID X-GM-LABELS)')

            self.parse(results[0])

        return self.message

    def fetch_thread(self):
        self.fetch()
        original_mailbox = self.mailbox
        self.mailbox.use_mailbox(original_mailbox.name)

        response, results = self.mailbox.proto.uid('SEARCH', None, '(X-GM-THRID ' + self.thread_id + ')')
        received_messages = {}
        uids = results[0].split(' ')
        if response == 'OK':
            for uid in uids: received_messages[uid] = Message(original_mailbox, uid)
            self.mailbox.fetch_multiple_messages(received_messages)
            self.mailbox.messages.update(received_messages)

        self.mailbox.use_mailbox('[Gmail]/Sent Mail')
        response, results = self.mailbox.proto.uid('SEARCH', None, '(X-GM-THRID ' + self.thread_id + ')')
        sent_messages = {}
        uids = results[0].split(' ')
        if response == 'OK':
            for uid in uids: sent_messages[uid] = Message(self.mailbox.mailboxes['[Gmail]/Sent Mail'], uid)
            self.mailbox.fetch_multiple_messages(sent_messages)
            self.mailbox.mailboxes['[Gmail]/Sent Mail'].messages.update(sent_messages)

        self.mailbox.use_mailbox(original_mailbox.name)

        return sorted(dict(received_messages.items() + sent_messages.items()).values(), key=lambda m: m.sent_at)


class Attachment:

    def __init__(self, attachment):
        self.name = attachment.get_filename()
        self.payload = attachment.get_payload(decode=True)
        self.size = int(round(len(self.payload)/1000.0))

    def save(self, path=None):
        if path is None:
            path = self.name
        elif os.path.isdir(path):
            path = os.path.join(path, self.name)

        with open(path, 'wb') as f:
            f.write(self.payload)
