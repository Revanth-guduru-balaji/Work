
import os

def svgRoomOut(r,rmName, labCat):
    directory = "SVG"
    
    
   
    
    # Start group of all rooms
    #oStr += "<g id=\"classrooms\">\n"
    #oStr += oStr2
    currUse = r["USE"]
    currCampus = r["CAMPUS"]
    validCampuses = ["UMLNORTH","UMLSOUTH","UMLEAST"]
    if currCampus in validCampuses:
        if  currUse == "CLASSROOM":
            #ofile = open( (oDir + currCampus + "\\" + currUse + "\\" + rmName + ".svg"),"w")
            oStr = makeSVGroom2(r,rmName)
          
            oStr = oStr.strip()
            filepath = directory+"/"+  rmName + ".svg"
            # Create the directory if it does not exist
            if not os.path.exists(directory):
                os.makedirs(directory)
            # Write to the file
            with open(filepath, "w") as f:
                f.write(oStr)

        elif currUse  == "CLASS LABORATORY":
            
            filepath = directory+"/"+ rmName + ".svg"
            # Create the directory if it does not exist
            if not os.path.exists(directory):
                os.makedirs(directory)
           
            print(rmName)
            try:
                currCat = labCat[rmName]["LAB_MAJOR_CATEGORY"]
                print("OKOKOKOK", currCat)
            except:
                currCat = "STEM"
            oStr2,ignoreX, ignoreY = makeSVGlab(rmName, r["RM_HRS"],currCat,0,0)
            oStr = oStr2 
             # Write to the file
            oStr = oStr.strip()
            print(filepath)
            with open(filepath, "w") as f:
                f.write(oStr)
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

    color = bAvgCat(bAvg)
    retVal = rmSize(numSeats,rmName,lblUtil,color)
    return(retVal)

def rmHrCat(rmHrs, rmCat):
    retVal = ""
    util = float(rmHrs)/40.
    if rmCat == "STEM":
        if util > .75:
            #retVal = "STEM5"
            retVal = "#59baed"
        elif util > .50:
            #retVal = "STEM4"
            retVal = "#a0ccef"
        elif util > .33:
            #retVal = "STEM3"
            #retVal = "bAVGkey150"
            retVal = "#f7eec3"
        elif util > .16:
            #retVal = "STEM3"
            retVal ="#eda29f"
        else:
            #retVal = "STEM1"
            retVal = "#ec7e79"
    elif rmCat == "Dry":
        if util > .82:
            retVal = "#59baed"
        elif util > .67:
            retVal = "#a0ccef"
        elif util > .50:
            #retVal = "DRY2"
            retVal = "#f7eec3"
        elif util > .33:
            #retVal = "DRY2"
            retVal = "#eda29f"
        else:
            retVal = "#ec7e79"
    else:
        print("error: check lab major category")
    return retVal

def makeSVGlab(rmName, rmHrs, labType, xpos, ypos):
    txtOffX = 18
    txtOffY = 30
    #retVal = "<g id=\"" + rmName + "\" onclick=\"loadPhotoplan(&quot;SOU&quot;);\">\n"
    #bCat = bAvgCat(bAvg)
    #print rmName, labType
    color = rmHrCat(rmHrs, labType)
    currUtil = float(rmHrs)/40.
    utilStr = "{:.1%}".format(currUtil)
    #class="st1 st2
    #    sizeW,sizeH = rmSize(numSeats)
    sizeW = 100.
    sizeH = 100.
    # need to adjust ypos based on sizeH so the line up at the bottom
    ypos += (120 - sizeH) # 120 is hard coded -it's the height of medium and large rooms. need variable
 
    retVal = rmSize(30,rmName,utilStr,color)
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
                moreStr = makeSVGroom(r,currUtil, campus[b][f]["rooms"][r]["PHYS_CAP"],maxX,currY)
                oStr2 += moreStr
            currY -= gapY_sameBldg
            print("********************** done with floor, increment Y", currY)
                    

    
    oStr = oStr2
    
    # Define the directory and file path
    directory = "2021F_Util"
    filepath = directory+"/"+campusName + "_test.svg"

    # Create the directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write to the file
    with open(filepath, "w") as f:
        f.write(oStr)

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

    #class="st1 st2
    color = get_color(bAvg)
    retVal = rmSize(numSeats,rmName,lblUtil,color)
   
    return(retVal)
        
    
def bAvgCat(util):
    retVal = ""
    util = float(util)
    if util > .600:
        retVal = "#59baed" 
    elif util > .450:
        retVal = "#a0ccef" 
    elif util > .300: 
        retVal = "#f7eec3" 
    elif util > .150:
        retVal = "#eda29f" 
    else:
        retVal = "#ec7e79" 
    return retVal

def get_color(util):
    color = ''
    util = float(util)
    if util > .600:
        color = "#59baed" 
    elif util > .450:
        color = "#a0ccef" 
    elif util > .300: 
        color = "#f7eec3" 
    elif util > .150:
        color = "#eda29f" 
    else:
        color = "#ec7e79"
    return color

def rmSize(seats,rmName,lblUtil,color):
    
   
    try:
        seats = float(seats)
    except:
        seats = 1.
    
    if seats>0 and seats<17:
        #small.svg
        return f"""
               <svg xmlns="http://www.w3.org/2000/svg" width="60" height="50" viewBox="0 0 60 50" fill="none">
                    <rect fill="{color}" width="60" height="50" />
                    <text x="26" y="30" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{lblUtil}</text>
                    <text x="26" y="45" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{rmName}</text>
                </svg>

                """
    elif seats>17 and seats<34:
        #polygon.svg
        return f"""
               <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60" fill="none">
                <!-- Hexagon above the square -->
                <polygon points="1,60 60,60 60,20 45,0 15,0 1,20" fill="{color}" stroke="{color}" />
                <text x="30" y="40" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{lblUtil}</text>
                <text x="30" y="55" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{rmName}</text>
                </svg>

                """
    elif seats>34 and seats<50:
        #circle.svg for mdeium
        return f""" 
             <svg xmlns="http://www.w3.org/2000/svg" width="60" height="70" viewBox="0 0 60 70" fill="none">
                <!-- Hexagon above the square -->
                <polygon points="1,70 60,70 60,30 15,0 15,0 0,0" fill="{color}" stroke="{color}" />
                <text x="30" y="50" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{lblUtil}</text>
                <text x="30" y="65" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{rmName}</text>
            </svg>

              """
    elif seats>50 and seats<76:
        #large.svg for  large
        return f"""
                <svg xmlns="http://www.w3.org/2000/svg" width="72" height="80" viewBox="0 0 72 80" fill="none">
                    <rect fill="{color}" width="72" height="80" />
                    <text x="36" y="60" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{lblUtil}</text>
                    <text x="36" y="75" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{rmName}</text>
                </svg>

                """
        
    else:
        #lecture.svg for lecture
        return f"""
                <svg xmlns="http://www.w3.org/2000/svg" width="100" height="80" viewBox="0 0 100 80" fill="none">
                <rect fill="{color}" width="100" height="80" />
                <text x="50" y="60" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{lblUtil}</text>
                <text x="50" y="75" text-anchor="middle" font-family="Frutiger" font-size="12" fill="black">{rmName}</text>
                </svg>

                """
   


