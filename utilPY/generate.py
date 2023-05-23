from bs4 import BeautifulSoup as bs
layout_path = "../assets/Layout.PNG"
script_path = "index.js"
halls = {
    "DAN":"Dandeneau Hall",
    "GPS":"GPS",
    "PER":"Perry Hall",
    "BAL":"Ball Hall",
    "SHA":"Shah Hall",
    "SOU":"Southwick Hall",
    "FAL":"Falmouth Hall",
    "OLN":"Olney Hall",
    "OLS":"Olsen Hall",
    "PTB":"Pulichino Tong Business Center",
    "COB":"Coburn Hall",
    "DUG":"Dugan Hall",
    "HSS":"Health & Social Sciences Building",
    "MAH":"Mahoney Hall",
    "MCG":"McGauvran Center",
    "OLE":"O’Leary Library",
    "RIV":"Riverview Suites",
    "WEE":"Weed Hall",
    "WAN":"Wannalancit Business Center",
    }

HEAD = """
    <!doctype html>
    <html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <script src="index.js" defer></script>
    <title>Hello, world!</title>
    <style>
        .Imagecontainer {
            transform: translate(-50% -50%);
            margin: 0px 0px 0px 0px;
            padding: 0px 0px 0px 30px;
        }
        .grid-container {
          display: flex;
          flex-wrap: wrap;
          margin-bottom: 20px;
        }
        .main.full-width {
            flex: 1;
        }
        .grid-item {
          flex-basis: auto; /* Adjust the percentage value as needed */
          margin: 50px 50px 0 0px; /* Adjust the margins as needed */ /* top | right | bottom | left */
        }
        .no-padding-col {
          padding-left: 0;
          padding-right: 5px;
          padding-top: 5px;
        }
        /************** Modal **************/	
      .modal_NTBT {	
        position: fixed;	
        left: 0;	
        top: 0;	
        width: 100%;	
        height: 100%;	
        background-color: rgba(0, 0, 0, 0.5);	
        opacity: 0;	
        visibility: hidden;	
        transform: scale(1.1);	
        transition: visibility 0s linear 0.25s, opacity 0.25s 0s,	
          transform 0.25s;	
      }	
      .modal-content_NTBT {	
        position: absolute;	
        top: 50%;	
        left: 50%;	
        transform: translate(-50%, -50%);	
        background-color: white;	
        padding: 1rem 1.5rem;	
        width: auto;	
        max-height: 80vh;	
        overflow: auto;	
        display: flex;	
        flex-direction: row-reverse;	
      }	
      .contents_NTBT {	
        margin: 2.5rem;	
      }	
      .close-button_NTBT {	
        display: flex;	
        font-size: larger;	
        font-weight: bolder;	
        align-items: center;	
        justify-content: center;	
        width: 1.5rem;	
        height: 2rem;	
        cursor: pointer;	
        background-color: rgb(0, 0, 0);	
        color: white;	
      }	
      .close-button_NTBT:hover {	
        background-color: darkgray;	
        color: black;	
      }	
      .show-modal_NTBT {	
        opacity: 1;	
        visibility: visible;	
        transform: scale(1);	
        transition: visibility 0s linear 0s, opacity 0.25s 0s, transform 0.25s;	
      }	
      .triggerModal:hover {	
        cursor: pointer;	
      }
     @page {
      size: 11in 17in;
      margin: 0;
    }
        #container {
      width: 100%;
      /* Set any desired styles for the container */
    }

    #svg-element {
      width: 100%;
      height: auto;
    }

    /* Media queries for different screen sizes */
    @media (max-width: 767px) {
      #svg-element {
        /* Define the desired width and height for smaller screens */
        width: 200px;
        height: auto; /* Maintain aspect ratio */
      }
    }

    @media (min-width: 768px) and (max-width: 1023px) {
      #svg-element {
        /* Define the desired width and height for medium-sized screens */
        width: 300px;
        height: auto; /* Maintain aspect ratio */
      }
    }

    @media (min-width: 1024px) {
      #svg-element {
        /* Define the desired width and height for larger screens */
        width:120%;
        height:auto;/* Maintain aspect ratio */
      }
      .no-padding-col {
          padding-left: 0;
          padding-right: 20px;
          padding-top: 5px;
      }
    }
    .row {
      margin-left: 0px;
      margin-right: 0px;
    }
    </style>
  </head>
  <body>
"""
LAYOUT =  f"""
    <div class="col-sm-auto col-lg-auto col-md-auto col-xs-auto Imagecontainer">
        <div>
            <div class="d-flex justify-content-end ">
                <button onclick="onCloseLayout(true)">&#10006;</button>
            </div>
            <div class="d-flex justify-content-end ">
                <img  src="{layout_path}" alt="" />
            </div>
        </div>
    </div>
    <div class="ml-4">
        <button
            id="openLayout"
            style="display: none"
            onclick="onCloseLayout(false)"
            >LayOut &#8250;
        </button>
    </div>
"""
BODY_OPENING = f""" 
    <h3 class="text-center"><b>FALL 2022 -</b> North Campus Classroom Utilization</h3>
    <h6 class="text-center"><div id="timestamp1"> </div></h6>
    <div >
        <div class="row ">
            {LAYOUT}
            <div class="col">
                <div class="grid-container  d-flex justify-content-between">
                       
"""
BODY_CLOSING = """
                </div>
             </div>
        </div>
    </div>


"""
CLOSING  = """
 <!-- Modal -->
    <div class="modal_NTBT">
      <div class="modal-content_NTBT">
        <button class="close-button_NTBT" style="padding: 0px;">&times;</button>
        <div class="contents_NTBT"></div>
      </div>
    </div>
  <script>
    let timestamp1 = document.getElementById("timestamp1");
    let timestamp = Date.now();
    var d = new Date(timestamp);
    timestamp1.innerHTML = d;
 </script>
<!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.3/dist/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
  </body>
</html>
"""


import os
from collections import defaultdict
east_build = defaultdict(list)
south_build = defaultdict(list)
north_build = defaultdict(list)
path = "UMLEAST"
dir_list = os.listdir(path)
for i in dir_list:
    temp = i.split('-')
    name = temp[0]
    room = temp[1].split('.svg')[0]
    east_build[name].append(room)

path = "UMLNORTH"
dir_list = os.listdir(path)
for i in dir_list:
    temp = i.split('-')
    name = temp[0]
    room = temp[1].split('.svg')[0]
    north_build[name].append(room)

path = "UMLSOUTH"
dir_list = os.listdir(path)
for i in dir_list:
    temp = i.split('-')
    name = temp[0]
    room = temp[1].split('.svg')[0]
    south_build[name].append(room)


def segregate_rooms(list_rooms):
    alphanumeric_list = []
    numeric_list = []

    for element in list_rooms:
        if element.isdigit():
            numeric_list.append(int(element))
        else:
            alphanumeric_list.append(element)

    sorted_alphanumeric = sorted(alphanumeric_list)
    sorted_numeric = sorted(numeric_list)

    # now segregate the list
    if len(sorted_alphanumeric):
        segregated_list = [tuple(sorted_alphanumeric)]
    else:
        segregated_list  = []
    if len(sorted_numeric):
        rooms = sorted_numeric
        current_range = [rooms[0]] 
            # Start with the first number as the initial range
        for i in range(1,len(rooms)):
            diff = rooms[i]//100 - rooms[i-1]//100
            if diff == 0:
                current_range.append(rooms[i])
            else:
                segregated_list.append(tuple(current_range))
                current_range = [rooms[i]]
        segregated_list.append(current_range)
    return segregated_list



def build(campus,build_dict):
    grid_items= ""
    north_order = ["OLS","BAL","PER","OLN","SHA","FAL","SOU","DAN","PTB","GPS"]
    south_order = ["WEE","OLE","DUG","MCG","HSS","MAH","RIV","COB"]
    if  campus == 'UMLNORTH':
        order = north_order
    elif campus == "UMLSOUTH":
        order = south_order
    else:
        order = ['WAN']
    for build in order:
        segregated_list = segregate_rooms(build_dict[build])
        rows = ""
        for i in segregated_list[::-1]:
            items=""
            for j in i:
                path = campus+"/"+build +"-"+str(j)+".svg"
                anchor_path = "HTML"+"/"+build +"-"+str(j)+"_schedDetail.html"
                items += f"""
                    <div class="col-xs-auto col-sm-auto col-md-auto col-lg-auto no-padding-col">
                        <a href="{anchor_path}"><img src="{path}" id="svg-element" alt="" /></a>
                    </div>
                    """
            rows+= f"""
                        <div class="row align-items-end">
                        {items}
                        </div>   
                    """
        grid_items+=  f"""
                        <div class="grid-item d-flex align-items-end">
                             <div class="container triggerModal">
                             {rows}
                            <h5 class="row align-items-end">{halls[build].upper()}</h5>
                            </div>
                        </div>
                    """
    return HEAD+BODY_OPENING+grid_items+BODY_CLOSING+CLOSING

for i in ["UMLNORTH","UMLSOUTH","UMLEAST"]: # need to pass ,"UMLSOUTH","UMLEAST"
    if i=="UMLNORTH":
        building = north_build 
        page="North.html"
    elif i=="UMLSOUTH":
        building = south_build
        page="South.html"
    else:
        building = east_build
        page="East.html"
    html_page = build(i,building)
    soup = bs(html_page,features="html.parser")
    prettyHTML = soup.prettify()
    with open(page, "w",encoding="utf-8") as f:
        f.write(prettyHTML)  
        f.close()





    

            


            
        
           

