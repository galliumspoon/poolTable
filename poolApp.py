import poolFunct as pool
import datetime
from poolFunct import Table
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

now = datetime.datetime.now()
emailFileName = '{0}-{1}-{2}.txt'.format(now.month, now.day, now.year)
poolNum = 0
tableList = []
finalDicts = []
newList = []

try:
    finalDicts = pool.jsonMakeOrPull(newList)
    pool.setUp(tableList)
except:
    pool.setUp(tableList)


pool.idTables(tableList, poolNum)

print("WELCOME TO YOUR POOL TABLE MANAGER")
print("Here are the pool tables: ")
pool.printTableList(tableList)

#altering tables
while True:
    userInp = raw_input("Enter a table number to alter its status or press q to quit: ")
    try:
        if userInp.lower() == 'q':
            break
        else:
            tableToAlt = pool.findTable(int(userInp), tableList)
            pool.giveTable(tableToAlt, finalDicts)
            print tableList
            pool.printTableList(tableList)
    except ValueError:
        print "Please only enter either a number or q."

pool.endJson(finalDicts)

newList = pool.jsonMakeOrPull(tableList)

while True:
    ynemail = raw_input("Would you like to email the log to someone? (y/n) ")
    if ynemail.lower() == 'y':
        while True:
            email = raw_input("Please enter an email: ")
            try:
                pool.makeFile(tableList)
                msg = pool.makeEmail(email)
                s = smtplib.SMTP('108.82.218.118', 22)
                s.sendmail('thegalliumspoon@gmail.com', email, msg.as_string())
                s.quit()
                break
            except smtplib.SMTPException:
                print 'Please enter a valid email.'
    elif ynemail.lower() == 'n':
        print 'Goodbye!'
        break
