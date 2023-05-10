import pyodbc
import json

def get_SoC():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=arcgis-sql.fs.uml.edu;'
                          'Database=SPACE;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM REGISTRAR_SCHEDULE_SRC')

    # build dictionary of field names, with numeric key for each
    field_names = {}
    num_fields = 0
    columns = [column[0] for column in cursor.description]
    for c in columns:
        field_names[num_fields] = c
        #print c
        num_fields += 1
        
    # walk the SQL data row by row
    i = 0
    SoC = {} # Schedule of Courses dictionary. Course ID will be row number
    for row in cursor:
        currRow = {} # dictionary for current row
        for j in range(0,num_fields):
            # add each field value, using field name as key
            #print row
            try:
                currRow[field_names[j]] = row[j].strip() # CHECK THIS! Had trouble with decimal            
            except:
                currRow[field_names[j]] = str(row[j]) # CHECK THIS! Had trouble with decimal
        # add current row's data, using space name as key
        SoC[i] = currRow
        i += 1
    print("pydobc sched rows: ", i)
    return(SoC)

def get_SpInv():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=arcgis-sql.fs.uml.edu;'
                          'Database=SPACE;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    # get space inventory view from SQL
    cursor.execute('SELECT * FROM V_ROOM_LIST')

    # build dictionary of field names, with numeric key for each
    field_names = {}
    num_fields = 0
    columns = [column[0] for column in cursor.description]
    for c in columns:
        field_names[num_fields] = c
        num_fields += 1
    # create dictionary for full space inventory
    spInv = {}

    # walk the SQL data row by row
    i = 0
    for row in cursor:
        currRow = {} # dictionary for current row
        for j in range(0,num_fields):
            # add each field value, using field name as key
            currRow[field_names[j]] = str(row[j]) # CHECK THIS! Had trouble with decimal
        # add current row's data, using space name as key
        spInv[row[14]] = currRow
        i += 1
    return(spInv)

def get_rmCapacities():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=arcgis-sql.fs.uml.edu;'
                          'Database=SPACE;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    # get space inventory view from SQL
    cursor.execute('SELECT * FROM R25_CAPACITY_FY22')

    # build dictionary of field names, with numeric key for each
    field_names = {}
    num_fields = 0
    columns = [column[0] for column in cursor.description]
    for c in columns:
        field_names[num_fields] = c
        num_fields += 1
    # create dictionary for full space inventory
    rmCap = {}

    # walk the SQL data row by row
    i = 0
    for row in cursor:
        currRow = {} # dictionary for current row
        for j in range(0,num_fields):
            # add each field value, using field name as key
            currRow[field_names[j]] = str(row[j]) # CHECK THIS! Had trouble with decimal
        # add current row's data, using space name as key
        rmCap[row[0]] = currRow
        i += 1
    return(rmCap)

def get_labCats_OLD():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=arcgis-sql.fs.uml.edu;'
                          'Database=SPACE;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    # get space inventory view from SQL
    cursor.execute('SELECT * FROM V_LAB_CATEGORIZED')

    # build dictionary of field names, with numeric key for each
    field_names = {}
    num_fields = 0
    columns = [column[0] for column in cursor.description]
    for c in columns:
        field_names[num_fields] = c
        num_fields += 1
    # create dictionary for full space inventory
    labCat = {}

    # walk the SQL data row by row
    i = 0
    for row in cursor:
        currRow = {} # dictionary for current row
        for j in range(0,num_fields):
            # add each field value, using field name as key
            currRow[field_names[j]] = str(row[j]) # CHECK THIS! Had trouble with decimal
        # add current row's data, using space name as key
        currLab = row[0].strip()
        labCat[currLab] = currRow
        i += 1
    return(labCat)

def get_labCats():
    #Updated Feb. 2023
    retVal = {}
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=arcgis-sql.fs.uml.edu;'
                          'Database=SPACE;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    # get space inventory view from SQL
    cursor.execute('SELECT * FROM V_USE_LAB_CATEGORY')

    # build dictionary of field names, with numeric key for each
    field_names = {}
    num_fields = 0
    columns = [column[0] for column in cursor.description]
    for c in columns:
        field_names[num_fields] = c
        num_fields += 1
    # create dictionary for full space inventory
    labCat = {}

    # walk the SQL data row by row
    i = 0
    for row in cursor:
        currRow = {} # dictionary for current row
        for j in range(0,num_fields):
            # add each field value, using field name as key
            currRow[field_names[j]] = str(row[j]) # CHECK THIS! Had trouble with decimal
        # DANGER! Assuming each space_name appears only once
        if currRow["USE_NAME"] == "CLASS LABORATORY":
            retVal[currRow["SPACE_NAME"]] = {"LAB_MAJOR_CATEGORY":currRow["LAB_MAJOR_CATEGORY"]}
        i += 1
    return(retVal)

Soc = get_SoC()
labCats = get_labCats()
labCats_old = get_labCats_OLD()
rmCapacities = get_rmCapacities()
SpInv = get_SpInv()

with open("Soc.json", "w") as outfile:
    json.dump(Soc, outfile)

with open("labCats.json", "w") as outfile:
    json.dump(labCats, outfile)

with open("labCats_old.json", "w") as outfile:
    json.dump(labCats_old, outfile)

with open("rmCapacities.json", "w") as outfile:
    json.dump(rmCapacities, outfile)

with open("SpInv.json", "w") as outfile:
    json.dump(SpInv, outfile)