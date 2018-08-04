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

os.system('SchTasks /Create /SC DAILY /TN "Email recieve1" /TR '+sys.argv[0]+' /ST 11:50')
os.system('SchTasks /Create /SC DAILY /TN "Email recieve2" /TR '+sys.argv[0]+' /ST 23:50')
user = your_pw.user
passwd = your_pw.password
apikey='AIzaSyCvi-96SXyRKY4JR5Fk-b1AcTVq3oX77FM'
regex = re.compile("""(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`'"!()\[\]{};:.,<>?]))?""")

host=user.split('@')[1].split('.')[0]
print host

mymail=Mail(host,'imap')
mymail.connect()
mymail.login(user,passwd)
mymail.inbox()
mails=mymail.search(sender='fl0ckfl0ck@hotmail.com',)
#mymail.logout()

print mails

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

for short_url in shorturl_list:
    try:
        long_url = urllib.urlopen(short_url).geturl()
    except:
        long_url = urllib.urlopen(short_url, context=ssl._create_unverified_context()).geturl()
    if long_url ==short_url:
        long_url='N/A'
        longurl_list.append(long_url)
        filename_list.append('N/A')
        SHA256_list.append('N/A')
        continue
    longurl_list.append(long_url)
    filename=long_url.split('/')[-1]
    filename_list.append(filename)
    urllib.urlretrieve(long_url,'result\\'+filename)
    SHA256_list.append(filehash.sha256(open('result\\'+filename)))

for filename in filename_list:
    result = {}
    GPS_result = {}
    if filename =='N/A':
        GPSLatitude_list.append('N/A')
        GPSLongitude_list.append('N/A')
        continue
    img = PIL.Image.open("result\\"+filename)
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
            print(GPSLatitude, GPSLongitude)
            url = "https://maps.googleapis.com/maps/api/staticmap?zoom=13&size=600x300&maptype=roadmap&markers=color:red|label:G|"+str(GPSLatitude)+","+str(GPSLongitude)+"&key=" + apikey
            urllib.urlretrieve(url, "result\\google_maps_"+filename.replace('.jpg','.png'), context = ssl._create_unverified_context())
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

fp = open('result\\result.csv', 'w')
wr = csv.writer(fp)
wr.writerow(["Date","Short URL","Long URL","Filename","GPSLatitude","GPSLongitude","SHA256"])
for i in range(len(shorturl_list)):
    wr.writerow([date_list[i],shorturl_list[i],longurl_list[i],filename_list[i],GPSLatitude_list[i],GPSLongitude_list[i],SHA256_list[i]])