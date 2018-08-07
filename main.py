#-*-coding: utf-8-*-
import sys
from mail import Mail
from data import *
import ssl
import re
import urllib
import csv
import PIL.Image
from PIL.ExifTags import TAGS, GPSTAGS
import filehash
import your_pw
import unicodedata
import os

reload(sys)
sys.setdefaultencoding("utf-8")


month_dic={'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

os.system('SchTasks /Create /SC DAILY /TN "Email recieve1" /TR '+sys.argv[0]+' /ST 11:50')
os.system('SchTasks /Create /SC DAILY /TN "Email recieve2" /TR '+sys.argv[0]+' /ST 23:50')

user = your_pw.user
passwd = your_pw.password
regex = re.compile("""(https?:\/\/).?(bitly.kr)\/([a-zA-Z0-9]{4})|(https?:\/\/).?(bit.ly)\/([a-zA-Z0-9]{7})|(https?:\/\/).?(goo.gl)\/([a-zA-Z0-9]{6})|(https?:\/\/).?(me2.do)\/([a-zA-Z0-9]{8})|(https?:\/\/).?(grep.kr)\/([a-zA-Z0-9]{4})|(https?:\/\/).?(hoy.kr)\/([a-zA-Z0-9]{4})""")

host=user.split('@')[1].split('.')[0]
#print host

mymail=Mail(host,'imap')
mymail.connect()
mymail.login(user,passwd)
mymail.inbox()
mails=mymail.search(sender='fl0ckfl0ck@hotmail.com')
#mymail.logout()

#print mails
shorturl_list=[]
data=[]

for mm in mails:
    mm.fetch()
    #print mm.body
    #print mm.headers["Date"]
    date=mm.headers["Date"].split(' ')
    day=('%02d'%int(date[1]))
    date=date[3]+'_'+month_dic[date[2]]+'_'+day
    os.system('mkdir '+'result\\'+date)
    exurl=regex.search(mm.body)
    if exurl != None:
        if not (exurl in shorturl_list):
            short_url=exurl.group()
            shorturl_list.append(short_url)
    a=Data(date,short_url)
    data.append(a.make_data())
    #print GPSLatitude_list
    #print GPSLongitude_list

pr=Print(data)
pr.map()
pr.csv()