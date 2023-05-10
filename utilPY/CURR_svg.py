def rmSize(seats):
    # new (AI) sizes: small - 50x45, 60x50, 60x70
    try:
        seats = float(seats)
    except:
        seats = 1.
    
    retVal_w = 0.
    retVal_h = 0.
    """
    if seats > 74.:
        retVal_w = 140.
        retVal_h = 120.
    elif seats > 35.:
        retVal_w = 100.
        retVal_h = 120.
    else:
        retVal_w = 100.
        retVal_h = 90.
    """
    if seats > 74.:
        retVal_w = 70.
        retVal_h = 60.
    elif seats > 35.:
        retVal_w = 50.
        retVal_h = 60.
    else:
        retVal_w = 50.
        retVal_h = 45.
    return retVal_w, retVal_h    
        
    
def bAvgCat(util):
    retVal = ""
    util = float(util)
    if util > .600:
        retVal = "bAVGkey600"
    elif util > .450:
        retVal = "bAVGkey450"
    elif util > .300:
        retVal = "bAVGkey300"
    elif util > .150:
        retVal = "bAVGkey150"
    else:
        retVal = "bAVGkeylow"
    return retVal

def rmHrCat(rmHrs, rmCat):
    retVal = ""
    util = float(rmHrs)/40.
    if rmCat == "STEM":
        if util > .75:
            #retVal = "STEM5"
            retVal = "bAVGkey600"
        elif util > .50:
            #retVal = "STEM4"
            retVal = "bAVGkey450"
        elif util > .33:
            #retVal = "STEM3"
            #retVal = "bAVGkey150"
            retVal = "bAVGkey300"
        elif util > .16:
            #retVal = "STEM3"
            retVal = "bAVGkey150"
        else:
            #retVal = "STEM1"
            retVal = "bAVGkeylow"
    elif rmCat == "Dry":
        if util > .82:
            retVal = "DRY5"
        elif util > .67:
            retVal = "DRY4"
        elif util > .50:
            #retVal = "DRY2"
            retVal = "DRY3"
        elif util > .33:
            #retVal = "DRY2"
            retVal = "DRY2"
        else:
            retVal = "DRY1"
    else:
        print("error: check lab major category")
    return retVal

def addBldgLabel(b, xpos, ypos):
    retVal = "<text id=\"bldgLbl_" + b + "\" class=\"st1 st5 st3\" x=\"" + str(xpos) + "\" y=\"" + str(ypos) + "\" fill=\"black\">" + b + "</text>\n"
    return retVal

def makeSVGroom(rmName, bAvg, numSeats, xpos, ypos):
    # new (AI) sizes: small - 50x45, 60x50, 60x70
    txtOffX = 9
    txtOffY = 15
    #retVal = "<g id=\"" + rmName + "\" onclick=\"loadPhotoplan(&quot;SOU&quot;);\">\n"
    lblUtil =  str(bAvg)
    if lblUtil[0] == "0":
        lblUtil = lblUtil[1:5]
    else:
        lblUtil = lblUtil[:5]
    bCat = bAvgCat(bAvg)
    #class="st1 st2
    sizeW,sizeH = rmSize(numSeats)
    # need to adjust ypos based on sizeH so the line up at the bottom
    ypos += (120 - sizeH) # 120 is hard coded -it's the height of medium and large rooms. need variable
    retVal = "<g id=\"" + rmName + "\">\n"
    retVal += "<rect x=\"" + str(xpos) + "\" y=\"" + str(ypos) + "\" width=\"" + str(sizeW) + "\" height=\"" + str(sizeH) + "\" class=\"" + bCat + "\" />\n"
    retVal += "<text id=\"lbl_" + rmName + "\" class=\"st1 st2\" x=\"" + str(xpos + txtOffX) + "\" y=\"" + str(ypos + txtOffY) + "\" fill=\"black\">" + rmName + "</text>\n"
    retVal += "<text id=\"util_" + rmName + "\" class=\"st1 st4 st3\" x=\"" + str(xpos + txtOffX + (txtOffX/2)) + "\" y=\"" + str(ypos + txtOffY+ txtOffY) + "\" fill=\"black\">" + lblUtil + "</text>\n"    
    retVal += "</g>\n"
    return(retVal,sizeW, sizeH)

def makeSVGlab(rmName, rmHrs, labType, xpos, ypos):
    txtOffX = 18
    txtOffY = 30
    #retVal = "<g id=\"" + rmName + "\" onclick=\"loadPhotoplan(&quot;SOU&quot;);\">\n"
    #bCat = bAvgCat(bAvg)
    #print rmName, labType
    utilCat = rmHrCat(rmHrs, labType)
    currUtil = float(rmHrs)/40.
    utilStr = "{:.1%}".format(currUtil)
    #class="st1 st2
    #    sizeW,sizeH = rmSize(numSeats)
    sizeW = 100.
    sizeH = 100.
    # need to adjust ypos based on sizeH so the line up at the bottom
    ypos += (120 - sizeH) # 120 is hard coded -it's the height of medium and large rooms. need variable
    retVal = "<g id=\"" + rmName + "\">\n"
    retVal += "<rect x=\"" + str(xpos) + "\" y=\"" + str(ypos) + "\" width=\"" + str(sizeW) + "\" height=\"" + str(sizeH) + "\" class=\"" + utilCat + "\" />\n"
    #retVal += "<text id=\"lbl_" + rmName + "\" class=\"st1 st2\" x=\"" + str(xpos + txtOffX) + "\" y=\"" + str(ypos + txtOffY) + "\" fill=\"black\">" + rmName + "</text>\n"
    #retVal += "<text id=\"util_" + rmName + "\" class=\"st1 st4 st3\" x=\"" + str(xpos + txtOffX + (txtOffX/2)) + "\" y=\"" + str(ypos + txtOffY+ txtOffY) + "\" fill=\"black\">" + utilStr + "</text>\n"    
    retVal += "<text id=\"lbl_" + rmName + "\" class=\"st1 st5\" x=\"50\" y=\"50\" fill=\"black\">" + rmName + "</text>\n"
    retVal += "<text id=\"util_" + rmName + "\" class=\"st1 st6 st3\" x=\"50\" y=\"80\" fill=\"black\">" + utilStr + "</text>\n"    
    retVal += "</g>\n"
    return(retVal,sizeW, sizeH)

def svgClassroomOut(campus, campusName, baseX):
    """
    Logic: Layout done in AI. Each building has a "starting" x/y. Loop over buildings, add
            floors with rooms, with a standard Y increment for floors and X increment for rooms
    """
    #illustPos = {"PTB":[804,1007],"SOU":[804,832],"SHA":[804,670],"BAL":[804,495],"OLS":[804,310],\
                 #"DAN":[1570,1014],"FAL":[1570,834],"PER":[1570,593],"OLN":[1570,330],"GPS":[1570,1230]}
    illustPos = {"PTB":[804,700],"SOU":[804,532],"SHA":[804,370],"BAL":[804,195],"OLS":[804,100],\
                 "DAN":[1570,700],"FAL":[1570,532],"PER":[1570,293],"OLN":[1570,30],"GPS":[1570,930],
                 "WEE":[0,10],"HSS":[0,110],"COB":[0,210],"DUG":[0,310],"MCG":[0,410],"OLE":[0,510],
                 "RIV":[0,610],"MAH":[0,710]}
    
    maxX = baseX + 50.
    maxX = 50.
    gapX = 20
    baseX = 20
    gapY_sameBldg = 70
    #gapY_newBldg =  40
    #maxY = (numFloors * (gapY_sameBldg+gapY_newBldg))
    #maxY = (numFloors * (gapY_sameBldg+gapY_newBldg) * 1.5)
    currY = 0

    """
    <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
             viewBox="0 0 3234.6 4525" style="enable-background:new 0 0 3234.6 4525;" xml:space="preserve">
    """
    oStr = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    oStr += "<!-- UML utilization SVG-->\n"
    oStr += "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\" "
    

    oStr2 = ""
    for b in reversed(sorted(campus)):
        currX = illustPos[b][0]
        currY = illustPos[b][1]
        print("start", b, " at Y=", currY,"\n")
        for f in sorted(campus[b]):
            maxX = currX
            print("==========", b)
            for r in sorted(campus[b][f]["rooms"]):
                print("\t>>>", r)
                currUtil = campus[b][f]["rooms"][r]["BAvg"]
                moreStr,wdth,ht = makeSVGroom(r,currUtil, campus[b][f]["rooms"][r]["PHYS_CAP"],maxX,currY)
                oStr2 += moreStr
                maxX += wdth + gapX
                print(maxX, currY, r)
            currY -= gapY_sameBldg
            print("********************** done with floor, increment Y", currY)
                    

    #oStr += "viewBox=\"0 0 4000 " + str(currY) + "\" style=\"enable-background:new 0 0 1366 768;\" xml:space=\"preserve\">\n"
    oStr += "viewBox=\"0 0 2000 2000\" style=\"enable-background:new 0 0 1366 768;\" xml:space=\"preserve\">\n"
    oStr += "<style type=\"text/css\">\n"
    oStr += ".bAVGkey600 {fill: #59baed;}\n.bAVGkey450 {fill:#a0ccef;}\n.bAVGkey300 {fill: #f7eec3;}\n.bAVGkey150 {fill: #eda29f;}\n.bAVGkeylow {fill: #ec7e79;}\n"
    oStr += ".st0{fill:#59baed;}\n.st1{text-align:center; font-family:'Frutiger';}\n.st2{font-size:9px;}\n.st3{font-weight:bold;}\n.st4{font-size:12px;}\n.st5{font-size:15px;}\n"
    oStr += "</style>\n"
    # Start group of all rooms
    oStr += "<g id=\"classrooms\">\n"
    oStr += oStr2
    oStr += "</g></svg>\n"
    ofile = open("C:\\temp\\2021F_Util\\" + campusName + "_test.svg","w")
    ofile.write(oStr)
    ofile.close()

def svgClassLabOut(campus, campusName, baseX, labCat):
    maxX = baseX + 50.
    maxX = 50.
    gapX = 20
    baseX = 20
    gapY_sameBldg = 140
    gapY_newBldg =  40
    #maxY = (numFloors * (gapY_sameBldg+gapY_newBldg))
    #maxY = (numFloors * (gapY_sameBldg+gapY_newBldg) * 1.5)
    currY = 0

    """
    <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
             viewBox="0 0 3234.6 4525" style="enable-background:new 0 0 3234.6 4525;" xml:space="preserve">
    """
    oStr = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    oStr += "<!-- UML utilization SVG-->\n"
    oStr += "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\" "
    

    # need to track max height of row to adjust row spacing
    maxHT = 0
    oStr2 = ""
    for b in reversed(sorted(campus)):
        currY += gapY_newBldg
        oStr2 += addBldgLabel(b,(baseX-100), (currY+gapY_sameBldg+60))
        for f in reversed(sorted(campus[b])):
            maxX = baseX
            maxHT = 0
            currY += gapY_sameBldg
            for r in reversed(sorted(campus[b][f]["rooms"])):
                currRmHrs = str(campus[b][f]["rooms"][r]["RM_HRS"])
                try:
                    currCat = labCat[r]["LAB_MAJOR_CATEGORY"]
                except:
                    print("Not categorized", r)
                    currCat = "Dry"
                #print r, currCat
                moreStr,wdth,ht = makeSVGlab(r,currRmHrs,currCat,maxX,currY)
                oStr2 += moreStr
                maxX += wdth + gapX
                if (ht > maxHT):
                    maxHT = ht
        
                #print maxX
                #print b, f, r
    oStr += "viewBox=\"0 0 2000 " + str(currY) + "\" style=\"enable-background:new 0 0 1366 768;\" xml:space=\"preserve\">\n"
    oStr += "<style type=\"text/css\">\n"
    oStr += ".bAVGkey600 {fill: #59baed;}\n.bAVGkey450 {fill:#a0ccef;}\n.bAVGkey300 {fill: #f7eec3;}\n.bAVGkey150 {fill: #eda29f;}\n.bAVGkeylow {fill: #ec7e79;}\n"
    oStr += ".STEM5 {fill: #59baed; stroke: black; stroke-width:3}\n.STEM4 {fill:#a0ccef;stroke: black; stroke-width:3}\n.STEM3 {fill: #f7eec3;stroke: black; stroke-width:3}\n"
    oStr += ".STEM2 {fill: #eda29f;stroke: black; stroke-width:3}\n.STEM1 {fill: #ec7e79;stroke: black; stroke-width:3}\n"
    oStr += ".DRY5 {fill: #59baed; stroke: black; stroke-width:3; stroke-dasharray:3}\n.STEM4 {fill:#a0ccef;stroke: black; stroke-width:3; stroke-dasharray:3}\n"
    oStr += ".DRY3 {fill: #f7eec3;stroke: black; stroke-width:3; stroke-dasharray:3}\n.DRY2 {fill: #eda29f;stroke: black; stroke-width:3; stroke-dasharray:3}\n.DRY1 {fill: #ec7e79;stroke: black; stroke-width:3; stroke-dasharray:3}\n"
    oStr += ".st0{fill:#59baed;}\n.st1{text-align:center; font-family:'Frutiger';}\n.st2{font-size:9px;}\n.st3{font-weight:bold;}\n.st4{font-size:12px;}\n.st5{font-size:30px;}\n"
    oStr += "</style>\n"
    # Start group of all rooms
    oStr += "<g id=\"classrooms\">\n"
    oStr += oStr2
    oStr += "</g></svg>\n"
    ofile = open("C:\\temp\\2021F_Util\\" + campusName + "_ClassLabtest.svg","w")
    ofile.write(oStr)
    ofile.close()



def output_svg(theRooms, labCat):
    northCR = {}
    southCR = {}
    northCL = {}
    southCL = {}
    
    for r in theRooms:
        currRoom = theRooms[r]
        if currRoom == "PHYS_LABS":
            currBldg = "OLN"
            currFlr = "OLN-1"
        else:
            currBldg = r[:3]
            currFlr = r[:5]
        if currRoom["CAMPUS"] == "UMLNORTH":
            if currRoom["USE"] == "CLASSROOM":
                if currBldg not in northCR:
                    northCR[currBldg] = {currFlr:{"rooms":{r:currRoom}}}
                else:
                    if currFlr not in northCR[currBldg]:
                        northCR[currBldg][currFlr] = {"rooms":{r:currRoom}}
                    else:
                        northCR[currBldg][currFlr]["rooms"][r] = currRoom
            elif currRoom["USE"] == "CLASS LABORATORY":
                #PHYS_LABS: ???? Don't add to this dictionary
                if currBldg not in northCL:
                    northCL[currBldg] = {currFlr:{"rooms":{r:currRoom}}}
                else:
                    if currFlr not in northCL[currBldg]:
                        northCL[currBldg][currFlr] = {"rooms":{r:currRoom}}
                    else:
                        northCL[currBldg][currFlr]["rooms"][r] = currRoom
                        
        elif currRoom["CAMPUS"] == "UMLSOUTH":
            if currRoom["USE"] == "CLASSROOM":
                if currBldg not in southCR:
                    print(currBldg)
                    southCR[currBldg] = {currFlr:{"rooms":{r:currRoom}}}
                else:
                    if currFlr not in southCR[currBldg]:
                        southCR[currBldg][currFlr] = {"rooms":{r:currRoom}}
                    else:
                        southCR[currBldg][currFlr]["rooms"][r] = currRoom
            elif currRoom["USE"] == "CLASS LABORATORY":
                if currBldg not in southCL:
                    southCL[currBldg] = {currFlr:{"rooms":{r:currRoom}}}
                else:
                    if currFlr not in southCL[currBldg]:
                        southCL[currBldg][currFlr] = {"rooms":{r:currRoom}}
                    else:
                        southCL[currBldg][currFlr]["rooms"][r] = currRoom
    svgClassroomOut(northCR, "North", 0)
    svgClassroomOut(southCR, "South", 0)
    svgClassLabOut(northCL, "North", 0, labCat)
    svgClassLabOut(southCL, "South", 0, labCat)
"""
{"PTB":1007,"SOU":832,"KIT":670}
x is 804 for PTB,right hand column
"""
def makeSVGroom2(r,rmName):
    bAvg = r["BAvg"]
    numSeats = r["PHYS_CAP"]

    
    xpos = 10
    ypos = 10
    
    txtOffX = 18
    txtOffY = 15
    
    lblUtil =  str(bAvg)
    if lblUtil[0] == "0":
        lblUtil = lblUtil[1:5]
    else:
        lblUtil = lblUtil[:5]
    bCat = bAvgCat(bAvg)

    
    #class="st1 st2
    sizeW,sizeH = rmSize(numSeats)
    # need to adjust ypos based on sizeH so the line up at the bottom
    #ypos += (120 - sizeH) # 120 is hard coded -it's the height of medium and large rooms. need variable
    retVal = "<g id=\"" + rmName + "\">\n"
    retVal += "<rect x=\"" + str(xpos) + "\" y=\"" + str(ypos) + "\" width=\"" + str(sizeW) + "\" height=\"" + str(sizeH) + "\" class=\"" + bCat + "\" />\n"
    retVal += "<text id=\"lbl_" + rmName + "\" class=\"st1 st2\" x=\"" + str(xpos + (sizeW/2)) + "\" y=\"" + str(ypos + txtOffY) + "\" fill=\"black\">" + rmName + "</text>\n"
    retVal += "<text id=\"util_" + rmName + "\" class=\"st1 st4 st3\" x=\"" + str(xpos + (sizeW/2)) + "\" y=\"" + str(ypos + txtOffY+ txtOffY) + "\" fill=\"black\">" + lblUtil + "</text>\n"    
    retVal += "</g>\n"
    return(retVal)

def svgRoomOut(r,rmName, labCat):
    oDir = "C:\\temp\\_SVG\\"
    """
    for l in labCat:
        for k in labCat[l]:
            print "????", l, k, labCat[l][k]
    """
    """
    <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
             viewBox="0 0 3234.6 4525" style="enable-background:new 0 0 3234.6 4525;" xml:space="preserve">
    """
    oStr = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    oStr += "<!-- UML utilization SVG-->\n"
    oStr += "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\" "
    

    oStr2 = ""
                    

    oStr += "viewBox=\"0 0 100 100 \" style=\"enable-background:new 0 0 1366 768;\" xml:space=\"preserve\">\n"
    oStr += "<style type=\"text/css\">\n"
    oStr += ".bAVGkey600 {fill: #59baed;}\n.bAVGkey450 {fill:#a0ccef;}\n.bAVGkey300 {fill: #f7eec3;}\n.bAVGkey150 {fill: #eda29f;}\n.bAVGkeylow {fill: #ec7e79;}\n"
    oStr += ".DRY5 {fill: #59baed;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n.DRY4 {fill:#a0ccef;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n"
    oStr += ".DRY3 {fill: #f7eec3;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n"
    oStr += ".DRY2 {fill: #eda29f;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n.DRY1 {fill: #ec7e79;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n"

    oStr += ".st0{fill:#59baed;}\n.st1{text-align:center; font-family:'Frutiger';}\n.st2{font-size:9px;text-anchor:middle}\n.st3{font-weight:bold;}\n.st4{font-size:12px;text-anchor:middle}\n.st5{font-size:15px;text-anchor:middle}\n"
    oStr += ".st6{font-size:22px;text-anchor:middle}\n"
    oStr += "</style>\n"
    # Start group of all rooms
    #oStr += "<g id=\"classrooms\">\n"
    #oStr += oStr2
    currUse = r["USE"]
    currCampus = r["CAMPUS"]
    validCampuses = ["UMLNORTH","UMLSOUTH","UMLEAST"]
    if currCampus in validCampuses:
        if  currUse == "CLASSROOM":
            #ofile = open( (oDir + currCampus + "\\" + currUse + "\\" + rmName + ".svg"),"w")
            ofile = open( (oDir +  "SP23\\" +  rmName + ".svg"),"w")
            oStr += makeSVGroom2(r,rmName)
            oStr += "</svg>\n"
            ofile.write(oStr)
            ofile.close()
        elif currUse  == "CLASS LABORATORY":
            ofile = open( (oDir + currCampus + "\\" + currUse + "\\" + rmName + ".svg"),"w")
            #def makeSVGlab(rmName, rmHrs, labType, xpos, ypos):
            #oStr2,ignoreX, ignoreY = makeSVGlab(rmName, r["RM_HRS"],labCat[r]["LAB_MAJOR_CATEGORY"],0,0)
            #oStr2,ignoreX, ignoreY = makeSVGlab(rmName, r["RM_HRS"],"STEM",0,0)
            print(rmName)
            try:
                currCat = labCat[rmName]["LAB_MAJOR_CATEGORY"]
                print("OKOKOKOK", currCat)
            except:
                currCat = "STEM"
            oStr2,ignoreX, ignoreY = makeSVGlab(rmName, r["RM_HRS"],currCat,0,0)
            oStr += oStr2 + "</svg>\n"
            ofile.write(oStr)
            ofile.close()

def svgLabCSVout(labRMU):
    # oct 31, 2022 cCSV file with just labs, room hours calculated from SOC, has lab categories
    # ['WEE-311', '28.33333333', '0.708333333', 'Biology', 'STEM', 'South']
    # need to add phys labs
    oDir = "C:\\temp\\_SVG\\"
    oStr = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    oStr += "<!-- UML utilization SVG-->\n"
    oStr += "<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\" "
    

    oStr2 = ""
                    

    oStr += "viewBox=\"0 0 100 100 \" style=\"enable-background:new 0 0 1366 768;\" xml:space=\"preserve\">\n"
    oStr += "<style type=\"text/css\">\n"
    oStr += ".bAVGkey600 {fill: #59baed;}\n.bAVGkey450 {fill:#a0ccef;}\n.bAVGkey300 {fill: #f7eec3;}\n.bAVGkey150 {fill: #eda29f;}\n.bAVGkeylow {fill: #ec7e79;}\n"
    oStr += ".DRY5 {fill: #59baed;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n.DRY4 {fill:#a0ccef;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n"
    oStr += ".DRY3 {fill: #f7eec3;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n"
    oStr += ".DRY2 {fill: #eda29f;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n.DRY1 {fill: #ec7e79;stroke:#000000;stroke-miterlimit:10;stroke-width:2}\n"

    oStr += ".st0{fill:#59baed;}\n.st1{text-align:center; font-family:'Frutiger';}\n.st2{font-size:9px;text-anchor:middle}\n.st3{font-weight:bold;}\n.st4{font-size:12px;text-anchor:middle}\n.st5{font-size:15px;text-anchor:middle}\n"
    oStr += ".st6{font-size:22px;text-anchor:middle}\n"
    oStr += "</style>\n"

    currCampus = labRMU[5]
    currUse = "CLASS LABORATORY"
    rmName = labRMU[0]
    print (oDir + currCampus + "\\" + currUse + "\\" + rmName + ".svg")
    #ofile = open( (oDir + currCampus + "\\" + currUse + "\\" + rmName + ".svg"),"w")
    ofile = open( (oDir + "SP23\\" + rmName + ".svg"),"w")
    currCat = labRMU[4]

    oStr2,ignoreX, ignoreY = makeSVGlab(rmName, labRMU[1],currCat,0,0)
    oStr += oStr2 + "</svg>\n"
    ofile.write(oStr)
    ofile.close()
    print("OKOK")
