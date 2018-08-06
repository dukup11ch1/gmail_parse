#-*-coding: utf-8-*-
import sys
from mail import Mail
import ssl
import re
import time
import urllib
import csv
import PIL.Image
from PIL.ExifTags import TAGS, GPSTAGS
import filehash
import your_pw
import os

reload(sys)
sys.setdefaultencoding("utf-8")
def float_location(data):
    d = float(data[0][0]) / float(data[0][1])
    m = float(data[1][0]) / float(data[1][1])
    s = float(data[2][0]) / float(data[2][1])

    return d + (m / 60.0) + (s / 3600.0)

now = time.localtime()
curdir="%04d_%02d_%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

os.system('SchTasks /Create /SC DAILY /TN "Email recieve1" /TR '+sys.argv[0]+' /ST 11:50')
os.system('SchTasks /Create /SC DAILY /TN "Email recieve2" /TR '+sys.argv[0]+' /ST 23:50')
os.system('mkdir '+'result\\'+curdir)
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
longurl_list=[]
date_list=[]
filename_list=[]
GPSLatitude_list=[]
GPSLongitude_list=[]
SHA256_list=[]

for mm in mails:
    mm.fetch()
    #print mm.body
    #print mm.headers["Date"]
    date_list.append(mm.headers["Date"])
    exurl=regex.search(mm.body)
    if exurl != None:
        if not (exurl in shorturl_list):
            shorturl_list.append(exurl.group())
    #print date_list
#print shorturl_list
mymail.logout()
for short_url in shorturl_list:
    try:
        long_url = urllib.urlopen(short_url).geturl()
    except:
        long_url = urllib.urlopen(short_url, context=ssl._create_unverified_context()).geturl()
        long_url = urllib.unquote(long_url).decode('utf-8')
    if long_url ==short_url:
        long_url='N/A'
        longurl_list.append(long_url)
        filename_list.append('N/A')
        SHA256_list.append('N/A')
        continue
    
    longurl_list.append(long_url)
    filename=urllib.unquote(long_url.split('/')[-1]).decode('utf-8')
    #print filename
    #filename=filename.encode('utf-8')
    filename_list.append(filename)
    urllib.urlretrieve(long_url,'result\\'+curdir+'\\'+filename)
    SHA256_list.append(filehash.sha256(open('result\\'+curdir+'\\'+filename)))

for filename in filename_list:
    result = {}
    GPS_result = {}
    if filename =='N/A':
        GPSLatitude_list.append('N/A')
        GPSLongitude_list.append('N/A')
        continue
    img = PIL.Image.open('result\\'+curdir+'\\'+filename)
    exif_data = img._getexif()
    if exif_data != None:  
        for tag, value in exif_data.items():
            name = TAGS.get(tag, tag)
            if name == "GPSInfo":
                for i in value:
                    GPS = GPSTAGS.get(i, i)
                    GPS_result[GPS] = value[i]
                result[name] = GPS_result
            else:
                result[name] = value
        try:
            GPSLatitude = result['GPSInfo']['GPSLatitude']
            GPSLongitude = result['GPSInfo']['GPSLongitude']
            GPSLatitude = float_location(GPSLatitude)
            GPSLongitude = float_location(GPSLongitude)
            #print(GPSLatitude, GPSLongitude)
        except:
            GPSLatitude = 'N/A'
            GPSLongitude = 'N/A'
    else:
        GPSLatitude = 'N/A'
        GPSLongitude = 'N/A'
    GPSLatitude_list.append(GPSLatitude)
    GPSLongitude_list.append(GPSLongitude)
    #print GPSLatitude_list
    #print GPSLongitude_list
"""
url = "https://maps.googleapis.com/maps/api/staticmap?zoom=3&size=600x300&maptype=roadmap&markers=color:red|label:G|"+str(GPSLatitude)+","+str(GPSLongitude)
#print url
urllib.urlretrieve(url, 'result\\'+curdir+'\\google_maps_'+filename.replace('.jpg','.png'), context = ssl._create_unverified_context())
"""
maker_list=""
for i in range(len(GPSLatitude_list)):
    if GPSLatitude_list[i]=="N/A":
        continue
    maker_list=maker_list+str(GPSLatitude_list[i])+','+str(GPSLongitude_list[i])+'|'

url = "https://maps.googleapis.com/maps/api/staticmap?zoom=1&size=600x300&maptype=roadmap&markers=color:red|label:G|"+maker_list
#print url
urllib.urlretrieve(url, 'result\\'+curdir+'\\google_maps_result.png', context = ssl._create_unverified_context())

fp = open('result\\'+curdir+'\\result.csv', 'w')
wr = csv.writer(fp)
wr.writerow(["Date","Short URL","Long URL","Filename","GPSLatitude","GPSLongitude","SHA256"])
for i in range(len(shorturl_list)):
    wr.writerow([date_list[i],shorturl_list[i],longurl_list[i],filename_list[i],GPSLatitude_list[i],GPSLongitude_list[i],SHA256_list[i]])