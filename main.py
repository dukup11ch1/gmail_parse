#-*-coding: utf-8-*-
import os
import sys
import email
import imaplib
import time
import base64
import re
import gmail
from email.parser import HeaderParser


reload(sys)
sys.setdefaultencoding("utf-8")


user = 'id'
passwd = 'pw'

g = gmail.login(user, passwd)

g.inbox().mail()