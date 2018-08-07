import hashlib

def sha1(fname):
    fp=open(fname,'rb')
    data=fp.read()
    fp.close()
    hash=hashlib.sha1(data)
    return hash.hexdigest()

def md5(fname):
    fp=open(fname,'rb')
    data=fp.read()
    fp.close()
    hash=hashlib.sha1(data)
    return hash.hexdigest()

def sha256(fname):
    fp=open(fname,'rb')
    data=fp.read()
    fp.close()
    hash=hashlib.sha256(data)
    return hash.hexdigest()

def sha512(fname):
    fp=open(fname,'rb')
    data=fp.read()
    fp.close()
    hash=hashlib.sha512(data)
    return hash.hexdigest()