import re
import pyodbc
import pandas as pd
import sqlite3

# conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ppmipoc.database.windows.net;Port=1433;Database=PPMI_LATEST;UID=ppmiadmin;PWD=Masori123$')


# conn = pyodbc.connect(
#     'Driver={SQL Server Native Client 11.0};Server=localhost;Database=PPMI_LATEST;Trusted_Connection=yes;')

query = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:ppmipoc.database.windows.net,1433;Database=PPMI_LATEST;Uid=ppmiadmin;Pwd=Masori123$;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=120;'
conn = ''
cursor = ''
retry_flag = True
retry_count = 0
while retry_flag and retry_count < 5:
  try:
    if retry_count > 2:
        print('Connected SQL Server')
        conn = pyodbc.connect(query)
        cursor = conn.cursor()
        break
    else:
        print('Connected SQLite')
        conn = sqlite3.connect("db.db", check_same_thread=False)
        cursor = conn.cursor()
        break
  except:
    print("Retry after 1 sec")
    retry_count = retry_count + 1
    time.sleep(1)


def get_city():
    cities = pd.read_sql_query(
        "Select distinct City from Filtered_Data order by city", conn)
    cities = list(filter(lambda x: str(x) != '', cities['City'].tolist()))
    return cities


def get_diagnosis():
    entity = pd.read_sql_query(
        "Select distinct Current_TA_On_Stage as Diagnosis from Filtered_Data Where Current_TA_On_Stage !='' order by Current_TA_On_Stage", conn)
    entity = list(filter(lambda x: str(x) != '', entity['Diagnosis'].tolist()))
    return entity


def get_drug():
    entityDrug = pd.read_sql_query(
        "Select distinct Medicines from Master_Medicines order by Medicines", conn)

    entityDrug = list(filter(lambda x: str(x) != '',
                             entityDrug['Medicines'].tolist()))
    return entityDrug



def check_user(username, password):
    cursor.execute("Select * from Users Where username='" + username+"' and password='"+password+"' and status='Active'")

    is_caught = False
    row = cursor.fetchone() 
    while row:
        is_caught = True
        row = cursor.fetchone()

    return is_caught

    user = pd.read_sql_query("Select * from Users Where username='" +
                             username+"' and password='"+password+"' and status='Active'", conn)
    if user.empty:
        return False
    else:
        return True


def get_patient_details(zipcode, city, diagnosis, drug):
    if city == "--Select City--":
        city = ""
    if diagnosis == "--Select Diagnosis--":
        diagnosis = ""
    if drug == "--Select Drug--":
        drug = ""

    # query = "Exec [dbo].[Get_Patient_Details] '" + \
    #     zipcode + "','"+city+"','"+diagnosis+"','"+drug+"'"

    query = "select Patient_Number " + \
        ",City " + \
        ",Current_TA_On_Stage " + \
        ",Current_Medicine " + \
        ",LifeStyle " + \
        ",Date_On_Stage_1 as Medicine_Date_On_Stage_1 " + \
        ",Date_On_Stage_2 as Medicine_Date_On_Stage_2 " + \
        ",Date_On_Stage_3 as Medicine_Date_On_Stage_3 " + \
        ",Date_On_Stage_4 as Medicine_Date_On_Stage_4 " + \
        ",Date_On_Stage_5 as Medicine_Date_On_Stage_5 " + \
        ",Date_On_Stage_6 as Medicine_Date_On_Stage_6 " + \
        ",Date_On_Stage_7 as Medicine_Date_On_Stage_7 " + \
        ",Date_On_Stage_8 as Medicine_Date_On_Stage_8 " + \
        ",Medicine_On_Stage_1 " + \
        ",Medicine_On_Stage_2 " + \
        ",Medicine_On_Stage_3 " + \
        ",Medicine_On_Stage_4 " + \
        ",Medicine_On_Stage_5 " + \
        ",Medicine_On_Stage_6 " + \
        ",Medicine_On_Stage_7 " + \
        ",Medicine_On_Stage_8 " + \
        ",TA_On_Stage_1 " + \
        ",TA_On_Stage_2 " + \
        ",TA_On_Stage_3 " + \
        ",TA_On_Stage_4 " + \
        ",TA_On_Stage_5 " + \
        ",TA_On_Stage_6 " + \
        ",TA_On_Stage_7 " + \
        ",TA_On_Stage_8 " + \
        ",Symptom_On_Stage_1 " + \
        ",Symptom_On_Stage_2 " + \
        ",Symptom_On_Stage_3 " + \
        ",Symptom_On_Stage_4 " + \
        ",Symptom_On_Stage_5 " + \
        ",Symptom_On_Stage_6 " + \
        ",Symptom_On_Stage_7 " + \
        ",Symptom_On_Stage_8 " + \
        ",Latest_MRI_Date " + \
        ",Is_GMR_Changed " + \
        ",MRI_Scan_Stage " + \
        "from Filtered_Data " + \
        "where "

    if zipcode != '':
        query = query + " Zipcode='" + zipcode + "'"

    if city != '':
        if zipcode != '':
            query = query + " and City='" + city + "'"
        else:
            query = query + " City='" + city + "'"

    if diagnosis != '':
        if zipcode != '' or city != '':
            query = query + " and (TA_On_Stage_1= '" + diagnosis + "'" + \
                "or TA_On_Stage_2 = '" + diagnosis + "'" + \
                "or TA_On_Stage_3 = '" + diagnosis + "'" + \
                "or TA_On_Stage_4 = '" + diagnosis + "'" + \
                "or TA_On_Stage_5 = '" + diagnosis + "'" + \
                "or TA_On_Stage_6 = '" + diagnosis + "'" + \
                "or TA_On_Stage_7 = '" + diagnosis + "'" + \
                "or TA_On_Stage_8 = '" + diagnosis + "'" + ")"
        else:
            query = query + " (TA_On_Stage_1= '" + diagnosis + "'" + \
                "or TA_On_Stage_2 = '" + diagnosis + "'" + \
                "or TA_On_Stage_3 = '" + diagnosis + "'" + \
                "or TA_On_Stage_4 = '" + diagnosis + "'" + \
                "or TA_On_Stage_5 = '" + diagnosis + "'" + \
                "or TA_On_Stage_6 = '" + diagnosis + "'" + \
                "or TA_On_Stage_7 = '" + diagnosis + "'" + \
                "or TA_On_Stage_8 = '" + diagnosis + "'" + ")"

    if drug != '':
        if zipcode != '' or city != '' or diagnosis != '':
            query = query + " and (Medicine_On_Stage_1 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_2 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_3 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_4 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_5 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_6 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_7 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_8 like '" + '%' + drug + '%' + "'" + ")"
        else:
            query = query + " (Medicine_On_Stage_1 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_2 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_3 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_4 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_5 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_6 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_7 like '" + '%' + drug + '%' + "'" + \
                "or Medicine_On_Stage_8 like '" + '%' + drug + '%' + "'" + ")"

    p_det = pd.read_sql_query(query, conn)

    return p_det


def get_similar_patient_details(patientnumber, lifestyle):
    # query = "Exec [dbo].[Get_Similar_Patient] '" + \
    #     patientnumber + "','"+lifestyle+"'"

    query = "select distinct " + \
        "Patient_Number " + \
        ",City " + \
        ",Current_TA_On_Stage " + \
        ",Current_Medicine " + \
        ",LifeStyle " + \
        ",Date_On_Stage_1 as Medicine_Date_On_Stage_1 " + \
        ",Date_On_Stage_2 as Medicine_Date_On_Stage_2 " + \
        ",Date_On_Stage_3 as Medicine_Date_On_Stage_3 " + \
        ",Date_On_Stage_4 as Medicine_Date_On_Stage_4 " + \
        ",Date_On_Stage_5 as Medicine_Date_On_Stage_5 " + \
        ",Date_On_Stage_6 as Medicine_Date_On_Stage_6 " + \
        ",Date_On_Stage_7 as Medicine_Date_On_Stage_7 " + \
        ",Date_On_Stage_8 as Medicine_Date_On_Stage_8 " + \
        ",Medicine_On_Stage_1 " + \
        ",Medicine_On_Stage_2 " + \
        ",Medicine_On_Stage_3 " + \
        ",Medicine_On_Stage_4 " + \
        ",Medicine_On_Stage_5 " + \
        ",Medicine_On_Stage_6 " + \
        ",Medicine_On_Stage_7 " + \
        ",Medicine_On_Stage_8 " + \
        ",TA_On_Stage_1 " + \
        ",TA_On_Stage_2 " + \
        ",TA_On_Stage_3 " + \
        ",TA_On_Stage_4 " + \
        ",TA_On_Stage_5 " + \
        ",TA_On_Stage_6 " + \
        ",TA_On_Stage_7 " + \
        ",TA_On_Stage_8 " + \
        ",Symptom_On_Stage_1 " + \
        ",Symptom_On_Stage_2 " + \
        ",Symptom_On_Stage_3 " + \
        ",Symptom_On_Stage_4 " + \
        ",Symptom_On_Stage_5 " + \
        ",Symptom_On_Stage_6 " + \
        ",Symptom_On_Stage_7 " + \
        ",Symptom_On_Stage_8 " + \
        ",Latest_MRI_Date " + \
        ",Is_GMR_Changed " + \
        ",MRI_Scan_Stage " + \
        "from Filtered_Data  " + \
        "where  " + \
        "[Patient_Number]!='"+patientnumber+"' and LifeStyle='"+lifestyle+"'"

    p_det = pd.read_sql_query(query, conn)

    return p_det


def get_hcp_details(city):
    # query = "Exec [dbo].[Get_HCP_Details] '" + \
    #     city + "'"

    query = "select distinct * " + \
        "from HCP_Details  " + \
        "where  " + \
        "city='"+city+"'"

    p_det = pd.read_sql_query(query, conn)
    return p_det
