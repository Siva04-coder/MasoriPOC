import pyodbc
import pandas as pd

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Port=1433;'
                      'Database=PPMI_LATEST;'
                      'Trusted_Connection=yes;')

pd.read_sql_query("Select * from [dbo].[Code_List]")

