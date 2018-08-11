class Fileinfo:
    def __init__(self,shorturl,longurl,date,filename,GPSLatitude,GPSLongitude,SHA256):
        self.shorturl=shorturl
        self.longurl=longurl
        self.date=date
        self.filename=filename
        self.GPSLatitude=GPSLatitude
        self.GPSLongitude=GPSLongitude
        self.SHA256=SHA256
    
    def shorturl_value(self,value=None):
        if value != None:
            self.shorturl=value
            return
        return self.shorturl
    
    def longurl_value(self,value=None):
        if value != None:
            self.longurl=value
            return
        return self.longurl
    
    def date_value(self,value=None):
        if value != None:
            self.date=value
            return
        return self.date
    
    def filename_value(self,value=None):
        if value != None:
            self.filename=value
            return
        return self.filename
    
    def GPSLatitude_value(self,value=None):
        if value != None:
            self.GPSLatitude=value
            return
        return self.GPSLatitude
    
    def GPSLongitude_value(self,value=None):
        if value != None:
            self.GPSLongitude=value
            return
        return self.GPSLongitude
    
    def SHA256_value(self,value=None):
        if value != None:
            self.SHA256=value
            return
        return self.SHA256
    
class Print:
    def __init__(self,data):
        self.data=data

    def csv(self):
        import csv
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")
        fp = open('result\\result.csv','wb')
        wr = csv.writer(fp)
        wr.writerow(["Date","Short URL","Long URL","Filename","GPSLatitude","GPSLongitude","SHA256"])
        for d in self.data:
            wr.writerow([d.date_value(),d.shorturl_value(),d.longurl_value(),d.filename_value(),d.GPSLatitude_value(),d.GPSLongitude_value(),d.SHA256_value()])
    
    def map(self):
        import urllib
        import ssl
        maker_list=""
        for GPS in self.data:
            if GPS.GPSLatitude_value()=="N/A":
                continue
            maker_list=maker_list+str(GPS.GPSLatitude_value())+','+str(GPS.GPSLongitude_value())+'|'

        url = "https://maps.googleapis.com/maps/api/staticmap?zoom=1&size=600x300&maptype=roadmap&markers=color:red|"+maker_list
        #print url
        urllib.urlretrieve(url, 'result\\google_maps_result.png', context = ssl._create_unverified_context())

class Data:
    def __init__(self,date,short_url,curdir):
        self.short_url=short_url
        self.date=date
        self.curdir=curdir
        return
    
    def make_data(self):
        import urllib
        import ssl
        import unicodedata
        import filehash
        import PIL.Image
        from PIL.ExifTags import TAGS, GPSTAGS
        import dataconvert
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")
        try:
            long_url = urllib.urlopen(self.short_url).geturl()
        except:
            long_url = urllib.urlopen(self.short_url, context=ssl._create_unverified_context()).geturl()
            long_url = urllib.unquote(long_url).decode('utf-8')
        if long_url == self.short_url:
            long_url='N/A'
            filename='N/A'
            SHA256='N/A'
            GPSLatitude='N/A'
            GPSLongitude='N/A'
            return Fileinfo(self.short_url,long_url,self.date,filename,GPSLatitude,GPSLongitude,SHA256)
        filename=unicodedata.normalize("NFC", unicode(urllib.unquote(long_url.split('/')[-1])))
        #print filename
        #filename=filename.encode('utf-8')
        urllib.urlretrieve(long_url,'result\\'+self.curdir+'\\'+filename)
        SHA256=filehash.sha256('result\\'+self.curdir+'\\'+filename)
        result = {}
        GPS_result = {}
        img = PIL.Image.open('result\\'+self.curdir+'\\'+filename)
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
                GPSLatitude = dataconvert.float_location(GPSLatitude)
                GPSLongitude = dataconvert.float_location(GPSLongitude)
                #print(GPSLatitude, GPSLongitude)
            except:
                GPSLatitude = 'N/A'
                GPSLongitude = 'N/A'
        else:
            GPSLatitude = 'N/A'
            GPSLongitude = 'N/A'
        return Fileinfo(self.short_url,long_url,self.date,filename,GPSLatitude,GPSLongitude,SHA256)