import pandas as pd
import mysql.connector as sqltor

mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")
x=789901234
# df=pd.read_sql(f"select signature from accountDetails where account_number = {x};",mycon)
df=pd.read_sql("select * from accountDetails;",mycon)

print(df.columns)
# df1=pd.read_sql("select account_holder from accountDetails where account_number=234567890;",mycon)
# print(df["signature"][0])


# emp=pd.read_sql("select * from emp ;",mycon)
# print(emp.columns)
# df.to_csv("accountDetails.csv",sep="|")