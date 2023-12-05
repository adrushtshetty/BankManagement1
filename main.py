from flask import Flask, request, jsonify, render_template, url_for, redirect
import pandas as pd
app = Flask(__name__)
from processing import *

import pandas as pd
import mysql.connector as sqltor

mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")
df=pd.read_sql("select * from accountDetails;",mycon)
emp=pd.read_sql("select * from emp;",mycon)
passBook=pd.read_sql("select * from passbook;",mycon)
mycon.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'dev':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/chequeBookClearance")
def chkBkClrFrm():
    return render_template("chequeBookClearance.html")

@app.route("/chequeBookClearanceKEYFailed")
def chequeBookClearanceKEYFailed():
    return render_template("chequeBookClearanceKEYFailed.html")

@app.route("/chequeBookClearanceIFSCFailed")
def chequeBookClearanceIFSCFailed():
    return render_template("chequeBookClearanceIFSCFailed.html")

@app.route("/chequeBookClearanceAccountNotFoundFailed")
def chequeBookClearanceAccountNotFoundFailed():
    return render_template("chequeBookClearanceAccountNotFoundFailed.html")

@app.route("/chequeBookClearanceTransacted")
def chequeBookClearanceTransacted():
    return render_template("chequeBookVerifyTaransact.html")

@app.route("/chequeBookClearanceAccountBlocked")
def chequeBookClearanceAccountBlocked():
    return render_template("chequeBookClearanceAccountBlocked.html")


@app.route("/chequeBookClearance", methods=['POST'])
def chkVerify():
    """
    789901234 | "signature17.jpg" | "210987543" | "michael@email.com" | "LMNOPQ12345" | "567 Pine St" | "Michael" | 8901 | "Savings" | {
        "Blocked": 1, "Reason": "Account frozen"} | "MNO789" | ['key33', 'key34'] | 14000.50
    """
    if request.method=='POST':
        f=(request.form['from'])
        t = request.form['to']
        name = request.form['name']
        k = request.form['key']
        i=request.form['ifsc']
        a = request.form['amount']

        with open('temp.txt', 'w') as file:
            file.write(f"{f}\n{t}\n{name}\n{k}\n{i}\n{a}")
        path="static/signatures/"
        if not(AccountValidity(t,df)) or not(AccountValidity(f,df)):
            file1=open("debug.txt","w")
            file1.write("Failed account credentials")
            file.close()
            AccNotFound=""
            if not(AccountValidity(f,df)):
                AccNotFound="Recipient's Account"
            elif not (AccountValidity(t, df)):
                AccNotFound = "Sender's Account"

            return render_template("chequeBookClearanceAccountNotFoundFailed.html", accNotFound='{}'.format(AccNotFound))

        # elif (AccountValidity(f,df)):
        #     file1 = open("debug.txt", "w")
        #     file1.write("Failed from account")
        #     file.close()
        #     return redirect(url_for('chequeBookClearanceAccountNotFoundFailed'))

        elif (AccountValidity(f,df)) and (AccountValidity(t,df)):
            file1 = open("debug.txt", "w")
            file1.write("Verified both accounts")
            file.close()

            for x in range(len(df["account_number"])):
                if int(df['account_number'][x]) == int(f):
                    ind = x
                    print("IND FOUND")
            # ind=findIndex(df, "account_number", df)

            keys=keysExtractions(df["keys_array"][ind])
            print(type(keys))
            path="static/signatures/"
            if (k in keys) and (i==df["ifsc_code"][ind]):
                chk=1
                file1 = open("debug.txt", "w")
                file1.write("Signature")
                file.close()
                print("SIGNATURE FOUND")

                path+=df['signature'][ind]

                # SQL PART
                # mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
                # df1=pd.read_sql(f"select signature from accountDetails where account_number = {int(f)};", mycon)
                # mycon.close()
                # path+=df1["signature"][0]


                print(path)

                return render_template("chequeBookVerify.html", FaccNo='{}'.format(f), TaccNo='{}'.format(t),
                                       Name='{}'.format(name), chkKey='{}'.format(k), Amount='{}'.format(a),
                                       img_path='{}'.format(path),IFSC='{}'.format(i))


            elif not(k in keys):
                print("here")
                return redirect(url_for('chequeBookClearanceKEYFailed'))

            elif not(i==df["ifsc_code"][ind]):
                return redirect(url_for('chequeBookClearanceIFSCFailed'))



@app.route("/chequeBookTransacted", methods=['POST'])
def chkTransaction():
    if request.method=='POST':
        import mysql.connector as sqltor
        eI =str(request.form['empID'])
        # f=request.form['from']
        # t = request.form['to']
        # name = request.form['name']
        # i=request.form['ifsc']
        # k = request.form['key']
        # a = request.form['amount']
        with open('temp.txt', 'r') as file:
            content = file.read().splitlines()
        if len(content) == 6:
            f, t, name, k, i, a = content
        f=int(f)
        t=int(t)
        a=float(a)

        eP =request.form['empPIN']
        

        if eI in emp["empid"].values and emp['pin'][findIndex(emp,'empid',eI)]==eP:
            # for x in range(len(emp['empid'])):
            #     if emp['empid'][x]==eI:
            #         ind=x
            if emp['pin'][findIndex(emp,'empid',eI)]==eP:
                if checkFBalance(a, df, f):
                    if AccountValidity(t,df):
                        if len(df['account_status'][findIndex(df,"account_number",f)])==14 and len(df['account_status'][findIndex(df,"account_number",t)])==14:
                            fInd = findIndex(passBook, "account_number", f)
                            tInd = findIndex(passBook, "account_number", t)
                            fL = GETpassbk(fInd, passBook)
                            tL = GETpassbk(tInd, passBook)
                            fL.append(-float(a))
                            tL.append(float(a))

                            mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")
                            cursor=mycon.cursor()
                            query = "UPDATE passbook SET passbk = %s WHERE account_number = %s"
                            cursor.execute(query, (str(fL), f))
                            cursor.execute(query, (str(tL), t))

                            df["balance"][fInd]-=float(a)
                            df["balance"][tInd]+=float(a)
                            query1 = "UPDATE accountDetails SET balance = %s WHERE account_number = %s"
                            cursor.execute(query1, (df["balance"][fInd], f))
                            cursor.execute(query1, (df["balance"][tInd], t))

                            mycon.commit()
                            cursor.close()
                            mycon.close()


                            return render_template("chequeBookVerifyTaransact.html", FaccNo='{}'.format(f),
                                                   TaccNo='{}'.format(t),
                                                   Name='{}'.format(name), chkKey='{}'.format(k), Amount='{}'.format(a), EmpID='{}'.format(eI), EmpPIN='{}'.format(eP),IFSC='{}'.format(i))

                        else:
                            f1 = open("debug.txt", 'w')
                            f1.write(reason(df['account_status'][findIndex(df,"account_number",f)])+'\n'+reason(df['account_status'][findIndex(df,"account_number",f)]))
                            f1.close()
                            if len(df['account_status'][findIndex(df, "account_number", f)])>14 and len(df['account_status'][findIndex(df, "account_number", t)])>14:
                                print("1")
                                mainblk="Both Accounts"
                                blockedAccount1=f
                                rsn1=reason(df['account_status'][findIndex(df, "account_number", f)])
                                blockedAccount2=t
                                rsn2=reason(df['account_status'][findIndex(df, "account_number", t)])


                            elif len(df['account_status'][findIndex(df, "account_number", t)])>14:
                                print("2")
                                blockedAccount1,mainblk=f,str(f)+" Account "
                                rsn1=reason(df['account_status'][findIndex(df, "account_number", f)])
                                blockedAccount2=""
                                rsn2=""
                            elif len(df['account_status'][findIndex(df, "account_number", f)])>14:

                                print("3")

                                blockedAccount1,mainblk=f,str(f)+" Account "
                                rsn1=reason(df['account_status'][findIndex(df, "account_number", f)])
                                blockedAccount2=""
                                rsn2=""
                            return render_template("chequeBookClearanceAccountBlocked.html", mainBlk='{}'.format(mainblk), blkAcc1='{}'.format(blockedAccount1),
                                       blkAcc2='{}'.format(blockedAccount2), Reason1='{}'.format(rsn1), Reason2='{}'.format(rsn2))


                else:
                    f1 = open("debug.txt", 'w')
                    f1.write("Not Enough Balance")
                    f1.close()
                    return render_template("chequeBookClearanceNoBalance.html", acc='{}'.format(f),
                                           bal='{}'.format(df['balance'][findIndex(passBook, "account_number", f)]),
                                           transfer='{}'.format(a))

        else:
            f1 = open("debug.txt", 'w')
            f1.write("emp id prob")
            f1.close()
            return render_template("chequeBookClearanceEMPcredFailed.html")



if __name__ == '__main__':
    app.run(debug=True)