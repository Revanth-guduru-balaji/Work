import collections, operator
from collections import defaultdict
from operator import itemgetter
from datetime import datetime
import json
import CURR_utilLib as uLib
import CURR_pyodbcLib as p
import CURR_svg as svgOut

def outputUtilbyRoom(theRooms):
    #["BUILDING_UML_ID"],SpInv[r]["BUILDING_CAMPUS"]
    retVal = "SPACE_NAME,BLDG,SEATS,WSCH,CAMPUS\n"
    
    for r in theRooms:
        if theRooms[r]["USE"] == "CLASSROOM":
            retVal += r + "," + r[:3] + "," + str(theRooms[r]["PHYS_CAP"]) + "," + str(theRooms[r]["WSCH"]) + "," + theRooms[r]["CAMPUS"] + "\n"

    return retVal                

    
"""


- COB-G*??
Sept 30 2021
SoC key is now the row number from SQL/SoC - NO LONGER THE COURSE NUMBER, THAT IS NOT UNIQUE!!
"""


SQLsched = p.get_SoC()
SpInv = p.get_SpInv()
rmCaps = p.get_rmCapacities()
labCat = p.get_labCats()


# connect to space inventory room list
# connect to registrar's schedule

theRooms = collections.defaultdict(dict)
spInvRooms = collections.defaultdict(dict)
SoC = []
WSCHcounts = {"CLASSROOM":0.0,"CLASS LABORATORY":0.0,"CONFERENCE":0.0,"ONLINE":0.0,"OTHER":0.0}
days = ("M","T","W","R","F","S","U")
rawWSCH = 0.

# ======================================================Build dictionary of space inventory rooms as objects ========================================
# 
for r in SpInv:
    args = [SpInv[r]["BUILDING_UML_ID"],SpInv[r]["BUILDING_CAMPUS"],SpInv[r]["FLOOR"],SpInv[r]["AREA"],SpInv[r]["SPACE_NAME"],\
            SpInv[r]["USE_NAME"],SpInv[r]["DEPARTMENT_NAME"],"Category TBD",0,0.00,0.00]
    newRoom = uLib.UMLroom(*args)
    spInvRooms[r] = newRoom
# Build dictionary of courses listed  in schedule
theRooms = collections.defaultdict(dict)

# ====================================================== Loop through SQL schedule of courses, build room-based SoC dictionary  ========================================
# Calculate WSCH for each course
# Build schedule room dictionary

dayCounts = {"M":0,"T":0,"W":0,"R":0,"F":0,"S":0,"U":0}
courseCount = 0
for i in SQLsched:
    currDays = ""
    if SQLsched[i]["Days"] != "None":
        #print "before", SQLsched[c]["Days"]
        currDays = uLib.fixDayStr(str(SQLsched[i]["Days"]))
    else:
        currDays = SQLsched[i]["Days"]
    for d in days:
        if d in currDays:
            dayCounts[d] += 1
    # 9/16/21 Adding args for cross listing and double dipping. We can't detect them yet - we need to build the dictionary, then loop over it and look
    defaultWSCH = 0.0
    defaultDuration = 0.0
    try:
        print(SQLsched["StartDate"])
    except:
        ignoreThis = 0
    args = [SQLsched[i]["Career"],SQLsched[i]["Term"],SQLsched[i]["Course"],SQLsched[i]["Comp"],SQLsched[i]["Title"],SQLsched[i]["Instructor"],SQLsched[i]["Status"],\
            SQLsched[i]["Campus"],SQLsched[i]["Room"],SQLsched[i]["IMode"],SQLsched[i]["Credit"],SQLsched[i]["Cap"],SQLsched[i]["Tot"],SQLsched[i]["Perm"],SQLsched[i]["Mtg"]\
            ,SQLsched[i]["Time"],currDays,SQLsched[i]["College"],SQLsched[i]["Dept"],SQLsched[i]["Section"],defaultWSCH,defaultDuration,False]
    #if SQLsched[i]["Course"] == "EECE.4590 201":
        #print args
    currCourse = uLib.Course(*args)
    #if currCourse.room == "WEE-205":
        #print currCourse.ID, currCourse.course
    #print "***", currCourse.ID, currCourse.course
    #print "???Time\t", 
    try:
        classMin = uLib.classMinutes(SQLsched[i]["Time"])
        currCourse.duration = classMin/60.
    except:
        currCourse.duration = 0
    currCourse.WSCH = float(currCourse.duration * int(currCourse.enrolled) * uLib.classDayCount(currCourse.days))
    #print "Dur >>>\t", currCourse.duration
    #print "Enrolled >>>\t", currCourse.enrolled
    #print "Days >>>\t", uLib.classDayCount(currCourse.days)
    #if currCourse.WSCH > 0:
        #print "...\t",currCourse.WSCH
    #print i, currCourse.course, currCourse.WSCH
    SoC.append(currCourse)
    if currCourse.room not in theRooms:
        currRoom = currCourse.room
        #print currRoom, currCourse.course
        #print "The room", currRoom, rmCaps[currRoom]["MAX_CAPACITY"]
        uLib.makeRoom(theRooms, currCourse.room)
        #for t in theRooms:
            #print t, theRooms[t]["WSCH"]
        theRooms[currCourse.room]["CAMPUS"] = currCourse.campus
        try:
            theRooms[currRoom]["PHYS_CAP"] = rmCaps[currRoom]["MAX_CAPACITY"]
        except:
            ignoreThis = 1

        if currCourse.room in spInvRooms:
            #print r, rmCaps[currRoom]["MAX_CAPACITY"]
            theRooms[currRoom]["USE"] = spInvRooms[currRoom].USE_NAME         
        else:
            theRooms[currCourse.room]["USE"] = "NOT_A_ROOM"
            theRooms[currRoom]["PHYS_CAP"] = -1     
        theRooms[currCourse.room]["WSCH"] += currCourse.WSCH
        #print currRoom, theRooms[currRoom]["WSCH"], currCourse.course, currCourse.WSCH
        
         
    else:
        theRooms[currCourse.room]["WSCH"] += currCourse.WSCH
    courseCount += 1
print("Total Courses:", courseCount)

#================================== SoC Loop done ====================================
for c in SoC: # loop on SoC
    #if c.room == "OLS-409":
        #print "????",c.room, c.course, c.ID, c.days, c.hrs
    if theRooms[c.room]["USE"] != "NOT_A_ROOM":
        #print c.room, c.course, theRooms[c.room]["USE"]
        # determine when it starts and how long it lasts
        try:
            startBlock, numBlocks = uLib.parseTimeSlots(c.hrs)
        except:
            startBlock = None
            numBlocks = None
        #print c.hrs, startBlock, numBlocks
        # if it's a "real" in person class, load up the day/time block dictionary
        
        if startBlock != None:
            for d in c.days:
                for i in range(startBlock,(startBlock + numBlocks+1)):
                    #if c.room == "OLS-409":
                        #print  theRooms[c.room][d][i]["COURSES"], type( theRooms[c.room][d][i]["COURSES"]),c.room, c.ID, c.course, c.hrs, c.days, d, i
                    try:
                        theRooms[c.room][d][i]["COURSES"].append(c.ID)
                        #if c.room == "OLS-409" and d == "T":
                            #if len(theRooms[c.room][d][i]["COURSES"]) > 1:
                                #print "****", theRooms[c.room][d][i]["COURSES"], d, i
                    except:
                        #print "Check day and times", c.room, d, i, c.course
                        ignoreThis= 0

#print theRooms["MCG-313"]["T"][141]["COURSES"]



#================== Just room hours: if it's not 0 courses, count 5 minutes of use
spInvSeats = 0
spInvClassrooms = 0
inCourse = False
for r in theRooms:
    if theRooms[r]["USE"] != "NOT_A_ROOM":
        if theRooms[r]["USE"] == "CLASSROOM":
            spInvClassrooms += 1
            try:
                spInvSeats += float(theRooms[r]["PHYS_CAP"])        
            except:
                print("Check PHYS_CAP", r)
            try:
                theRooms[r]["BAvg"] = theRooms[r]["WSCH"]/(40.*float(theRooms[r]["PHYS_CAP"]))
            except:
                theRooms[r]["BAvg"] = 0.0
            #print r, theRooms[r]["WSCH"],theRooms[r]["PHYS_CAP"], theRooms[r]["BAvg"]
            #print type(r), type(theRooms[r]["WSCH"]), type(theRooms[r]["PHYS_CAP"])    
        for d in days:
            for i in range(0,180):   
                if len(theRooms[r][d][i]["COURSES"])> 0:
                    inCourse = True
                    theRooms[r]["RM_HRS"] += (1./12.)
                    #if len(theRooms[r][d][i]["COURSES"])> 0 and r == "OLS-409":
                        #print "in", r, d, i, theRooms[r]["RM_HRS"], theRooms[r][d][i]["COURSES"]
                else:
                    #print "What?"
                    #inCourse == True:
                    #if r == "OLS-409" and inCourse == True:
                        #theRooms[r]["RM_HRS"] -= (1./12.) # can't count first and last
                        #print "out", r, d, i, theRooms[r]["RM_HRS"], (theRooms[r]["RM_HRS"]*60), theRooms[r][d][i]["COURSES"]
                    inCourse = False


XLrawWSCH = 106029.1667
XLallWSCH = 143707.167
XLcrCount = 128
XLseatCount = 6142
rawWSCH = 0.
allWSCH = 0.
SoCclassrms = []
northClassrooms = []
southClassrooms = []
theCounts = {"SoCrms":0,"SoCseats":0,"SpInvRms":0,"SpInvSeats":0}
for i in SoC:
    if theRooms[i.room]["USE"] == "CLASSROOM":
        if theRooms[i.room]["CAMPUS"] == "UMLNORTH" and i.room not in northClassrooms:
            northClassrooms.append(i.room)
        elif theRooms[i.room]["CAMPUS"] == "UMLSOUTH"and i.room not in southClassrooms:
            southClassrooms.append(i.room)
        if i.room not in SoCclassrms:
            SoCclassrms.append(i.room)
        rawWSCH += i.WSCH
    else:
        allWSCH += i.WSCH


print("SoC classrooms", len(SoCclassrms))
print("SoC Raw WSCH Calc", rawWSCH, "SoC all WSCH:", (rawWSCH + allWSCH))
print("SpInv classroom count", spInvClassrooms, " and seats", spInvSeats)
print("North Classrooms", len(northClassrooms))
print("south Classrooms", len(southClassrooms))
print("Excel says all Raw WSCH is", XLrawWSCH, " and all WSCH is", XLallWSCH )
print("Excel says SoC classroom count is", XLcrCount, " and seats", XLseatCount)
print("WSCH compare: py/excel", (rawWSCH/XLrawWSCH))
print("EXcel util:", (XLrawWSCH/(40*spInvSeats)))
print("SpInv util:", (rawWSCH/(40*spInvSeats)))

print("Overall 2021 Utilization:", (rawWSCH/(40*spInvSeats)))


northGrid = uLib.makeGrid()
southGrid = uLib.makeGrid()

gridDays = ("M","T","W","R","F")
"""
for d in theRooms["WEE-LH1"]:
    print d
    for i in theRooms["WEE-LH1"]["M"]:
        print i, theRooms["WEE-LH1"]["M"][i]["COURSES"]
"""
for r in theRooms:
    for d in gridDays:
        for i in theRooms[r][d]:
            if theRooms[r]["CAMPUS"] == "UMLNORTH" and (len(theRooms[r][d][i]["COURSES"]) > 0) and theRooms[r]["USE"] == "CLASSROOM":
                if r not in northGrid[i][d]:
                    northGrid[i][d].append(r)
                #print r, d, theRooms[r][d][i]["COURSES"]
            if theRooms[r]["CAMPUS"] == "UMLSOUTH" and (len(theRooms[r][d][i]["COURSES"]) > 0) and theRooms[r]["USE"] == "CLASSROOM":
                if r not in southGrid[i][d]:
                    southGrid[i][d].append(r)

oGrid = open("C:\\temp\\southgrid.csv","w")
oGrid.write("Time,M,T,W,R,F\n")

#for i in southGrid:
for i in southGrid:
    if i % 6 == 0:
        oStr = str(i) + ","
        for d in gridDays:
            inUse = len(southGrid[i][d])
            available = len(southClassrooms) - inUse
            oStr += str(available) + ","
        oStr += "\n"
        oGrid.write(oStr)
oGrid.close()

oGrid = open("C:\\temp\\northgrid.csv","w")
oGrid.write("Time,M,T,W,R,F\n")


for i in northGrid:
    if i % 6 == 0:
        oStr = str(i) + ","
        for d in gridDays:
            inUse = len(northGrid[i][d])
            available = len(northClassrooms) - inUse
            oStr += str(available) + ","
        oStr += "\n"
        oGrid.write(oStr)
oGrid.close()

"""
utilCSV = outputUtilbyRoom(theRooms)
ofile = open("C:\\temp\\utilCSV.csv","w")
ofile.write(utilCSV)
ofile.close()

#svgOut.output_svg(theRooms, labCat)
for r in theRooms:
    #print theRooms[r]
    svgOut.svgRoomOut(theRooms[r],r, labCat)

#print "*** Room Hours", theRooms["OLS-409"]["RM_HRS"]
"""


