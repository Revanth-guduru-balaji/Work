import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
import collections, operator
from collections import defaultdict
from datetime import datetime
import itertools

days = ("M","T","W","R","F","S","U")
startTimes = []

def fixDayStr(s):
    new1 = s.replace("Tu","T")
    new2 = new1.replace("Th","R")
    new3 = new2.replace("Sa","S")
    new4 = new3.replace("Su","U")
    return new4

def classMinutes(SoCstr):
    #Error check!!???
    toks = SoCstr.split('-')
    classStart = toks[0].strip()
    classEnd = toks[1].strip()

    FMT = '%I:%M %p'
    try:
        tdelta = datetime.strptime(classEnd, FMT) - datetime.strptime(classStart, FMT)
        tStr = str(tdelta)
        #print tStr
        h, m, s = [int(i) for i in tStr.split(':')]
    except:
        h = 0
        m = 0
        s= 0
    return((h*60) + m)

def classDayCount(SoCstr):
    # determine number of days per week class meets
    # watch out: SQL version has Tu and Th and Sa and Su
    numDays = 0
    for c in SoCstr:
        if (c == 'M' or c == 'T' or c == 'W' or c == 'R' or c == 'F'):
            numDays += 1
    return numDays

def parseTimeSlots(timeStr):
    # we want to know the starting time slot (7 AM = 0)
    # and the duration in 5-minute blocks
    fmt = '%I:%M %p'

    zeroTime = datetime.strptime("07:00 AM",fmt)
    
    toks = timeStr.split('-')
    startStr = toks[0].strip()
    endStr = toks[1].strip()

    start = datetime.strptime(startStr, fmt)
    end = datetime.strptime(endStr, fmt)
    startBlock = (start-zeroTime)
    duration = (end-start)
    # Convert duration to hours
    return  (int(startBlock.seconds/300.0), int(duration.seconds/300.0))

class UMLroom(object):
    # 2018-11-23 Updated to add seat capacity and category for classrooms, and category for class labs
    # which is an hour target (20 or 27)
    # From V ROOM LIST DEV - all 47 fields
    #BUILDING_ID	BUILDING	BUILDING_FAMIS_ID	BUILDING_UML_ID	BUILDING_NAME	BUILDING_CAMPUS	FLOOR_ID	FLOOR	FLOOR_SORT	BUILDING_FLOOR	ROOM_ID	ROOM	ROOM_NAME	AREA	SPACE_NAME	USE_ID	USE_CODE	FICM_USE	USE_NAME	FMG_USE	FMG_USE_NAME	USE_FILL_CODE	USE_FILL_CODE_ALT	DEPARTMENT_ID	DEPARTMENT_CODE	DEPARTMENT	DEPARTMENT_NAME	DEPARTMENT_NUMBER	DEPARTMENT_LEVEL	GROUP_ID	GROUP_CODE	GROUP_	GROUP_NAME	FMG_DEPARTMENT	FMG_DEPARTMENT_NAME	MAJOR_USE_ID	MAJOR_USE_CODE	MAJOR_USE	FMG_MAJOR_USE	SCHOOL_FILL_CODE	ASSIGNABILITY_ID	ASSIGNABILITY	PARENT_ID	PARENT_CODE	PARENT	PARENT_NAME

    def __init__(self, BLDG_UML_ID, BLDG_CAMPUS, FLOOR, AREA, SPACE_NAME, USE_NAME, DEPARTMENT_NAME,CATEGORY,PHYS_CAP,B_AVG,WSCH):
        self.bldgID = BLDG_UML_ID
        self.campus = BLDG_CAMPUS
        self.floor = FLOOR
        self.area = AREA
        self.roomID = SPACE_NAME
        self.USE_NAME = USE_NAME
        self.dept_name = DEPARTMENT_NAME
        self.category = CATEGORY
        self.phys_cap = PHYS_CAP
        self.battingAVG = B_AVG
        self.WSCH = WSCH
def makeGrid():
    retVal = collections.defaultdict(dict)
    for i in range(0,180):
        if i == 0:
            retVal[i] = collections.defaultdict(dict)
        for d in days:
            retVal[i][d] = []
    return retVal
def makeRoom(theRooms, r):
    #print "****", r, len(theRooms)
    theRooms[r] = collections.defaultdict(dict)
    theRooms[r]["WSCH"] = 0.0
    theRooms[r]["RM_HRS"] = 0.0
    theRooms[r]["CAMPUS"] = ""
    theRooms[r]["USE"] = "TBD"
    theRooms[r]["PHYS_CAP"] = 0.
    theRooms[r]["BAvg"] = 0.0
    for d in days:
        theRooms[r][d] = collections.defaultdict(list)
        for i in range(0,180):
            #theRooms[r][d][i] = collections.defaultdict(str)
            #theRooms[r][d][i]= {"COURSES":{"MAX_COURSE_FOR_UTIL":{"MaxEnrolled":0,"Career":"TBD"}}}
            theRooms[r][d][i] ={"COURSES":[]}


# Need space inventory to crosswalk SoC rooms -- and capacities
class Course(object):
    newID = itertools.count().next
    def __init__(self, career, term, course, comp, title, instructor, status, campus, room,
                 imode, credit, cap, enrolled, perm, mtgNum, hrs, days, college, dept, session, WSCH,
               duration, crossList):
        self.career = career
        self.term = term
        self.course = course
        self.comp = comp
        self.title = title
        self.instructor = instructor
        self.status = status
        self.campus = campus
        self.room = room
        self.imode = imode
        self.credit = credit
        self.cap = cap
        self.enrolled = int(enrolled)
        self.perm = perm
        self.mtgNum = mtgNum
        self.hrs = hrs
        self.days = days
        self.college = college
        self.dept = dept
        self.session = session # dropped instructor role 9/2/2021
        self.WSCH = float(WSCH)
        self.duration = 0
        self.crossList = crossList
        self.doubleDip = [] # was an int, count changing to list of IDs
        self.ID = Course.newID()

def getCourse_fromID(SoC, i):
    for c in SoC:
        if c.ID == i:
            return c
            break
    return "Not found"

def calc_seatOcc(theRooms,r, d,i,):
    cList = theRooms[r][d][i]["COURSES"]
    #print "`",r," ****", len(cList)
    #for c in cList:
        #print d,cList[c].hrs,i,cList[c].course,cList[c].enrolled,cList[c].career, cList[c].mtgNum

def output_rmHrs(theRooms):
    ofile = open("C:\\temp\\rmHrs_histogram.csv","w")
    oStr = "Room,Day,"
    oStr += timeslots()
    oStr += "\n"
    ofile.write(oStr)
    for r in theRooms:
        if theRooms[r]["USE"] != "NOT_A_ROOM":
            for d in ["M","T","W","R","F"]:
                oStr = r + ","
                oStr += d + ","
                for i in range(0,180):
                    currLen = len(theRooms[r][d][i]["COURSES"])
                    if currLen == 0:
                        oStr += "0,"
                    else:
                        oStr += ".08333,"
                oStr += "\n"
                ofile.write(oStr)
    ofile.close()

def output_rmHrs2(theRooms):
    print (len(theRooms))
    ofile = open("C:\\temp\\rmHrs_histogram2.csv","w")
    oStr = "Day,"
    oStr += timeslots()
    oStr += "\n"
    ofile.write(oStr)
    for d in ["M","T","W","R","F"]:
        oStr = d + ","
        for i in range(0,180):
            rms_in_use = 0
            for r in theRooms:
                if theRooms[r]["USE"] != "NOT_A_ROOM":    
                    currLen = len(theRooms[r][d][i]["COURSES"])
                    if currLen > 1:
                        rms_in_use += 1
            oStr += str(rms_in_use) + ","
            print rms_in_use
        oStr += "\n"
        ofile.write(oStr)
    ofile.close()

def output_lab_rmHrs(theRooms, labCat):
    #ofile = open("C:\\temp\\labQC.txt","w")
    
    for r in theRooms:
        if theRooms[r]["USE"] != "NOT_A_ROOM":
            if theRooms[r]["USE"] == "CLASS LABORATORY" and r in labCat:
                print r, theRooms[r]["USE"], theRooms[r]["RM_HRS"], labCat[r]["LAB_CATEGORY"],labCat[r]["LAB_MAJOR_CATEGORY"]
            #else:
                #print r, theRooms[r]["USE"], theRooms[r]["RM_HRS"]
    #for l in labCat:
        #print ">>>>", l, "<<<<<"
        

def timeslots():
    oStr = ""
    hr = 7
    m = 0
    a = "AM"
    for i in range(0,180):
        if hr == 12:
            a = "PM"
        if hr > 12:
            hr -= 12
        if m < 10:
            #print (str(hr) + ":0" + str(m) + " " + a)
            oStr += (str(hr) + ":0" + str(m) + " " + a) + ","
        else:
            #print (str(hr) + ":" + str(m) + " " + a)
            oStr += (str(hr) + ":" + str(m) + " " + a) + ","
        if m == 55:
            m =0
            hr += 1
        else:
            m += 5
    return oStr

def bAvg_byBldg(theRooms):
    bldg_bAvg = {}
    for r in theRooms:
        if theRooms[r]["USE"] == "CLASSROOM":
            currBldg = r[:3]
            if r not in bldg_bAvg:
                #print r, currBldg
                bldg_bAvg[currBldg] = {"WSCH":theRooms[r]["WSCH"],"PHYS_CAP":theRooms[r]["PHYS_CAP"]}
            else:
                bldg_bAvg[currBldg]["WSCH"] += theRooms[r]["WSCH"]
                bldg_bAvg[currBldg]["PHYS_CAP"] += theRooms[r]["PHYS_CAP"]

    for b in bldg_bAvg:
        print b, bldg_bAvg[b]["WSCH"], bldg_bAvg[b]["PHYS_CAP"], (float(bldg_bAvg[b]["WSCH"])/(40.*float(theRooms[r]["PHYS_CAP"])))

def output_RoomUseGrid(theRooms):
    ofile_north = open("C:\\temp\\north_cr_grid.csv","w")
    ofile_south = open("C:\\temp\\south_cr_grid.csv","w")
    for i in range(1,180,6): # Starting at 7:05 am, going by 30 minutes
        oStrNorth = ""
        oStrSouth = ""
        for d in ["M","T","W","R","F"]:
            NorthCount = 0
            SouthCount = 0
            for r in theRooms:
                if theRooms[r]["USE"] == "CLASSROOM" and theRooms[r]["CAMPUS"] == "UMLNORTH":
                        if len(theRooms[r][d][i]["COURSES"]) > 0:
                               NorthCount += 1
                elif theRooms[r]["USE"] == "CLASSROOM" and theRooms[r]["CAMPUS"] == "UMLSOUTH":
                         if len(theRooms[r][d][i]["COURSES"]) > 0:
                               SouthCount += 1
            # Done with current day-timeslot, output
            oStrNorth += str(NorthCount) + ","
            oStrSouth += str(SouthCount) + ","
        # Done with current time slot - output line of values
        oStrNorth += "\n"
        oStrSouth += "\n"
        ofile_north.write(oStrNorth)
        ofile_south.write(oStrSouth)
    ofile_north.close()
    ofile_south.close()

def output_RoomHistogram(theRooms):
    ofile_north = open("C:\\temp\\north_cr_histo.csv","w")
    ofile_south = open("C:\\temp\\south_cr_histo.csv","w")
    for d in ["M","T","W","R","F"]:
        oStrNorth = ""
        oStrSouth = "" 
        for i in range(0,180): # Starting at 7:05 am, going by 30 minutes
            NorthCount = 0
            SouthCount = 0
            for r in theRooms:
                if theRooms[r]["USE"] == "CLASSROOM" and theRooms[r]["CAMPUS"] == "UMLNORTH":
                        if len(theRooms[r][d][i]["COURSES"]) > 0:
                               NorthCount += 1
                elif theRooms[r]["USE"] == "CLASSROOM" and theRooms[r]["CAMPUS"] == "UMLSOUTH":
                         if len(theRooms[r][d][i]["COURSES"]) > 0:
                               SouthCount += 1
            # Done with current day-timeslot, output
            oStrNorth += str(NorthCount) + ","
            oStrSouth += str(SouthCount) + ","
        # Done with current time slot - output line of values
        oStrNorth += "\n"
        oStrSouth += "\n"
        print i, oStrNorth
        print i, oStrSouth
        ofile_north.write(oStrNorth)
        ofile_south.write(oStrSouth)
    ofile_north.close()
    ofile_south.close()

def output_util_byRoom(theRooms):
    ofile = open("C:\\temp\\util_by_room.csv","w")
    ofile.write("Campus,Room,Seats,WSCH,Util\n")
    for r in theRooms:
        if theRooms[r]["USE"] == "CLASSROOM":
            oStr = theRooms[r]["CAMPUS"] + "," + r + "," + str(theRooms[r]["PHYS_CAP"]) + ","
            oStr += str(theRooms[r]["WSCH"]) + "," + str(theRooms[r]["BAvg"])[:5] + "\n"
            ofile.write(oStr)
    ofile.close()
