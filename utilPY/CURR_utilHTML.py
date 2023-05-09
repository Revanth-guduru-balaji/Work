from datetime import datetime

"""
2020-01-01
Should add a way to get number of stations for classrooms and class labs
- Check list of classrooms and labs, if room is there
    - get number of stations
    - use lab or classroom to call function for additional header info
What to do about coloring the time slots? Check for classroom/lab first
then funnel appropriately
BTW, we have this functionality - spInvRooms - add back in???
"""
def tstamper():
    now = datetime.now()
    tstamp = str(now.year) + str(now.month) + str(now.day) + "_"
    tstamp += str(now.hour) + str(now.minute) + str(now.second)
    return(tstamp)

def numDays(daysStr):
    theDays = ["M","Tu","W","Th","F","Sa","Su"]
    
def classMinutes(SoCstr):
    #Error check!!???
    #print ">>>>>>>>>>>>>>>>>", SoCstr
    toks = SoCstr.split('-')
    classStart = toks[0].strip()
    classEnd = toks[1].strip()

    FMT = '%I:%M %p'
    try:
        tdelta = datetime.strptime(classEnd, FMT) - datetime.strptime(classStart, FMT)
        tStr = str(tdelta)
        #print "from classMinutes:", tStr
        h, m, s = [int(i) for i in tStr.split(':')]
    except:
        h = 0
        m = 0
        s= 0
    return((h*60) + m)

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

def labCat27(rmHrs):
    retVal = ""
    if (rmHrs < 9):
        retVal = "bAVGlow"
    elif (rmHrs < 18):
        retVal = "bAVG150"
    elif (rmHrs < 27):
        retVal = "bAVG300"
    elif (rmHrs < 36):
        retVal = "bAVG450"
    else:
        retVal = "bAVG600"
    return retVal

def labCat20(rmHrs):
    retVal = ""
    if (rmHrs < 10):
        retVal = "bAVGlow"
    elif (rmHrs < 20):
        retVal = "bAVG150"
    elif (rmHrs < 30):
        retVal = "bAVG450"
    else:
        retVal = "bAVG600"
    return retVal
#bAVGkey600

def bAvgCategory(bAvg):
    retVal = ""
    #print "bAvgCategory:", bAvg
    # maybe try catch is better so any non-float value gets NA
    try:
        bAvg = float(bAvg)
        if (bAvg < 0.150):
            retVal = "bAVGlow"
        elif (bAvg < 0.300):
            retVal = "bAVG150"
        elif (bAvg < 0.450):
            retVal = "bAVG300"
        elif (bAvg < 0.600):
            retVal = "bAVG450"
        else:
            retVal = "bAVG600"
    except:
        retVal = "bAVG_NA"
    #print "??????", retVal
    return retVal

def SURcategory(SUR):
    retVal = ""
    if (SUR < 0.17):
        retVal = "SURlow"
    elif (SUR < 0.33):
        retVal = "SUR17"
    elif (SUR < 0.50):
        retVal = "SUR33"
    elif (SUR < 0.67):
        retVal = "SUR50"
    else:
        retVal = "SUR67"
    return retVal
################### HTML OUTPUT                                     #
def writeTopTableCR(bAvg, rmHrs):
    blankCell = "<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>"
    oStr = "<table>\n<!-- top row: labels -->\n<tr>\n<td colspan='5'>Utilization - Executive Office of Education metric</td>\n"
    oStr += blankCell + "\n<td colspan='4'>Room hours</td>" + blankCell + "\n"
    oStr += "<td colspan='5'>&nbsp;</td>\n</tr><tr><td colspan='5'>Target is .450, roughly 67% room use, 67% seat fill</td>\n"
    oStr += blankCell+ "<td colspan='4'>Target is 30 hours </td><td>" + blankCell + "\n"
    oStr += "<td colspan='5'>&nbsp;</td></tr>\n"
    #print "!?", bAvg
    cc = 0 # just a counter for except errors
    try:
        bAvgCat = bAvgCategory(bAvg)
        if (bAVG != "bAVG_NA"):
            if (float(bAvg) < 1):
                bAvg = bAvg[-4:]
    except:
        #print "Error in writeTopTable\n"
        cc += 1
        
    #oStr += "<!-- middle row: data -->\n<tr><td colspan='5' class='" + bAvgCat + "'>" + ("%0.3f" % bAvg) + "</td>\n"
    oStr += "<!-- middle row: data -->\n<tr><td colspan='5' class='" + bAvgCat + "'>" + bAvg + "</td>\n"
    rmHrCat = labCat20(rmHrs)
    if rmHrCat == "bAVG450": rmHrCat = "bAVG300"
    oStr += blankCell + "<td colspan='4' class='" + rmHrCat + "'>" + ("%2.1f" % rmHrs)+  "</td>\n" + blankCell + "\n"
    oStr += "<td colspan='5' valign='bottom' align='right'>Seat utilization displayed on calendar.<br/>Target is 67%</td></tr>\n"
    oStr += "<!-- bottom row: key/legend -->\n"
    oStr += "<tr><td class='bAVGkeylow'><.150</td><td class='bAVGkey150'>.150+</td><td class='bAVGkey300'>.300+</td>"
    oStr += "<td class='bAVGkey450'>.450+</td><td class='bAVGkey600'>.600+</td>" + blankCell + "\n"
    oStr += "<td class='bAVGkeylow'><10</td><td class='bAVGkey150'>10+</td><td class='bAVGkey300'>20+</td>"
    oStr += "<td class='bAVGkey600'>30+</td>" + blankCell + "\n"
    oStr += "<td class='SURlow'><17%</td><td class='SUR17'>17%+</td><td class='SUR33'>33%+</td><td class='SUR50'>50%+</td>"
    oStr += "<td class='SUR67'>67%+</td></tr>\n"
    return oStr

def writeTopTableCLASSLAB(category, rmHrs):
    # 20 hour target vs 27
    # that means the key on the first table is different as is the coloring of the room hour number
    blankCell = "<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>"
    oStr = "<table>\n<!-- top row: labels -->\n<tr>\n"
    if (category == 20):
        oStr += "\n<td colspan='4'>"
    else:
        oStr += "\n<td colspan='5'>"
    oStr += "Room hours (target is: " + str(category) + " hours)</td>" + blankCell + "\n"
    # room hour target is a variable!
    oStr += "<td colspan='5'>" + blankCell + "</td>\n"
    oStr += "<td colspan='5'>&nbsp;</td></tr>\n"
    oStr += "<!-- middle row: data -->\n<tr>\n"
    # need to assess RMU to get CSS class
    if (category == 20):
        rmHrCat = labCat20(rmHrs)
        oStr += "<td colspan='4' class='" + rmHrCat + "'>" + ("%2.1f" % rmHrs)+  "</td>\n" + blankCell + "\n"
        oStr += "<td colspan='5' valign='bottom' align='right'>Seat utilization displayed on calendar.<br/>Target is 67%</td></tr>\n"
        oStr += "<!-- bottom row: key/legend -->\n"
        oStr += "<tr><td class='bAVGkeylow'><10</td><td class='bAVGkey150'>10+</td><td class='bAVGkey450'>20+</td>"
        oStr += "<td class='bAVGkey600'>30+</td>" + blankCell + "\n"
    else:
        rmHrCat = labCat27(rmHrs)
        #print "WHATTTTTT?"
        oStr += "<td colspan='5' class='" + rmHrCat + "'>" + ("%2.1f" % rmHrs)+  "</td>\n" + blankCell + "\n"
        oStr += "<td colspan='5' valign='bottom' align='right'>Seat utilization displayed on calendar.<br/>Target is 67%</td></tr>\n"
        oStr += "<!-- bottom row: key/legend -->\n"
        oStr += "<tr><td class='bAVGkeylow'><9</td><td class='bAVGkey150'>9+</td><td class='bAVGkey300'>18+</td>"
        oStr += "<td class='bAVGkey450'>27+</td><td class='bAVGkey600'>36+</td>"+ blankCell + "\n"
    oStr += "<td class='SURlow'><17%</td><td class='SUR17'>17%+</td><td class='SUR33'>33%+</td><td class='SUR50'>50%+</td>"
    oStr += "<td class='SUR67'>67%+</td></tr>\n"
    return oStr


def writeHeaderCLASSROOM(roomID, rmUse, category, phys_cap, bAvg, rmHrs, WSCH):
    #def writeHeader(roomID, rmUse, rmHrs, WSCH):
    # Calcs
    #print "@@@@@", roomID, bAvg
    print "HELLO"
    RMU = rmHrs/40.
    photoURL = "https://www.uml.edu/service/Apps/Facilities/RoomCapture/Rooms/View?building="
    photoURL2 = "&room="
    """
    try:
        bAvg = WSCH/(40. * phys_cap)
    except:
        "Failed on: ", roomID, WSCH, phys_cap
        bAvg = 0.000
    """
    classStr = bAvgCategory(bAvg)
    if bAvg[0] == "0":
        bAvg = bAvg[1:5]
    else:
        bAvg = bAvg[:5]
    #print "!!!!!", bAvg, roomID
    toks = roomID.split("-")
    oStr = "<HTML><HEAD><title>" + roomID + "</title>"
    oStr += "<link rel = 'stylesheet' type = 'text/css' href = 'roomDetail.css' /></HEAD><BODY>\n"
    #print ":::", roomID, rmUse, category, phys_cap
    try:
        phys_cap = "{:.0f}".format(float(phys_cap))
    except:
        phys_cap = "None"
    oStr += "<h4>DRAFT Spring 2020 | " + roomID + "| " + rmUse + " | " + str(phys_cap) + " seats</h4>\n"
    try:
        pURL = photoURL + toks[0] + photoURL2 + toks[1]
        oStr += "<h6><a href='" + pURL + "'>Photos of: " + roomID + "</a></h6>"
    except:
        print "no photosphere"
    oStr += writeTopTableCR(bAvg, rmHrs)
    #print ("Photosphere link:" + photoURL + toks[0] + photoURL2 + toks[1]) 
    #https://www.uml.edu/service/Apps/Facilities/RoomCapture/Rooms/View?building=BAL&room=412

    return oStr

#def writeHeader(roomID, rmUse, category, phys_cap,bAvg, rmHrs, WSCH):
def writeHeader(roomID, theRoom):
    rmUse = theRoom["USE"]
    category = theRoom["LAB_CAT"]
    phys_cap = theRoom["SEAT_CAP"]
    bAvg = theRoom["UTIL"]
    rmHrs = theRoom["RM_HRS"]
    WSCH = theRoom["WSCH"]
    #rmUse, category, phys_cap,bAvg, rmHrs, WSCH):
    oStr = ""
    #theRooms[r]["USE"], 20, theRooms[r]["PHYS_CAP"],str(theRooms[r]["BAvg"]),theRooms[r]["RM_HRS"], theRooms[r]["WSCH"]))
    # Calcs
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!! DEBUGGING ONLY ###############
    #rmUse = "CLASSROOM"
    if rmUse == "CLASSROOM":
        #print "?????", roomID, rmUse, category, phys_cap, "batting average:", bAvg, rmHrs, WSCH
        oStr = writeHeaderCLASSROOM(roomID, rmUse, category, phys_cap, bAvg, rmHrs, WSCH)
    # change so denom is always 40
    # 2 different scales: 50% is good, 75% great
    # or, more like classrooms, 5 steps (in fact, same, right?)
    else:
        print "::::", category
        if category == "NA":
            denom = 40.
        else:
            denom = category
        print rmHrs, type(rmHrs), denom, type(denom)
        RMU = rmHrs/denom

        oStr = "<HTML><HEAD><title>" + roomID + "</title>"
        oStr += "<link rel = 'stylesheet' type = 'text/css' href = 'roomDetail.css' /></HEAD><BODY>\n"
        oStr += "<h4>" + roomID + "| " + rmUse + "| " + str(phys_cap) +  " stations</h4>\n"
        oStr += writeTopTableCLASSLAB(category, rmHrs)
      
    return oStr

def writeHeader2(roomID, rmHrs, WSCH):
    oStr = ""
    oStr = "<HTML><HEAD><title>" + roomID + "</title>"
    oStr += "<link rel = 'stylesheet' type = 'text/css' href = 'roomDetail.css' /></HEAD><BODY>\n"
    oStr += "<h4>Fall 2019 Schedule | " + roomID + "| " + str(rmHrs) + " room hours | " + str(WSCH) + " WSCH</h4>\n"
      
    return oStr

def writeHeader3(semester, roomID, rmUse, category, phys_cap, rmHrs, WSCH):
    oStr = ""
    
    # Calcs
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!! DEBUGGING ONLY ###############
    if rmUse == "CLASSROOM":
        #print "?????", roomID, rmUse, category, phys_cap, "batting average:", bAvg, rmHrs, WSCH
        try:
            bAvg = WSCH/(40*phys_cap)
        except:
            bAvg = "NA"
        oStr = writeHeaderCLASSROOM(roomID, rmUse, category, phys_cap, str(bAvg), rmHrs, WSCH)
    # change so denom is always 40
    # 2 different scales: 50% is good, 75% great
    # or, more like classrooms, 5 steps (in fact, same, right?)
    elif rmUse == "CLASS LABORATORY":
        #print "!!!!", roomID, rmUse, category
        oStr = "<HTML><HEAD><title>" + roomID + "</title>"
        oStr += "<link rel = 'stylesheet' type = 'text/css' href = 'roomDetail.css' /></HEAD><BODY>\n"
        oStr += "<h4>" + semester + " | " + roomID + "| " + rmUse + "| " + str(phys_cap) +  " stations</h4>\n"
        #print ">>>>", category
        oStr += writeTopTableCLASSLAB(category, rmHrs)

    else:
        try:
            RMU = rmHrs/category
        except:
            RMU = rmHrs/40.
            
        oStr = "<HTML><HEAD><title>" + roomID + "</title>"
        oStr += "<link rel = 'stylesheet' type = 'text/css' href = 'roomDetail.css' /></HEAD><BODY>\n"
        oStr += "<h4>Fall 2019 | " + roomID + "| " + rmUse + "| " + str(phys_cap) +  " stations</h4>\n"
        oStr += writeTopTableCLASSLAB(40, rmHrs)
  
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

def writeBody2(startTimes, days, roomData, tstamp):
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
    for s in startTimes:
        oStr += "<tr><td class='time'>" + s + "</td>"
        for d in days:
            if d != "S":
                if roomData[d][s][0] != 0:
                    SURcat = "filled"
                    oStr += "<td colspan='2' class='" + SURcat + "'>" + roomData[d][s][0]
                    oStr += ":     " + str(roomData[d][s][1]) + "</td>"
                else:
                    oStr += "<td colspan='2' class='empty'>  </td>"
        oStr += "</tr>\n"
    
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
        ofile = open("C:\\temp\\t\\" + r + "_schedDetail.html","w")
        try:
            rmUse = theRooms[r]["USE"]
        except:
            rmUse = "OTHER/NON-ROOM"
            #writeHeader(roomID, rmUse, category, phys_cap,bAvg, rmHrs, WSCH):
        ofile.write(writeHeader(r, theRooms[r]["USE"], 20, theRooms[r]["PHYS_CAP"],str(theRooms[r]["BAvg"]),theRooms[r]["RM_HRS"], theRooms[r]["WSCH"]))
        #writeBody(startTimes, days, roomData, phys_cap, tstamp):
        tstamp = tstamper()
        ofile.write(writeBody(startTimes2, days, theRooms[r], 20,tstamp))
        ofile.write(writeFooter())
        ofile.close()
print "utilHTML reloaded"
