import re
import pyodbc
import pandas as pd


conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ppmipoc.database.windows.net;Port=1433;Database=PPMI_LATEST;UID=ppmiadmin;PWD=Masori123$')


def get_city():
    cities = pd.read_sql_query(
        "Select distinct City from Filtered_Data", conn)
    cities = list(filter(lambda x: str(x) != '', cities['City'].tolist()))
    return cities


def get_diagnosis():
    entity = pd.read_sql_query(
        "Select distinct Current_TA_On_Stage as Diagnosis from Filtered_Data Where Current_TA_On_Stage !=''", conn)
    entity = list(filter(lambda x: str(x) != '', entity['Diagnosis'].tolist()))
    return entity


def get_drug():
    entityDrug = pd.read_sql_query(
        "Select distinct Medicines as Current_Medicine from Master_medicines", conn)
    entityDrug = list(filter(lambda x: str(x) != '',
                             entityDrug['Current_Medicine'].tolist()))
    return entityDrug


def check_user(username, password):
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

    query = "Exec [dbo].[Get_Patient_Details] '" + \
        zipcode + "','"+city+"','"+diagnosis+"','"+drug+"'"
    p_det = pd.read_sql_query(query, conn)

    return p_det


def get_similar_patient_details(patientnumber, lifestyle):
    
    query = "Exec [dbo].[Get_Similar_Patient_Details] '" + \
        patientnumber + "','"+lifestyle+"'"

    print(query)
    p_det = pd.read_sql_query(query, conn)

    return p_det

