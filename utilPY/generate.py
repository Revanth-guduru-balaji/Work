HEAD = """
    <!doctype html>
    <html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <script src="boot.js" defer></script>
    <title>Hello, world!</title>
    <style>
        .Imagecontainer {
            transform: translate(-50% -50/%);
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
          margin: 50px 0 0 70px; /* Adjust the margins as needed */ /* top | right | bottom | left */
        }
        .no-padding-col {
          padding-left: 0;
          padding-right: 10px;
          padding-top: 5px;
        }
    </style>
  </head>
"""
ROW_ITEM = """ 
    <div class="row align-items-end ">

     </div>
"""
COL_ITEM = """
    <div class="col-xs-auto col-sm-auto col-md-auto col-lg-auto no-padding-col">
    
    </div>
"""
ITEM_TITLE = """
    <h5 >Olsen Hall</h5>  
"""
GRID_ITEM  = """
    <div  class="grid-item d-flex align-items-end ">
            <div class="container">
       
            </div>
    </div>
"""
LAYOUT =  """
    <div class="col-sm-4 Imagecontainer">
        <div>
            <div class="d-flex justify-content-end ">
                <button onclick="onCloseLayout(true)">&#10006;</button>
            </div>
            <div class="d-flex justify-content-end ">
                <img class="triggerModal" src="assets/Layout.PNG" alt="" />
            </div>
        </div>
    </div>
    <button
        id="openLayout"
        style="display: none"
        onclick="onCloseLayout(false)"
        >LayOut &#8250;
    </button>
"""
BODY_OPENING = f""" 
    <h3 class="text-center"><b>FALL 2022 -</b> North Campus Classroom Utilization</h3>
    <div >
        <div class="row ">
            {LAYOUT}
            <div class="col">
                <div class="grid-container ">
                       
"""
BODY_CLOSING = """
                </div>
             </div>
        </div>
    </div>


"""
CLOSING  = """
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
    room = temp[1]
    east_build[name].append(room)

path = "UMLNORTH"
dir_list = os.listdir(path)
for i in dir_list:
    temp = i.split('-')
    name = temp[0]
    room = temp[1]
    north_build[name].append(room)

path = "UMLSOUTH"
dir_list = os.listdir(path)
for i in dir_list:
    temp = i.split('-')
    name = temp[0]
    room = temp[1]
    south_build[name].append(i)

sorted_build_north = sorted(north_build, key=lambda k: len(north_build[k]))
sorted_build_south = sorted(south_build, key=lambda k: len(south_build[k]))
sorted_build_east  = sorted(east_build, key=lambda k: len(east_build[k]))


def build(build_dict):
    for i in build_dict:
        OStr=""
        for j in i: 
            OStr  += f"""
                    <div class="col-xs-auto col-sm-auto col-md-auto col-lg-auto no-padding-col">
                    {j}
                    </div>
                """
           

