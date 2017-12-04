import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

now = datetime.datetime.now()
emailFileName = '{0}-{1}-{2}.txt'.format(now.month, now.day, now.year)
fileName = '{:02d}-{:02d}-{:02d}.json'.format(now.month, now.day, now.year)

class Table:

    def __init__(self):
        self.occupied = 'n'
        self.num = 1
        self.startTime = None
        self.endTime = None
        self.cost = 0
        self.totalTime = 0
        self.totalHours = ""

def getTotalHours(table):
    minsStart = (int(table.startTime[:2]) * 60) + (int(table.startTime[-2:]))
    minsEnd = (int(table.endTime[:2]) * 60) + (int(table.endTime[-2:]))
    return minsEnd - minsStart

def giveTable(table, finalDicts):
    while True:
        occ = raw_input('Enter "y" to make the table occupied, enter "n" to make it unoccupied: ')
        if occ.lower() == 'y':
            if table.occupied == 'y':
                print 'Pool Table {0} is currently occupied.'.format(table.num)
                break
            elif table.occupied == 'n':
                now = datetime.datetime.now()
                table.startTime = '{:02d}:{:02d}'.format(now.hour, now.minute)
                table.occupied = 'y'
                print 'Pool Table {0} is now occupied! The start time is {1}.'.format(table.num, table.startTime)
                break
        elif occ.lower() == 'n':
            if table.occupied == 'n':
                print 'This table is already empty! Please try again!'
                break
            if table.occupied == 'y':
                now = datetime.datetime.now()
                table.endTime = '{:02d}:{:02d}'.format(now.hour, now.minute)
                totalHours = getTotalHours(table)
                hours = totalHours / 60
                minutes = totalHours % 60
                table.occupied = 'n'
                table.cost = totalHours * .5
                table.totalHours = '{:02d}:{:02d}'.format(hours, minutes)
                table.cost = format(table.cost, '.2f')
                toDict, table = tableToDict(table)
                finalDicts.append(toDict)
                print 'Pool Table {0} is now no longer occupied! The end time is {1}.'.format(table.num, table.endTime)
                print "The total cost is ${0}.".format(str(table.cost))
                break
        else:
            print 'Please enter only "y" or "n".'

def jsonMakeOrPull(tableList):
    with open(fileName) as fileToUse:
        newList = json.load(fileToUse)
        arrayToArrayOne(newList, tableList)
        return tableList

def endJson(aList):
    with open(fileName, 'w') as fileToUse:
        json.dump(aList, fileToUse)

def dictToTable(tableDict):
    newTable = Table()
    newTable.occupied = tableDict['occupied']
    newTable.num = tableDict['num']
    newTable.startTime = tableDict['startTime']
    newTable.endTime = tableDict['endTime']
    newTable.cost = tableDict['cost']
    newTable.totalHours = tableDict['totalHours']
    return newTable

def arrayToArrayOne(oldList, newList):
    for item in oldList:
        newList.append(dictToTable(item))

def arrayToArrayTwo(oldList, newList):
    for item in oldList:
        newList.append(tableToDict(item))

def tableToDict(table):
    newDict = {'occupied' : table.occupied, 'num' : table.num, 'startTime' : table.startTime, 'endTime' : table.endTime, 'cost' : table.cost, 'totalHours' : table.totalHours}
    return newDict, table

def idTables(tableList, poolNum):
    for item in tableList:
        poolNum += 1
        item.num = poolNum

def findTable(idToFind, tableList):
    for t in tableList:
        if t.num == idToFind:
            return t

def setUp(tableList):
    for i in range(0,12):
        table = Table()
        tableList.append(table)

def printTableList(tableList):
    for item in tableList:
        toPrint = "TABLE {0} - ".format(item.num)
        if item.occupied == 'y':
            minsStart = (int(item.startTime[:2]) * 60) + (int(item.startTime[-2:]))
            now = datetime.datetime.now()
            minsNow = (now.hour * 60) + now.minute
            totalHrs = (minsNow - minsStart) / 60
            totalMins = (minsNow - minsStart) % 60
            toPrint += 'OCCUPIED - TIME PLAYED: {:02d}:{:02d}'.format(totalHrs, totalMins)
        elif item.occupied == 'n':
            toPrint += 'NOT OCCUPIED'
        print toPrint

def makeEmail(email):
    msg = MIMEMultipart()
    msg['Subject'] = 'Pool Table Status'
    msg['From'] = 'thegalliumspoon@gmail.com'
    msg['To'] = email
    msg.preamble = 'Pool table status document for {0}-{1}-{2}'.format(now.month, now.day, now.year)

    fj = open(emailFileName, 'r')
    table = MIMEText(fj.read())
    fj.close()
    msg.attach(table)

    return msg

def getTotalHoursNow(table):
    minsStart = (int(table.startTime[:2]) * 60) + (int(table.startTime[-2:]))
    now = datetime.datetime.now()
    minsEnd = (now.hour * 60) + (now.minute)
    return minsEnd - minsStart

def makeFile(tableList):
    toPrint = ""
    for table in tableList:
        #for tables who have been opened and closed and aren't in a session
        if table.endTime != None and table.occupied == 'n' and tableList.index(table) not in range(0,11):
            toPrint += "--------------------\n"
            toPrint += "TABLE {0}\n".format(str(table.num))
            toPrint += "START TIME: {0}\n".format(table.startTime)
            toPrint += "END TIME: {0}\n".format(table.endTime)
            toPrint += "TIME PLAYED: {0}\n".format(table.totalHours)
            toPrint += "COST: {0}\n".format(table.cost)
            toPrint += "--------------------\n"
        #for tables that have been opened and not closed
        elif table.occupied == 'y':
            toPrint += "--------------------\n"
            toPrint += "TABLE {0}\n".format(str(table.num))
            totalMins = getTotalHoursNow(table)
            toPrint += "START TIME: {0}\n".format(table.startTime)
            toPrint += "END TIME: N/A\n"
            toPrint += "TIME PLAYED: As of {:02d}:{:02d}, the total time played was {:02d}:{:02d}.\n".format(now.hour, now.minute, totalMins / 60, totalMins % 60)
            toPrint += "COST: ${0}\n".format(str(totalMins * .5))
            toPrint += "--------------------\n"
        #for tables that haven't been occupied
        elif table.endTime == None and table.occupied == 'n':
            toPrint += "--------------------\n"
            toPrint += "TABLE {0}\n".format(str(table.num))
            toPrint += "START TIME: N/A\n"
            toPrint += "END TIME: N/A\n"
            toPrint += "TIME PLAYED: N/A\n"
            toPrint += "--------------------\n"
    with open(emailFileName, 'w') as fileName:
        fileName.write(toPrint)
