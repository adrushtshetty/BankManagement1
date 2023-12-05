import mysql.connector as sqltor
import pandas as pd
mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
passBook=pd.read_sql("select * from passbook;",mycon)
cursor = mycon.cursor()
for x, y in zip(passBook['passbk'], passBook['account_number']):
    t = (sum(list(map(float, ((x[1:-1]).split(", "))))))
    query = "UPDATE accountDetails SET balance = %s WHERE account_number = %s;"
    cursor.execute(query, (t, y))
mycon.commit()
cursor.close()
mycon.close()
