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
def float_location(data):
    d = float(data[0][0]) / float(data[0][1])
    m = float(data[1][0]) / float(data[1][1])
    s = float(data[2][0]) / float(data[2][1])

    return d + (m / 60.0) + (s / 3600.0)

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
    try:
        long_url = urllib.urlopen(short_url).geturl()
    except:
        long_url = urllib.urlopen(short_url, context=ssl._create_unverified_context()).geturl()
        long_url = urllib.unquote(long_url).decode('utf-8')
    if long_url ==short_url:
        long_url='N/A'
        filename='N/A'
        SHA256='N/A'
        GPSLatitude='N/A'
        GPSLongitude='N/A'
        data.append(Fileinfo(short_url,long_url,date,filename,GPSLatitude,GPSLongitude,SHA256))
        continue
    curdir=date
    filename=unicodedata.normalize("NFC", unicode(urllib.unquote(long_url.split('/')[-1])))
    #print filename
    #filename=filename.encode('utf-8')
    urllib.urlretrieve(long_url,'result\\'+curdir+'\\'+filename)
    SHA256=filehash.sha256('result\\'+curdir+'\\'+filename)
    result = {}
    GPS_result = {}
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
    data.append(Fileinfo(short_url,long_url,date,filename,GPSLatitude,GPSLongitude,SHA256))
    #print GPSLatitude_list
    #print GPSLongitude_list
"""
url = "https://maps.googleapis.com/maps/api/staticmap?zoom=3&size=600x300&maptype=roadmap&markers=color:red|label:G|"+str(GPSLatitude)+","+str(GPSLongitude)
#print url
urllib.urlretrieve(url, 'result\\'+curdir+'\\google_maps_'+filename.replace('.jpg','.png'), context = ssl._create_unverified_context())
"""
maker_list=""
for GPS in data:
    if GPS.GPSLatitude_value()=="N/A":
        continue
    maker_list=maker_list+str(GPS.GPSLatitude_value())+','+str(GPS.GPSLongitude_value())+'|'

url = "https://maps.googleapis.com/maps/api/staticmap?zoom=1&size=600x300&maptype=roadmap&markers=color:red|label:G|"+maker_list
#print url
urllib.urlretrieve(url, 'result\\google_maps_result.png', context = ssl._create_unverified_context())

fp = open('result\\result.csv', 'w')
wr = csv.writer(fp)
wr.writerow(["Date","Short URL","Long URL","Filename","GPSLatitude","GPSLongitude","SHA256"])
for d in data:
    wr.writerow([d.date_value(),d.shorturl_value(),d.longurl_value(),d.filename_value(),d.GPSLatitude_value(),d.GPSLongitude_value(),d.SHA256_value()])