from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import mysql.connector as sqltor
from processing import *
from datetime import datetime


app = Flask(__name__)

mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")

    # df = pd.read_sql("select * from accountDetails;", mycon)
    # print(df.head())
dfa = pd.read_sql(f"select * from accountdetails;", mycon)  # account details table dataframe
emp = pd.read_sql(f'select * from emp;', mycon)  # employee table dataframe
date = pd.read_sql(f"select * from stat_acc;", mycon)  # stat_acc table dataframe
dat = pd.read_sql(f"select * from stat_acc;", mycon)
mycon.close()



@app.route('/')
def home():
    return render_template("index.html")


@app.route("/accblock")
def accblock1():
    return render_template("form-element.html")


@app.route("/accblock", methods=["POST"])
def accblock():
    # f = open("output.txt", "w")
    a = request.form["accnum"]
    b = request.form["empid"]
    c = request.form["emppin"]
    d = request.form["reason"]
    e = request.form["date"]

    value = False
    t1 = False
    if int(a) in dfa["account_number"].values:
        value = True
        if len(dfa["account_status"][findIndex(dfa, "account_status", a)]) == 14:
            if str(b) in emp["empid"].values and int(emp["pin"][findIndex(emp, "empid", b)]) == int(c):
                if len(date["date"][findIndex(date, "account_number", a)]) == 11:
                    t1 = True
                    dict1 = {"Reason": d, "Blocked": 1}
                    # to turn mm-dd-yyyy date which is e to dd-mm-yyyy
                    e = datetime.strptime(e, "%Y-%m-%d").strftime("%d-%m-%Y")
                    # print(type(d), d, dict1, type(dict1))
                    mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")
                    cursor = mycon.cursor()
                    query = "UPDATE accountDetails SET account_status = %s WHERE account_number = %s"
                    cursor.execute(query, (str(dict1), a))
                    quer = "UPDATE stat_acc SET date = %s WHERE account_number = %s"
                    cursor.execute(quer, (str(e), a))
                    mycon.commit()
                    cursor.close()
                    mycon.close()
                    # {"Blocked": 0}
            else:
                return render_template("employeenotfound.html")
        else:
            return render_template("accountalreadyblocked.html", reasonS="{}".format(reason(dfa["account_status"][findIndex(dfa, "account_number", a)])))
    else:
        return render_template("accountnotfound.html")
    # f.write(str(value))
    # f.write(str(t1))
    return redirect(url_for("accsucblock"))

@app.route("/accsucblock")
def accsucblock():
    return render_template("success.html")

@app.route("/accunblock")
def accunblock1():
    return render_template("unblockform.html")


@app.route("/accunblock", methods=["POST"])
def accunblock():
    # f = open("output.txt", "w")
    a = request.form["accnum"]
    b = request.form["empid"]
    c = request.form["emppin"]
    e = request.form["date"]

    value = False
    t1 = False
    if int(a) in dfa["account_number"].values:
        value = True
        if str(dfa["account_status"][findIndex(dfa, "account_status", a)]) != r"{'Blocked': 0}":
            if str(b) in emp["empid"].values and int(emp["pin"][findIndex(emp, "empid", b)]) == int(c):
                if len(dat["date"][findIndex(dat, "account_number", a)]) != 11:
                    t1 = True
                    dict1 = {"Blocked": 0}
                    f = open("output.txt", "w")
                    f.write(str(dat.columns))
                    # print(type(d), d, dict1, type(dict1))
                    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
                    cursor = mycon.cursor()
                    query = "UPDATE accountDetails SET account_status = %s WHERE account_number = %s"
                    cursor.execute(query, (str(dict1), a))
                    quer = "UPDATE stat_acc SET date = %s WHERE account_number = %s"
                    cursor.execute(quer, ("not blocked", a))
                    mycon.commit()
                    cursor.close()
                    mycon.close()

            else:
                return render_template("employeenotfound1.html")
        else:
            return render_template("accountalreadyunblocked.html")
    else:
        return render_template("accountnotfound1.html")

    return render_template('unblocksuccess.html')


if __name__ == '__main__':
    app.run(debug=True)
