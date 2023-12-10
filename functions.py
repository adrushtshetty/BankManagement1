import pandas as pd
import mysql.connector as sqltor
from  processing import *

mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")
df=pd.read_sql("select * from accountDetails ;",mycon)
passBook=pd.read_sql("select * from passbook;",mycon)
emp=pd.read_sql("select * from emp;",mycon)
# print(df.columns)
# print(passBook.columns)

def findIndex(emp,column,empID):
    for x in range(len(emp[column])):
        if empID == emp[column][x]:
            ind = x
    return ind


# def refreshBalanceFromPassBook():
#     """Refreshes the balance from the table passBook"""
#     cursor = mycon.cursor()
#     res=[]
#     for x,y in zip(passBook['passbk'],passBook['account_number']):
#         t=(sum(list(map(int,(x.split(","))))))
#         cursor.execute(f"UPDATE accountDetails SET amount = {t} WHERE account_number = {y};")
#         mycon.commit()
#         cursor.close()

def checkFBalance(amount, df, f):
    if df['balance'][findIndex(df, "account_number", f)] - amount > 0:
        return (True)
    else:
        return (False)

empID="A123"
empPass="1234"
amount=2000
f=789901234
t=123234567
# Check if sender has enough balance
# def checkFBalance(amount,df,f):
#         if df['balance'][findIndex(df,"account_number",f)]-amount>0:
#             return(True)
#         else:
#             return(False)
# print(checkFBalance(amount,df,f))

# Check account status
# 14
# if (len(df['account_status'][findIndex(df,'account_number',f)]))>14:
#     msg=(reason(df['account_status'][findIndex(df,'account_number',f)]))
#     #render_template()
# else:
#     # passed for transaction

# Checking if account is found or not
# t=123
# if not(t in df['account_number']):
#     print(True)
#     #render_template()
# else:
#     # passed for transaction

# Check account status
# 14
# if (len(df['account_status'][findIndex(df,'account_number',f)]))>14:
#     msg=(reason(df['account_status'][findIndex(df,'account_number',f)]))
#     #render_template()
# else:
#     # passed for transaction

# SUBTRACT
amount=2000
f=789901234
t=123234567
fInd=findIndex(passBook,"account_number",f)
tInd=findIndex(passBook,"account_number",t)


# s=(passBook['passbk'][tInd])[1:-1]
# print(s.split(", "))

# fL=GETpassbk(fInd,passBook)
# tL=GETpassbk(tInd,passBook)
# fL.append(-float(amount))
# print(fL)
#
# tL.append(float(amount))
# print(tL)


#
# mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")
# cursor=mycon.cursor()
# query = "UPDATE passbook SET passbk = %s WHERE account_number = %s"
# cursor.execute(query, (str(fL), f))
# cursor.execute(query, (str(tL), t))
# mycon.commit()
# cursor.close()
# mycon.close()

#
# refreshBalanceFromPassBook(passBook)
#

f=789901234
# ind1 = None
# for x in range(len(df["account_number"])):
#     if f == df["account_number"][x]:
#         ind1 = x
# diff = float(df['balance'][ind1]) - amount
# if diff > 0:
#     print(ind1)
#     print (True, diff)
# else:
#     print (False, diff * -1)
# def f1(df,f,amount):
#     ind1=None
#     for x in range(len(df["account_number"])):
#         if f == df["account_number"][x]:
#             ind1 = x
#     diff=float(df['balance'][ind1]) - amount
#     if diff> 0:
#         return (True,diff)
#     else:
#         return (False,diff*-1)
# if (f1(df,str(123234567),2000)):
#     print("Block working")

# a=2000
# if checkFBalance(a, df, f):
#     print("Works")
# else:
#     print("Change")

print(sum([10000.0, 10000.0, -3000.0, 0.9, 2000.0, -1000.0, -1000.0, -1000.0]))
# print(refreshBalanceFromPassBook(passBook))


# import mysql.connector as sqltor
# mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
# cursor = mycon.cursor()
# for x, y in zip(passBook['passbk'], passBook['account_number']):
#     t = (sum(list(map(float, ((x[1:-1]).split(", "))))))
#     query = "UPDATE accountDetails SET balance = %s WHERE account_number = %s;"
#     cursor.execute(query, (t, y))
# mycon.commit()
# cursor.close()
# mycon.close()

# refreshBalanceFromPassBook(passBook)
# from processing import *
# print(AccountValidity(1234567812345,df))
#print(findIndex(df,"account_number",1234567812345))
d={}
for x,y in zip(df['account_number'].values,df['balance'].values):
    d[x]=y
# print(d)



import pandas as pd
import mysql.connector as sqltor
from  processing import *

# mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")
# df=pd.read_sql("select * from accountDetails ;",mycon)
f=567789012
t=567890123
f=567789012
t=567890123
# t=567789012
# print(AccountValidity(f,df))
# print(AccountValidity(t,df))
# print("-"*100)
# for x in df["account_number"].values:
#     print(type(int(x)))
# if f in df["account_number"].values

# print(int(f) in (list(map(int,list(df["account_number"].values)))))
# print((list(map(int,list(df["account_number"].values)))))
# print(t in (list(map(int,list(df["account_number"].values)))))


# acc=numbers_list = [123234567, 123345678, 123456789, 234345678, 234456789, 234567890, 345456789, 345567890, 345678901, 456567890, 456678901, 456789012, 567678901, 567789012, 567890123, 678789012, 678890123, 678901234, 789012345, 789901234, 890012345, 890123456, 901123456, 901234567, 987654321]
#
# res = [[10000, 10000, -3000, 0.9],[2000, 2000, -100, 600, 0.5], [5000, 5000, 0],[2000, 2000, 0.1], [8000, 8000, 0.7], [2000, 3000, 0.75], [3000, 3000, 0.25], [4000, 3500, 0.8], [1000, 500, 0.25], [6000, 6000, 0.5], [1000, 1000, 0.95], [4000, 4000, 0.9], [16000, 16000, 0.75], [1500, 1500, 0.1], [15000, 15000, 0.2]]
# for x,y in zip(acc,res):
#     cursor = mycon.cursor()
#     t=str(y)
#     cursor.execute(f"UPDATE passBook SET passbk = {t} WHERE account_number = {x};")
#     mycon.commit()
#     cursor.close()
#     # print(x,t)
#
# print(sum([10000, 10000, -3000, 0.9]))
#


# elements = [123234567, 123345678, 123456789, 234345678, 234456789, 234567890, 345456789, 345567890, 345678901, 456567890, 456678901, 456789012, 567678901, 567789012, 567890123, 678789012, 678890123, 678901234, 789012345, 789901234, 890012345, 890123456, 901123456, 901234567, 987654321]
# modified_data = [[10000, 10000, -3000, 0.9], [-2000, 500, 4000, 0.5], [5000, 5000, 0, 0.0], [-1000, 1000, 3000, 0.1], [10000, 6000, -1000, 0.7], [-2000, 7000, -2000, 0.75], [500, 2000, 3000, 0.25], [2000, 2000, 3500, 0.8], [0, 1500, 0, 0.25], [10000, 1000, 1000, 0.5], [-1000, 2000, 1000, 0.95], [2000, 2000, 4000, 0.9], [10000, 20000, 2000, 0.75], [-1000, 1000, 3000, 0.1], [15000, 15000, 0, 0.2], [8000, 901, 0, 0.0], [-500, 1000, 8000, 0.0], [-3000, 6000, -544.0], [8000, 1000, 12, 0.0], [8000, 901, 0, 0.0], [8000, 1000, 12, 0.0], [4000, 1000, 678, 0.0], [-500, 500, 1234, 0.0], [-500, 500, 1234, 0.0], [4000, 1000, 678, 0.0]]
#
# print(len(modified_data))

f=123234567
t=123345678
a=float(100)
df3 = passBook
passbok = {x:y for x,y in zip(df3["account_number"],df3["passbk"])}
passbok[f]=str(list(map(float,passbok[f][1:-1].split(", ")))+[-a])
passbok[t]=str(list(map(float,passbok[f][1:-1].split(", ")))+[a])
# print(passbok[f])
# print(passbok[t])
# print(type(list(passbok.keys())[0]))
# l=[10000.0, 10000.0, -3000.0, 0.9, 2000.0, -1000.0, -1000.0, -1000.0, -100.0]
#
# print(sum(l))
# a="adrusthshetty@gmail.com"
# b="adrushtshetty@gmail.com"
# print(a==b)
# print(str(list(map(float,passbok[f][1:-1].split(", ")))))
# print(str(list(map(float,passbok[t][1:-1].split(", ")))))
# print()
from datetime import datetime

print(list(map(lambda x: x.strftime("%d-%m-%Y"),(list(map(lambda x : (datetime.strptime(x, "%Y-%m-%d")),(list(map(lambda x: x[1:-1],passBook['date'][findIndex(passBook,'account_number',f)][1:-1].split(", "))))))))))

# from datetime import datetime
#
# # Original list of strings in "YYYY-MM-DD" format
# original_dates = ["2023-01-15", "2023-02-20", "2023-03-25", "2023-04-30"]
#
# datetime_objects = [datetime.strptime(date, "%Y-%m-%d") for date in original_dates]
#
# # Convert datetime objects to strings in "DD-MM-YYYY" format
# formatted_dates = [date.strftime("%d-%m-%Y") for date in datetime_objects]
#
# # Print the original and formatted dates
# print("Original Dates:", original_dates)
# print("Formatted Dates:", formatted_dates)
t='adrushtshetty@gmail.com'
print(df['account_number'][findIndex(df,'email',t)])
print(list(map(float,passBook['passbk'][findIndex(passBook,'account_number',df['account_number'][findIndex(df,'email',t)])][1:-1].split(", "))))