import openpyxl, math, random
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
import collections, operator
from collections import defaultdict
from datetime import datetime

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


def writeBody(startTimes, days, theRooms, r):
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
    #Now data
    for s in startTimes:
        oStr += "<tr><td class='time'>" + s + "</td>"
        for d in days:
            if d != "S" and d != "U":
                """
                print "in", r, d, i, theRooms[r]["RM_HRS"], theRooms[r][d][i]["COURSES"]
                FIX WHAT DATA WE PASS IN - PASS IN WHOLE theRooms and specific room
                """
                """
                if len(theRooms[r][d][s]["COURSES"]) > 0:
                    # s may be formatted but we need i, slot number
                    oStr += "<td colspan='2' class='filled'>" + theRooms[r][d][s]["COURSES"]
                    oStr += ":     " + str(roomData[d][s][1]) + "</td>"
                else:
                    oStr += "<td colspan='2' class='empty'>  </td>"
                """
                oStr += "<td colspan='2' class='filled'>TBD</td><td colspan='2' class='empty'>  </td>"
                """
                oStr += "<td colspan='2' class='empty'>  </td>"
                """
        oStr += "</tr>\n"
    
    oStr += "</table>\n"   
    return oStr

def writeFooter():
    oStr = "</BODY></HTML>\n"
    return oStr

def make_schedDetail(theRooms, SoC, spInvRooms):
    days = ("M","T","W","R","F")
    startTimes2 = build_startTimes()
    for r in theRooms:
        ofile = open("C:\\temp\\t\\" + r + "_schedDetail.html","w")
        try:
            rmUse = theRooms[r]["USE"]
        except:
            rmUse = "OTHER/NON-ROOM"
            # (roomID, rmUse,rmHrs, WSCH):
        ofile.write(writeHeader(r, "TBD", theRooms[r]["RM_HRS"], theRooms[r]["WSCH"]))
        ofile.write(writeBody(startTimes2, days, theRooms, r))
        ofile.write(writeFooter())
        ofile.close()

