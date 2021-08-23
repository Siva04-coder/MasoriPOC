import pyodbc
import pandas as pd

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=localhost;'
                      'Port=1433;'
                      'Database=PPMI_LATEST;'
                      'Trusted_Connection=yes;')

def get_city():
    cities = pd.read_sql_query("Select (Case "
		"when rsqg1city!='nan' then rsqg1city "
		"when rsqf1city!='nan' then rsqf1city "
		"when rsqe1city!='nan' then rsqe1city "
		"when rsqd1city!='nan' then rsqd1city "
		"when rsqc1city!='nan' then rsqc1city "
		"when rsqb1city!='nan' then rsqb1city "
		"when rsqa1city!='nan' then rsqa1city "
		"else '' "
		"End) as City "
        "from [dbo].[FOUND_RFQ_Residential_History] order by City", conn)
    cities = list(filter(lambda x: str(x) != '', cities['City'].tolist()))
    return cities

def get_diagnosis():
    entity = pd.read_sql_query("Select Distinct D.Therapeutic_Area as Diagnosis from [dbo].[FOUND_RFQ_Residential_History] R "
    "Join [dbo].[Concomitant_Medications] C On R.patno = C.Patient_Number_PATNO "
    "Join [dbo].[Drug_To_Therapeutic_Area] D On C.WHO_DRUG_NAME_WHODRUG = D.Drug_Name order by Diagnosis", conn)
    entity = list(filter(lambda x: str(x) != '', entity['Diagnosis'].tolist()))
    return entity

def get_drug():
    entityDrug = pd.read_sql_query("Select Distinct D.Drug_Name as Drug from [dbo].[FOUND_RFQ_Residential_History] R "
    "Join [dbo].[Concomitant_Medications] C On R.patno = C.Patient_Number_PATNO "
    "Join [dbo].[Drug_To_Therapeutic_Area] D On C.WHO_DRUG_NAME_WHODRUG = D.Drug_Name order by Drug", conn)
    entityDrug = list(filter(lambda x: str(x) != '', entityDrug['Drug'].tolist()))
    return entityDrug

def check_user(username, password):
    user = pd.read_sql_query("Select * from Users Where username='"+username+"' and password='"+password+"' and status='Active'", conn)
    if user.empty:
        return False
    else:
        return True
        
def get_patient_details(zipcode, city, diagnosis, drug):
    p_det = pd.read_sql_query("Exec [dbo].[Get_Patient_Details] '" + zipcode + "','"+city+"','"+diagnosis+"','"+drug+"'", conn)

    return p_det

