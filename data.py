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