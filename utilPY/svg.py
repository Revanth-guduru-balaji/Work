
import os
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
                    

    oStr = """
                <?xml version="1.0" encoding="utf-8"?>
                <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                viewBox="0 0 792 612" style="enable-background:new 0 0 792 612;" xml:space="preserve">
         """
    oStr += oStr2
    oStr += "</svg>\n"
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
    retVal = rmSize(numSeats,rmName,lblUtil,bAvg)
   
    return(retVal)
        
    
def bAvgCat(util):
    retVal = ""
    util = float(util)
    if util > .600:
        retVal = "bAVGkey600" #59baed
    elif util > .450:
        retVal = "bAVGkey450" #a0ccef
    elif util > .300: 
        retVal = "bAVGkey300" #f7eec3
    elif util > .150:
        retVal = "bAVGkey150" #eda29f
    else:
        retVal = "bAVGkeylow" #ec7e79
    return retVal


def rmSize(seats,rmName,lblUtil,util):
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
    fillcolor = ".st0{fill:"+color+";}"
    styles = """.st1{fill:none;}
                .st2{font-family:'FrutigerLTStd-Bold';}
                .st3{font-size:5.3427px;}
                .st4{font-family:'FrutigerLTStd-Roman';}
                .st5{font-size:4.1098px;}
                """
    style = f"""<style type="text/css">
                {fillcolor}
                {styles}
            </style>
            """
    try:
        seats = float(seats)
    except:
        seats = 1.
    
    if seats>0 and seats<17:
        #small.svg
        return style+f"""
                <rect x="57.19" y="78.14" class="st0" width="23.08" height="22.19"/>
                <rect x="57.19" y="88.35" class="st1" width="23.08" height="10.11"/>
                <text transform="matrix(1 0 0 1 62.0435 92.3594)"><tspan x="0" y="0" class="st2 st3">{lblUtil}</tspan><tspan x="-1.19" y="4.93" class="st4 st5">{rmName}</tspan></text>
                """
    elif seats>17 and seats<34:
        #polygon.svg
        return style+f"""
                <polygon class="st0" points="88.11,71.21 82.13,78.27 82.34,100.33 105.42,100.33 105.42,78.27 99.65,71.21 "/>
                <rect x="82.24" y="88.35" class="st1" width="23.08" height="10.11"/>
                <text transform="matrix(1 0 0 1 87.0923 92.3594)"><tspan x="0" y="0" class="st2 st3">{lblUtil}</tspan><tspan x="-1.19" y="4.93" class="st4 st5">{rmName}</tspan></text>
                """
    elif seats>34 and seats<50:
        #circle.svg for mdeium
        return style+f"""
                        
                <path class="st0" d="M107.55,79.62l-0.06,20.71h23.08V79.62c0,0-1.24-8.58-11.54-8.58S107.55,79.62,107.55,79.62z"/> 
                <rect x="107.49" y="88.35" class="st1" width="23.08" height="10.11"/>
                <text transform="matrix(1 0 0 1 112.3467 92.3594)"><tspan x="0" y="0" class="st2 st3">{lblUtil}</tspan><tspan x="-1.19" y="4.93" class="st4 st5">{rmName}</tspan></text> 
                """
    elif seats>50 and seats<76:
        #large.svg for  large
        return style+f"""
                            
                    <rect x="132.64" y="71.04" class="st0" width="23.08" height="29.29"/>
                    <rect x="132.64" y="88.35" class="st1" width="23.08" height="10.11"/>
                    <text transform="matrix(1 0 0 1 137.4985 92.3594)"><tspan x="0" y="0" class="st2 st3">{lblUtil}</tspan><tspan x="-1.19" y="4.93" class="st4 st5">{rmName}</tspan></text>
                """
        
    else:
        #lecture.svg for lecture
        return style+f"""
                <rect x="157.79" y="71.04" class="st0" width="36.25" height="29.29"/>
                <rect x="157.79" y="88.35" class="st1" width="36.25" height="10.11"/>
                <text transform="matrix(1 0 0 1 169.2339 92.3594)"><tspan x="0" y="0" class="st2 st3">{lblUtil}</tspan><tspan x="-1.19" y="4.93" class="st4 st5">{rmName}</tspan></text>
                """
   


