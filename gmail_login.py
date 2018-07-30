import smtplib

def gmail_login(id,pw):
    server = smtplib.SMTP('smtp.gmail.com',587) #this is gmail 
    server.ehlo()
    server.starttls()
    server.login(id,pw)
    print 'login success'
    return server
