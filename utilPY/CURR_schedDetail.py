import openpyxl, math, random
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
import collections, operator
from collections import defaultdict
from datetime import datetime
import os

def tstamper():
    now = datetime.now()
    tstamp = str(now.year) + str(now.month) + str(now.day) + "_"
    tstamp += str(now.hour) + str(now.minute) + str(now.second)
    return(tstamp)
def build_startTimes():
    startTimes = []

    # create list of start times, 1/2 hour increments
    startTimes2 = []
    for s in range(7,10):
        startTimes2.append("0" + str(s) + ":00 AM")
        startTimes2.append("0" + str(s) + ":30 AM")
    for s in range(10,12):
        startTimes2.append(str(s) + ":00 AM")
        startTimes2.append(str(s) + ":30 AM")
    startTimes2.append("12:00 PM")
    startTimes2.append("12:30 PM")
    for s in range(1,10):
        startTimes2.append("0" + str(s) + ":00 PM")
        startTimes2.append("0" + str(s) + ":30 PM")
    return startTimes2

def writeHeader(roomID, rmUse,rmHrs, WSCH):
    # we'll want a CSS reference here
    oStr = "<HTML><HEAD><title>" + roomID + "</title>"
    oStr += "<link rel = 'stylesheet' type = 'text/css' href = 'roomDetail.css' /></HEAD><BODY>\n"
    oStr += "<h4>Fall 2018 Utilization | " + roomID + " | Room Hrs:" + str(rmHrs)[:4] + " | WSCH:" + str(WSCH) + "</h4>\n"
    oStr += "<h4>" + rmUse + "</h4>\n"
    return oStr

def writeBody(startTimes, days, roomData, phys_cap, tstamp):
    #2 rows at top: day, then the 2 fields we display:course name,enrollment
    #if theRooms[r][d][s][0] != 0:
    #oStr += theRooms[r][d][s][0] + "\t" + str(theRooms[r][d][s][1])

    oStr = "<table><tr><th>  </th>"
    fulldays = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

    for f in fulldays:
        oStr += "<th colspan='2'>" + f + "</th>"
    oStr += "</tr>\n"
    oStr += "<tr><th>Times</th>"
    for f in fulldays:
        oStr += "<th>Course Name</th><th>Enrolled</th>"
    oStr += "</tr>\n"
    #Now data - adding SUR category
    # how do we do time slots (i) vs startTimes
    j = 0
    for s in startTimes:
        oStr += "<tr><td class='time'>" + s + "</td>"
        for d in days:
            if d != "S":
                if len(roomData[d][j]["COURSES"])> 0:
                    oStr += "<td colspan='2' class='filled'>" + str(roomData[d][j]["COURSES"][0])
                    # this is course ID but we need name and enrollment - need to lookup)
                    #print "?????????",phys_cap
                    if (phys_cap == "NA" or phys_cap == "#N/A"):
                        SURcat = "NA"
                    elif (phys_cap > 0):
                        #print ":::", roomData[d][s][1],phys_cap
                        #FIX THIS 11/20/2021 SURcat = SURcategory(float(float(roomData[d][s][1]))/float(phys_cap))
                        SURcat = "SUR33"
                    else:
                        SURcat = "filled"
                    # FIX THIS 11/20/2021
                    #oStr += "<td colspan='2' class='" + SURcat + "'>" + roomData[d][s][0]
                    #oStr += ":     " + str(roomData[d][s][1]) + "</td>"
                    oStr += "<td colspan='2' class='" + SURcat + "'>" + "FIX THIS"
                    oStr += ":     " + "FIX THIS" + "</td>"
                else:
                    oStr += "<td colspan='2' class='empty'>  </td>"
        oStr += "</tr>\n"
        j += 6
        if j > 180:
            j = 180
        
    
    oStr += "</table>\n"
    oStr += "<h6>Last updated:" + tstamp + "<h6>\n"
    return oStr

def writeFooter():
    oStr = "</BODY></HTML>\n"
    return oStr

def make_schedDetail(theRooms, SoC, spInvRooms):
    days = ("M","T","W","R","F")
    startTimes2 = build_startTimes()
    for r in theRooms:
         # Define the directory and file path
        directory = "HTML"
        filepath = directory+"/"+ r + "_schedDetail.html"

        # Create the directory if it does not exist
        if not os.path.exists(directory):
            os.makedirs(directory)

              
        
        try:
            rmUse = theRooms[r]["USE"]
        except:
            rmUse = "OTHER/NON-ROOM"
            #writeHeader(roomID, rmUse, category, phys_cap,bAvg, rmHrs, WSCH):
        # Write to the file
        roomID = r
        rmHrs = theRooms[r]["RM_HRS"]
        WSCH = theRooms[r]["WSCH"]
        with open(filepath, "w") as f:
            f.write(writeHeader(roomID,rmUse ,rmHrs,WSCH))  
            tstamp = tstamper()
            f.write(writeBody(startTimes2, days, theRooms[r], 20,tstamp))
            f.write(writeFooter())
            f.close()

