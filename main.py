import os
import smtplib
from email.message import EmailMessage

from flask import Flask, request, jsonify, render_template, url_for, redirect
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
import random
from processing import *
from datetime import datetime
import pandas as pd
import mysql.connector as sqltor

mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")

df=pd.read_sql("select * from accountDetails;",mycon)
dfa=df.copy()

emp=pd.read_sql("select * from emp;",mycon)
passBook=pd.read_sql("select * from passbook;",mycon)
dat = pd.read_sql(f"select * from stat_acc;", mycon)
date=dat.copy()
mycon.close()


@app.route('/')
def l():
    return render_template('login.html',stat='clear')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    empID=request.form['username']
    empPass=request.form['password']
    if empID in emp['empid'].values:
        if emp['pin'][findIndex(emp, 'empid', empID)] == empPass:
            ind = findIndex(emp, 'empid', empID)
            with open('empID.txt', 'w') as file:
                file.write(f"{empID}")
            file.close()
            with open('eind.txt', 'w') as file:
                file.write(f"{ind}")
            file.close()
            balance=(sum(list(df['balance'].values)))
            cust=(len(list(df['balance'].values)))
            return render_template('index.html', Lmail='{}'.format(empID),balance='{}'.format(balance),lenC='{}'.format(cust))
        else:
            error = 'Invalid Credentials. Please try again.'
    else:
        error = 'Invalid Credentials. Account Not Found.'
    return render_template('login.html', error=error)


@app.route("/client")
def lgoinC():
    return render_template("loginc.html",stat="clear")

@app.route('/client', methods=['GET', 'POST'])
def loginClient():
    error = None
    mail=request.form['username']
    Lmail=mail
    key=request.form['password']
    if mail in df['email'].values:

        if df['security_code'][findIndex(df,'email',mail)]==key:
            ind=findIndex(df,'email',mail)
            with open('Lmail.txt', 'w') as file:
                file.write(f"{Lmail}")
            file.close()
            with open('ind.txt', 'w') as file:
                file.write(f"{ind}")
            file.close()
            data = zip((list(map(float, passBook['passbk'][findIndex(passBook, 'account_number', df['account_number'][findIndex(df, 'email', mail)])][1:-1].split(", "))))[::-1], (list(map(lambda x: x.strftime("%d-%m-%Y"), (list(map(lambda x: (datetime.strptime(x, "%Y-%m-%d")), (list(map(lambda x: x[1:-1], passBook['date'][findIndex(passBook,'account_number', df['account_number'][findIndex(df,'email', mail)])][1:-1].split(", "))))))))))[::-1])
            return render_template('indexc.html',Lmail='{}'.format(mail),Pbk=passBook,Db=df,IND=ind,dataS=data)

        else:
            error = 'Invalid Credentials. Please try again.'
    else:
        error = 'Invalid Credentials. Account Not Found.'
    return render_template('loginc.html', error=error)

@app.route("/homec")
def clienthome():
    with open('Lmail.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        Lmail= str(content[0])
    with open('ind.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        ind= int(content[0])
    ind = findIndex(df, 'email', Lmail)
    data = zip((list(map(float, passBook['passbk'][findIndex(passBook, 'account_number',
                                                             df['account_number'][findIndex(df, 'email', Lmail)])][
                                1:-1].split(", "))))[::-1], (list(map(lambda x: x.strftime("%d-%m-%Y"), (list(
        map(lambda x: (datetime.strptime(x, "%Y-%m-%d")), (list(map(lambda x: x[1:-1], passBook['date'][
                                                                                           findIndex(passBook,
                                                                                                     'account_number',
                                                                                                     df[
                                                                                                         'account_number'][
                                                                                                         findIndex(df,
                                                                                                                   'email',
                                                                                                                   Lmail)])][
                                                                                       1:-1].split(", "))))))))))[::-1])
    return render_template("indexc.html",Lmail=Lmail,Pbk=passBook,Db=df,IND=ind,dataS=data)

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/chequeBookClearance")
def chkBkClrFrm():
    return render_template("chequeBookClearance.html")
def calculate_age(birthdate):
    today = datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

app.jinja_env.filters['calculate_age'] = calculate_age
@app.route("/search")
def search():
    return render_template("change.html")

@app.route("/search",methods=['POST'])
def searchP():
    s=int(request.form['sel'])
    l =["q1","q2","q3",'q4','q5','q6','q7','q8','q9','q10','q11']

    if s==6:
        return redirect(url_for(l[int(s)]))
    return redirect(url_for(l[int(s)], order='desc'))



@app.route("/query1/<order>")
def q1(order):
    if order=="desc":
        return render_template("q1.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type']].sort_values(by='balance',ascending=False),orderS=order)
    if order=="asc":
        print(order)
        return render_template("q1.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type']].sort_values(by='balance',ascending=True),orderS=order)

@app.route("/query2/<order>")
def q2(order):
    if order=="desc":
        return render_template("q2.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type']].sort_values(by='balance',ascending=False),orderS=order)
    if order=="asc":
        return render_template("q2.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type']].sort_values(by='balance',ascending=True),orderS=order)

@app.route("/query3/<order>")
def q3(order):
    if order=="desc":
        return render_template("q3.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type']].sort_values(by='balance',ascending=False),orderS=order)
    if order=="asc":
        return render_template("q3.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type']].sort_values(by='balance',ascending=True),orderS=order)

@app.route("/query4/<order>")
def q4(order):
    if order=="desc":
        return render_template("q4.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type']].sort_values(by='account_holder',ascending=False),orderS=order)
    if order=="asc":
        return render_template("q4.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type']].sort_values(by='account_holder',ascending=True),orderS=order)

@app.route("/query5/<order>")
def q5(order):
    if order=="desc":
        return render_template("q5.html",Sdf=df[["account_number","account_holder","contact_number",'balance','date_column','account_type']].sort_values(by='date_column',ascending=False),orderS=order)
        return render_template("q5.html",Sdf=df[["account_number","account_holder","contact_number",'balance','date_column','account_type']].sort_values(by='date_column',ascending=False),orderS=order)
    if order=="asc":
        return render_template("q5.html",Sdf=df[["account_number","account_holder","contact_number",'balance','date_column','account_type']].sort_values(by='date_column',ascending=True),orderS=order)

@app.route("/query6/<order>")
def q6(order):
    if order=="desc":

        return render_template("q6.html",Sdf=df[["account_number","account_holder","contact_number",'balance','dob','account_type']].sort_values(by='dob',ascending=False,key=lambda x: df['dob'].apply(calculate_age)),orderS=order)
    if order=="asc":
        return render_template("q6.html",Sdf=df[["account_number","account_holder","contact_number",'balance','dob','account_type']].sort_values(by='dob',ascending=True,key=lambda x: df['dob'].apply(calculate_age)),orderS=order)

@app.route("/query7")
def q7():
    return render_template("q7.html",checkS="form")

@app.route("/query7",methods=['POST'])
def q7P():
    a=int(request.form['con'])
    a1=int(request.form['con1'])
    if a==a1 and (a in df['account_number'].values):
        t=df[["account_number","account_holder","contact_number",'address','balance','dob','account_type','account_status','date_column']].iloc[findIndex(df,'account_number',a)]
        rsn = ""
        if len(t['account_status'])>14:
            rsn=reason(t['account_status'])
        return render_template('q7.html', checkS="res", Sdf=t,rsn=rsn)


    elif not(a in (df['account_number'].values)):
        print("Here")
        return render_template('q7.html',checkS="form",checkS1='notThere')
    if a!=a1:
        return render_template('q7.html',checkS="form",checkS1='change_error')

@app.route("/query8")
def q8():
    return render_template("q8.html", checkS="form")

@app.route("/query8", methods=['POST'])
def q8P():
    a = (request.form['con'])
    a1 = (request.form['con1'])
    if a == a1 and (a in df['contact_number'].values):
        t = df[["account_number", "account_holder", "contact_number", 'address', 'balance', 'dob', 'account_type',
                'account_status', 'date_column']].iloc[findIndex(df, 'contact_number', a)]
        rsn = ""
        if len(t['account_status']) > 14:
            rsn = reason(t['account_status'])
        return render_template('q8.html', checkS="res", Sdf=t, rsn=rsn)


    elif not (a in (df['contact_number'].values)):
        return render_template('q8.html', checkS="form", checkS1='notThere')
    if a != a1:
        return render_template('q8.html', checkS="form", checkS1='change_error')

@app.route("/query9")
def q9():
    return render_template("q9.html", checkS="form")


@app.route("/query9", methods=['POST'])
def q9P():
    a = (request.form['con'])
    a1 = (request.form['con1'])
    if a == a1 and (a in df['UID'].values):
        t = df[["account_number", "account_holder", "contact_number", 'address', 'balance', 'dob', 'account_type',
                'account_status', 'date_column']].iloc[findIndex(df, 'UID', a)]
        rsn = ""
        if len(t['account_status']) > 14:
            rsn = reason(t['account_status'])
        return render_template('q9.html', checkS="res", Sdf=t, rsn=rsn)


    elif not (a in (df['UID'].values)):
        return render_template('q9.html', checkS="form", checkS1='notThere')
    if a != a1:
        return render_template('q9.html', checkS="form", checkS1='change_error')

@app.route("/query11")
def q11():
    return render_template("q11.html", checkS="form")


@app.route("/query11", methods=['POST'])
def q11P():
    a = (request.form['con'])
    a1 = (request.form['con1'])
    if a.upper() == a1.upper() and (a.upper() in list(map(lambda x: x.upper(),list(df['account_holder'].values)))):
        t = df[["account_number", "account_holder", "contact_number", 'address', 'balance', 'dob', 'account_type',
                'account_status', 'date_column']].iloc[findNameIndex(df, a)]
        rsn = ""
        if len(t['account_status']) > 14:
            rsn = reason(t['account_status'])
        return render_template('q11.html', checkS="res", Sdf=t, rsn=rsn)


    elif not (a.upper() in list(map(lambda x: x.upper(),list(df['account_holder'].values)))):
        return render_template('q11.html', checkS="form", checkS1='notThere')
    elif (a.upper() != a1.upper()):
        return render_template('q11.html', checkS="form", checkS1='change_error')

@app.route("/query10/<order>")
def q10(order):
    if order=="desc":
        return render_template("q10.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type','account_status']].sort_values(by='balance',ascending=False),orderS=order)
    if order=="asc":
        return render_template("q10.html",Sdf=df[["account_number","account_holder","contact_number",'balance','account_type','account_status']].sort_values(by='balance',ascending=True),orderS=order)


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




        elif (AccountValidity(f,df)) and (AccountValidity(t,df)):
            file1 = open("debug.txt", "w")
            file1.write("Verified both accounts")
            file.close()

            for x in range(len(df["account_number"])):
                if int(df['account_number'][x]) == int(f):
                    ind = x

            # ind=findIndex(df, "account_number", df)

            keys=keysExtractions(df["keys_array"][ind])

            path="static/signatures/"
            if (k in keys) and (i==df["ifsc_code"][ind]):
                chk=1
                file1 = open("debug.txt", "w")
                file1.write("Signature")
                file.close()

                path+=df['signature'][ind]

                # SQL PART
                # mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
                # df1=pd.read_sql(f"select signature from accountDetails where account_number = {int(f)};", mycon)
                # mycon.close()
                # path+=df1["signature"][0]


                return render_template("chequeBookVerify.html", FaccNo='{}'.format(f), TaccNo='{}'.format(t),
                                       Name='{}'.format(name), chkKey='{}'.format(k), Amount='{}'.format(a),
                                       img_path='{}'.format(path),IFSC='{}'.format(i))


            elif not(k in keys):

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
                        print(len(df['account_status'][findIndex(df, "account_number", f)]),
                              (df['account_status'][findIndex(df, "account_number", f)]))
                        print()
                        print(print(len(df['account_status'][findIndex(df, "account_number", t)]),
                                  (df['account_status'][findIndex(df, "account_number", t)])))
                        print()
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

                            l = keysExtractions(df['keys_array'][findIndex(df, "account_number", f)])
                            l.remove(k)
                            print(l)
                            df['keys_array'][findIndex(df, "account_number", f)] = str(l)
                            query2 = "UPDATE accountDetails SET keys_array = %s WHERE account_number = %s"
                            cursor.execute(query2, (str(l), f))


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
                            print(len(df['account_status'][findIndex(df, "account_number", f)]),
                                  (df['account_status'][findIndex(df, "account_number", f)]))
                            if len(df['account_status'][findIndex(df, "account_number", f)])>14 and len(df['account_status'][findIndex(df, "account_number", t)])>14:

                                mainblk="Both Accounts"
                                blockedAccount1=f
                                rsn1=reason(df['account_status'][findIndex(df, "account_number", f)])
                                blockedAccount2=t
                                rsn2=reason(df['account_status'][findIndex(df, "account_number", t)])


                            elif len(df['account_status'][findIndex(df, "account_number", t)])>14:
                                blockedAccount1,mainblk=t,str(t)+" Account "
                                rsn1=reason(df['account_status'][findIndex(df, "account_number", t)])
                                blockedAccount2=""
                                rsn2=""


                            elif len(df['account_status'][findIndex(df, "account_number", f)])>14:
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


@app.route('/fundtransfer/<ft_val>')
def fundt(ft_val):

    return render_template('fundtransfer.html', ft_val = ft_val)


@app.route('/fundtransfer_func', methods=["POST"] )
def fundt_fun():
    def findIndex(emp, column, empID):
        ind1=0
        for x in range(len(emp[column])):
            if empID == emp[column][x]:
                ind1 = x
        return ind1

    df1 = df
    df2 = emp
    df3 = passBook

    li1 = {x: y for x, y in zip(df1["account_number"], df1["balance"])}  # This is a Dictionary
    li2 = [list(df2.iloc[i]) for i in range(len(df2))]
    li_req = [int(request.form["Acc_from"]), int(request.form["Acc_to"]), request.form["Emp_id"], request.form["Emp_pin"]]
    print(li_req)
    accFrom_valid = li_req[0] in li1.keys()
    accTo_valid = li_req[1] in li1.keys()
    emp_valid = [li_req[2], li_req[3]] in li2
    senderBlk = len(df['account_status'][findIndex(df,'account_number',li_req[0])])==14
    receiverBlk = len(df['account_status'][findIndex(df, 'account_number', li_req[1])])==14

    if accFrom_valid and accTo_valid and emp_valid and senderBlk and receiverBlk:
        Amount = float(request.form["Amt"])
        if Amount > li1[li_req[0]]:
            return redirect(url_for('fundt', ft_val="fundtransfer_insuffFund"))
        else:
            li1[li_req[0]] = li1[li_req[0]]-Amount
            mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
            cursor = mycon.cursor()
            li1[li_req[1]] = li1[li_req[1]]+Amount
            cursor.execute("update accountdetails set balance=%s where account_number=%s ;", [li1[li_req[0]], li_req[0]])
            cursor.execute("update accountdetails set balance=%s where account_number=%s ;", [li1[li_req[1]], li_req[1]])
            passbok = {x:y for x,y in zip(df3["account_number"],df3["passbk"])}
            # correction for updating into table passbook from [10000.0, 10000.0, -3000.0, 0.9, 2000.0, -1000.0, -1000.0, -1000.0],-100.0 to [10000.0, 10000.0, -3000.0, 0.9, 2000.0, -1000.0, -1000.0, -1000.0, -100.0]
            passbok[(li_req[0])] = str(list(map(float, passbok[(li_req[0])][1:-1].split(", "))) + [-Amount])
            passbok[(li_req[1])] = str(list(map(float, passbok[(li_req[1])][1:-1].split(", "))) + [Amount])
            cursor.execute("update passbook set passbk=%s where account_number=%s ;",[f"{passbok[li_req[0]]}", li_req[0]])
            cursor.execute("update passbook set passbk=%s where account_number=%s ;",[f"{passbok[li_req[1]]}", li_req[1]])
            mycon.commit()
            mycon.close()
            return redirect(url_for('fundt', ft_val="fundt_success"))
    elif not accFrom_valid:
        return redirect(url_for('fundt', ft_val="fundt_accfInvalid"))
    elif not accTo_valid:
        return redirect(url_for('fundt', ft_val="fundt_acctInvalid"))
    elif not emp_valid:
        return redirect(url_for('fundt', ft_val="fundt_empInvalid"))
    elif not senderBlk:
        return redirect(url_for('fundt', ft_val="fundt_senderBlocked"))
    elif not receiverBlk:
        return redirect(url_for('fundt', ft_val="fundt_receiverBlocked"))


@app.route("/accblock")
def accblock1():
    return render_template("form-element.html")


@app.route("/accblock", methods=["POST"])
def accblock():
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
    dfa = pd.read_sql("select * from accountDetails;", mycon)
    date = pd.read_sql(f"select * from stat_acc;", mycon)
    mycon.close()
    # f = open("output.txt", "w")
    a = request.form["accnum"]
    b = request.form["empid"]
    c = request.form["emppin"]
    d = request.form["reason"]
    e = request.form["date"]

    value = False
    t1 = False
    print(type(int(a)),a ,type((dfa['account_number'].values)[0]))
    if int(a) in dfa["account_number"].values:
        value = True
        if len(dfa["account_status"][findIndex(dfa, "account_number", int(a))]) == 14:
            if str(b) in emp["empid"].values and int(emp["pin"][findIndex(emp, "empid", b)]) == int(c):
                if len(date["date"][findIndex(date, "account_number", int(a))]) == 11:
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
                    return redirect(url_for("accsucblock"))
                    # {"Blocked": 0}
            else:
                return render_template("employeenotfound.html")
        else:
            return render_template("accountalreadyblocked.html", reasonS="{}".format(reason(dfa["account_status"][findIndex(dfa, "account_number", a)])))
    else:
        return render_template("accountnotfound.html")
    # f.write(str(value))
    # f.write(str(t1))
    # return redirect(url_for("accsucblock"))

@app.route("/accsucblock")
def accsucblock():
    return render_template("success.html")

@app.route("/accunblock")
def accunblock1():
    return render_template("unblockform.html")


@app.route("/accunblock", methods=["POST"])
def accunblock():
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
    dat = pd.read_sql(f"select * from stat_acc;", mycon)
    dfa = pd.read_sql("select * from accountDetails;", mycon)
    mycon.close()
    # f = open("output.txt", "w")
    a = request.form["accnum"]
    b = request.form["empid"]
    c = request.form["emppin"]


    value = False
    t1 = False
    print(type(int(a)),a,type((dfa['account_number'].values)[0]))
    print(int(a) in list(map(int,list(dfa["account_number"].values))))
    if int(a) in list(map(int,list(dfa["account_number"].values))):
        value = True
        if str(dfa["account_status"][findIndex(dfa, "account_number", int(a))]) != r"{'Blocked': 0}":
            if str(b) in emp["empid"].values and int(emp["pin"][findIndex(emp, "empid", b)]) == int(c):
                if len(dat["date"][findIndex(dat, "account_number", int(a))]) != 11:
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
                    return render_template('unblocksuccess.html')

            else:
                return render_template("employeenotfound1.html")
        else:
            return render_template("accountalreadyunblocked.html")
    else:
        return render_template("accountnotfound1.html")
    # return render_template('unblocksuccess.html')




@app.route("/change")
def change():
    return render_template("change1.html")

@app.route("/change", methods=["POST"])
def change1():
    global accno
    accno = int(request.form["Acc"])
    with open('temp.txt', 'w') as file:
        file.write(f"{accno}")
    empid = request.form["empid"]
    pin = request.form["empd"]
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
    cur = mycon.cursor()
    cur.execute("select account_number from accountdetails")
    lacc = cur.fetchall()
    cur.execute("select empid, pin from emp")
    lemp = cur.fetchall()
    mycon.commit()
    cur.close()
    mycon.close()
    if (accno,) in lacc and (empid, pin) in lemp:
        l = ["cno", "em", "add", "acchol", "acctyp", "accblock1"]
        return redirect(url_for(l[int(request.form["sel"])]))
    else:
        return redirect(url_for("status", check="InvalidCredentials"))


@app.route("/cno")
def cno():
    return render_template("Contact_number.html")


@app.route("/cno", methods=["POST"])
def contact():
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno = int(accno[0])
    con = int(request.form["con"])
    con1 = int(request.form["con1"])
    if con == con1:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set contact_number={0} where account_number={1}".format(con, accno))
        mycon.commit()
        cur.close()
        mycon.close()

        return redirect(url_for("status", check='success'))
    else:
        return redirect(url_for("Statuscno", check='change_error'))

@app.route("/statusCn/<check>")
def Statuscno(check):
    return render_template("Contact_number.html", check=check)

@app.route("/em")
def em():
    return render_template("email.html")

@app.route("/em", methods=["POST"])
def email():
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno = int(accno[0])
    print(accno)
    email = request.form["email"]
    email1 = request.form["email1"]
    if email == email1:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set email=%s where account_number=%s", (email, accno))
        mycon.commit()
        cur.close()
        mycon.close()
        print("done")
        return redirect(url_for("status", check='success1'))
    else:
        return redirect(url_for("StatusEm", check='change_error'))

@app.route("/statusEm/<check>")
def StatusEm(check):
    return render_template("email.html", check=check)

@app.route("/add")
def add():
    return render_template("address.html")


@app.route("/add", methods=["POST"])
def address():
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno = int(accno[0])
    adr = request.form["adr"]
    if adr != "":
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set address=%s where account_number=%s", (adr, accno))
        mycon.commit()
        cur.close()
        mycon.close()
        return redirect(url_for("status", check='success2'))
    else:
        return redirect(url_for("StatusAdr", check='change_error'))


@app.route("/statusAdr/<check>")
def StatusAdr(check):
    return render_template("address.html", check=check)

@app.route("/acchol")
def acchol():
    return render_template("Account_Holder.html")

@app.route("/accounthol", methods=["POST"])
def accounthol():
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno = int(accno[0])
    ach = request.form["ach"]
    ach1 = request.form["ach1"]
    if ach == ach1:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set account_holder=%s where account_number=%s", (ach, accno))
        mycon.commit()
        cur.close()
        mycon.close()
        return redirect(url_for("status", check='success3'))
    else:
        return redirect(url_for("StatusHol", check='change_error'))


@app.route("/statusHol/<check>")
def StatusHol(check):
    return render_template("Account_Holder.html", check=check)


@app.route("/acctyp")
def acctyp():
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
    cur = mycon.cursor()
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno = int(accno[0])
    cur.execute("select account_type from accountdetails where account_number=%s", [accno])
    lacc = cur.fetchall()
    print(lacc)
    if ("Current",) in lacc:
        cur.execute("update accountdetails set account_type='Savings' where account_number=%s", [accno])
        mycon.commit()
        cur.close()
        mycon.close()
        return redirect(url_for("status", check='success4'))
    else:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set account_type='Current' where account_number=%s", [accno])
        mycon.commit()
        cur.close()
        mycon.close()
        return redirect(url_for("status", check='success5'))

@app.route("/status/<check>")
def status(check):
    return render_template("change1.html",check=check)

@app.route("/chequeBookOrdering/<check>")
def cheque(check):
    return render_template("cheque.html", check=check)

@app.route("/balanceenq/<check>")
def balenq(check):
    return render_template("balanceenq.html", check=check)

@app.route("/passbook/<check>")
def passbook(check):
    return render_template("passbook.html", check=check)

@app.route("/passbook/<check>", methods=["POST"])
def passbook2(check):
    otp = request.form["otp"]
    with open('d.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        d = content[0]
    file.close()
    with open('t.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        t = content[0]
    file.close()

    if int(d )== int(otp):
        check = "success"
        data=zip((list(map(float,passBook['passbk'][findIndex(passBook,'account_number',df['account_number'][findIndex(df,'email',t)])][1:-1].split(", "))))[::-1],(list(map(lambda x: x.strftime("%d-%m-%Y"),(list(map(lambda x : (datetime.strptime(x, "%Y-%m-%d")),(list(map(lambda x: x[1:-1],passBook['date'][findIndex(passBook,'account_number',df['account_number'][findIndex(df,'email',t)])][1:-1].split(", "))))))))))[::-1])
        return render_template("passbook.html", check=check, Sdf=passBook,St=t,dataS=data)
    else:
        return render_template("passbook.html", check="failed")

@app.route("/chequeBookOrdering/<check>", methods=["POST"])
def cheque2(check):
    if check=="placeOrder":
        s = request.form['accname']
        from email.message import EmailMessage
        import ssl
        import smtplib

        email_sender = "drdev.maill@gmail.com"
        email_password = "mmieeonadmnrylqz"
        email_receiver = ['adrushtshetty@gmail.com']
        subject = "Cheque Book Ordering"
        body = """
            Dear Admin,
            A cheque Book of {s} size was request for the account {d}
            Sincerely,

                ShettyShrinivasDawoodKokrady Co-Operative Bank of India

            """.format(d=df['account_number'][findIndex(df,'email',t)],s=s)
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        return render_template("cheque.html", check="done")
    else:
        otp = request.form["otp"]
        print(t, otp)
        if d==int(otp):
            balance = dfa["balance"][findIndex(dfa, 'email', t)]
            check = "success"
            return render_template("cheque.html", check=check, balances=balance)
        else:
            return render_template("cheque.html", check="failed")

@app.route("/chequeBookOrdering", methods=["POST"])
def cheque1():
    a = int(request.form["accname"])
    b = request.form["email"]
    if a in list(dfa["account_number"].values):
        print(a, type(a), dfa["account_holder"][0], type(dfa["account_holder"][0]))
        if b == dfa["email"][findIndex(dfa, "email", a)]:
            global t
            t = b
            with open('t.txt', 'w') as file:
                file.write(str(t))
            file.close()

            global d
            d = random.randint(100000, 999999)
            with open('d.txt', 'w') as file:
                file.write(str(d))
            file.close()

            from email.message import EmailMessage
            import ssl
            import smtplib

            email_sender = "drdev.maill@gmail.com"
            email_password = "mmieeonadmnrylqz"
            email_receiver = [f"{b}"]
            subject = "balance enquiry"
            body = """
                Dear Customer,

                Your OTP for balance enquiry is {d}

                Sincerely,

                    ShettyShrinivasDawoodKokrady Co-Operative Bank of India

                """.format(d=d)
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            return redirect(url_for('cheque', check="otp"))


        else:
            return redirect(url_for('cheque', check="noemail"))
    else:
        return redirect(url_for('cheque', check="noacc"))


@app.route("/passbook", methods=["POST"])
def passbook1():
    a = request.form["accname"]
    b = request.form["email"]
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
    dfa = pd.read_sql(f"select * from accountdetails;", mycon)
    if int(a) in list(dfa["account_number"].values):
        print(a, type(a), dfa["email"][findIndex(dfa, "account_number", a)],b ,b==dfa["email"][findIndex(dfa, "account_number", a)],type(dfa["account_holder"][0]))
        if b == dfa["email"][findIndex(dfa, "account_number", a)]:
            global t
            t = b

            with open('t.txt', 'w') as file:
                file.write(str(t))
            file.close()
            global d
            d = random.randint(100000, 999999)
            with open('d.txt', 'w') as file:
                file.write(str(d))
            file.close()

            from email.message import EmailMessage
            import ssl
            import smtplib

            email_sender = "drdev.maill@gmail.com"
            email_password = "mmieeonadmnrylqz"
            email_receiver = [f"{b}"]
            subject = "balance enquiry"
            body = """
                Dear Customer,

                Your OTP for balance enquiry is {d}

                Sincerely,

                    ShettyShrinivasDawoodKokrady Co-Operative Bank of India

                """.format(d=d)
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
            return redirect(url_for('passbook', check="otp"))

        else:
            return redirect(url_for('passbook', check="noemail"))
    else:
        return redirect(url_for('passbook', check="noacc"))

@app.route("/balanceenq/<check>", methods=["POST"])
def balenq2(check):
    otp = request.form["otp"]
    print(t, otp)
    if d==int(otp):
        balance = dfa["balance"][findIndex(dfa, 'email', t)]
        check = "success"
        return render_template("balanceenq.html", check=check, balances=balance)
    else:
        return render_template("balanceenq.html", check="failed")


@app.route("/balenceenq", methods=["POST"])
def balenq1():
    a = request.form["accname"]
    b = request.form["email"]
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
    dfa = pd.read_sql(f"select * from accountdetails;", mycon)
    if a in list(dfa["account_holder"].values):
        print(a, type(a), dfa["account_holder"][0], type(dfa["account_holder"][0]))
        if b == dfa["email"][findIndex(dfa, "email", a)]:
            global t
            t = b
            global d
            d = random.randint(100000, 999999)
            from email.message import EmailMessage
            import ssl
            import smtplib

            email_sender = "drdev.maill@gmail.com"
            email_password = "mmieeonadmnrylqz"
            email_receiver = [f"{b}"]
            subject = "balance enquiry"
            body = """
                Dear Customer,

                Your OTP for balance enquiry is {d}

                Sincerely,

                    ShettyShrinivasDawoodKokrady Co-Operative Bank of India

                """.format(d=d)
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            return redirect(url_for('balenq', check="otp"))


        else:
            return redirect(url_for('balenq', check="noemail"))
    else:
        return redirect(url_for('balenq', check="noacc"))


@app.route("/loanapp")
def loanapp():
    return render_template("loanapplication.html")


@app.route("/loanapp", methods=["POST"])
def loanapp1():
    a = request.form["name"]
    b = request.form["email"]
    c = request.form["address"]
    d = request.form["accnum"]
    e = request.form["occ"]
    f = request.form["uid"]
    g = request.form["amount"]
    h = request.form["salary"]
    if d in dfa["account_number"].values:
        if a in dfa["account_holder"].values:
            if b in dfa["email"].values:
                if f in dfa["UID"].values:
                    from email.message import EmailMessage
                    import ssl
                    import smtplib

                    name = request.form['name']
                    subject = request.form['subject']
                    message = request.form['message']
                    mail = request.form['email']

                    email_sender = "drdev.maill@gmail.com"
                    email_password = "mmieeonadmnrylqz"
                    email_receiver = ["adrushtshetty@gmail.com"]
                    body = """
                            New Personal Loan Application,

                            Details:

                            Account Number: {number}
                            Name: {name}
                            Email Address: {email}
                            Address: {address}
                            Occupation: {occupation}
                            Government UID: {uid}
                            Amount Required: {amount}
                            salary: {salary}


                            """.format(number=d, name=a, address=c, email=b, occupation=e, amount=g, salary=h, uid=f)
                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em['subject'] = subject
                    em.set_content(body)
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return render_template("loanapplication.html")


@app.route("/card_edit/<check>")
def cardedit(check):
    return render_template("card_edit.html", check=check)


@app.route("/card_edit_func2", methods=["POST"])
def cardeditfunc2():
    tem = open("temp2.txt")
    dis = tem.read().split()
    tem.close()
    print(dis[4])
    print(request.form["acc_otp"])
    if dis[4] == request.form["acc_otp"]:
        return redirect(url_for("cardedit3", check3="acc_next"))
    else:
        return redirect(url_for("cardedit2", check2="wrong_otp"))



@app.route("/card_edit_func", methods=["POST"])
def cardeditfunc():
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")

    df1 = pd.read_sql("select * from debit_card_details", mycon)
    df2 = pd.read_sql("select * from accountdetails", mycon)

    di1 = {x: y for x, y in zip(df1["account_number"], df1["debit_card_number"])}
    di2 = {x: [y, z] for x, y, z in zip(df2["account_number"], df2["email"], df2["contact_number"])}
    di3 = {x: y for x, y in zip(df1["debit_card_number"], df1["pin"])}
    di4 = {x: y for x, y in zip(df1["account_number"], df1["status"])}

    li_acc = list(df1["account_number"])
    mycon.close()

    if int(request.form["account"]) not in li_acc:
        return redirect(url_for("cardedit", check="invalid_acc"))

    if di1[int(request.form["account"])] == int(request.form["card_num"]):
        if di2[int(request.form["account"])] == [request.form["acc_email"], request.form["acc_contact"]]:
            if di3[int(request.form["card_num"])] == int(request.form["acc_pin"]):
                tem = open("temp.txt", "w")
                tem.write(request.form["account"])
                tem.close()
                from random import randint
                otp = randint(100000, 999999)
                from email.message import EmailMessage
                import ssl
                import smtplib

                email_sender = "drdev.maill@gmail.com"
                email_password = "mmieeonadmnrylqz"
                email_receiver = ['adnaandawood101@gmail.com']
                subject = "Debit Card Editing"
                body = """
Dear Customer,

Your OTP for Debit Card Editing is {d}
Please Do Not Share it with Others.

Sincerely,

    ShettyShrinivasDawoodKokrady Co-Operative Bank of India

                """.format(d=otp)
                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['subject'] = subject
                em.set_content(body)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
                tem = open("temp2.txt", "w")
                tem.write(' '.join([request.form["card_num"], request.form["account"], request.form["acc_email"],
                                    request.form["acc_contact"], str(otp), di4[int(request.form["account"])]]))
                tem.close()
                return redirect(url_for("cardedit2", check2="acc_next"))
            else:
                return redirect(url_for("cardedit", check="invalid_pin"))
        else:
            return redirect(url_for("cardedit", check="invalid_email"))
    else:
        return redirect(url_for("cardedit", check="acc_wrong"))


@app.route("/card_edit2/<check2>")
def cardedit2(check2):
    tem = open("temp2.txt")
    dis = tem.read().split()
    tem.close()

    return render_template("card_edit2.html", check2=check2, dis=dis)

@app.route("/card_edit3/<check3>")
def cardedit3(check3):
    tem = open("temp2.txt")
    dis = tem.read().split()
    tem.close()

    if (dis[5] == "Enabled" and check3 == "acc_next") or check3 == "debi_enable":
        return render_template("card_edit31.html", check31=check3)
    elif check3 == "debi_disable":
        return render_template("card_edit32.html", check32=check3)
    else:
        return render_template("card_edit32.html", check32=check3)


@app.route("/card_edit_func3", methods=["POST"])
def cardeditfunc3():
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
    tem = open("temp.txt")
    acc_no = int(tem.read())
    tem.close()
    cursor = mycon.cursor()

    try:
        if request.form["chek"] == 'T':
            cursor.execute("update debit_card_details set status = 'Disabled' where account_number=%s;", [acc_no])
            mycon.commit()

    except:
        try:
            if request.form["chg_pin"] == request.form["chg_confpin"]:
                cursor.execute("update debit_card_details set pin = %s where account_number=%s;",
                               [request.form["chg_pin"], acc_no])
                mycon.commit()

            else:
                return redirect(url_for("cardedit3", check31="notmatching"))
        except:
            pass
        try:
            if request.form["acc_type_online"] == "online":
                cursor.execute("update debit_card_details set online_transaction = 'Yes' where account_number=%s;",
                               [acc_no])
                mycon.commit()
        except:
            cursor.execute("update debit_card_details set online_transaction = 'No' where account_number=%s;", [acc_no])
            mycon.commit()

        try:
            if request.form["acc_type_international"] == "international":
                cursor.execute(
                    "update debit_card_details set international_transaction = 'Yes' where account_number=%s;",
                    [acc_no])
                mycon.commit()
        except:
            cursor.execute("update debit_card_details set international_transaction = 'No' where account_number=%s;",
                           [acc_no])
            mycon.commit()

        try:
            if int(request.form["chg_limit"]) > 0:
                cursor.execute("update debit_card_details set limit_amount=%s where account_number=%s;",
                               [request.form["chg_limit"], acc_no])
                mycon.commit()
        except:
            pass
        cursor.execute("update debit_card_details set status = 'Enabled' where account_number=%s;", [acc_no])
        mycon.commit()

    return redirect(url_for("cardedit", check="done"))




@app.route('/new_account/<newacc_val>')
def newacc(newacc_val):

    return render_template('new-acc.html', newacc_val= newacc_val)


@app.route('/new_account_func', methods=["POST"])
def newacc_func():
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")

    df1 = pd.read_sql("select * from accountdetails;", mycon)
    df2 = pd.read_sql("select * from emp;", mycon)

    li_acc = list(df1["account_number"])
    li_no = list(df1["contact_number"])
    li_email = list(df1["email"])

    try:
        accnumber = request.form["account"]
        if int(request.form["account"]) in li_acc:
            return redirect(url_for("newacc", newacc_val="newacc_accexist"))
    except:
        from random import randint
        accnumber = randint(100000000, 999999999)
        while accnumber in li_acc :
            accnumber = randint(100000000, 999999999)


    if request.form["contact_number"] in li_no:
        return redirect(url_for("newacc", newacc_val="newacc_numexist"))

    if request.form["email"] in li_email:
        return redirect(url_for("newacc", newacc_val="newacc_emailexist"))



    li1 = [list(df2.iloc[i]) for i in range(len(df2))]
    emp_valid = [request.form["Emp_id"], request.form["Emp_pin"]] in li1
    if not (request.form["security_code"] == request.form["security_code_check"]):
        return redirect((url_for('newacc', newacc_val="newacc_passnotmatch")))

    if emp_valid:
        tu = (accnumber, request.form["contact_number"], request.form["email"], request.form["security_code"], request.form["address"], request.form["name"], 0, request.form["acc_type"], '{"Blocked": 0}', request.form["ifsc"])
        cursor = mycon.cursor()
        cursor.execute("insert into accountdetails (account_number, contact_number, email, security_code, address, account_holder, balance, account_type, account_status, ifsc_code) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", tu)
        cursor.execute("insert into passbook (account_number) values (%s)", [tu[0]])
        mycon.commit()
        cursor.close()
        return redirect(url_for('newacc', newacc_val="newacc_success"))
    else:
        return redirect(url_for('newacc', newacc_val="newacc_empInvalid"))



@app.route('/fundtransferc/<ft_val>')
def fundtc(ft_val):

    return render_template('fundtransferc.html', ft_val = ft_val)


@app.route('/fundtransfer_funcC', methods=["POST"] )
def fundt_funC():
    def findIndex(emp, column, empID):
        ind1=0
        for x in range(len(emp[column])):
            if empID == emp[column][x]:
                ind1 = x
        return ind1

    df1 = df
    df2 = emp
    df3 = passBook

    li1 = {x: y for x, y in zip(df1["account_number"], df1["balance"])}
    li2 = [list(df2.iloc[i]) for i in range(len(df2))]
    li_req = [int(request.form["Acc_from"]), int(request.form["Acc_to"]),  request.form["Emp_pin"]]
    print(li_req)
    accFrom_valid = li_req[0] in li1.keys()
    accTo_valid = li_req[1] in li1.keys()
    emp_valid = df1['security_code'][findIndex(df1,'account_number',li_req[0])]==li_req[2]
    senderBlk = len(df['account_status'][findIndex(df,'account_number',li_req[0])])==14
    receiverBlk = len(df['account_status'][findIndex(df, 'account_number', li_req[1])])==14

    if accFrom_valid and accTo_valid and emp_valid and senderBlk and receiverBlk:
        Amount = float(request.form["Amt"])
        if Amount > li1[li_req[0]]:
            return redirect(url_for('fundt', ft_val="fundtransfer_insuffFund"))
        else:
            li1[li_req[0]] = li1[li_req[0]]-Amount
            mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
            cursor = mycon.cursor()
            li1[li_req[1]] = li1[li_req[1]]+Amount
            cursor.execute("update accountdetails set balance=%s where account_number=%s ;", [li1[li_req[0]], li_req[0]])
            cursor.execute("update accountdetails set balance=%s where account_number=%s ;", [li1[li_req[1]], li_req[1]])
            passbok = {x:y for x,y in zip(df3["account_number"],df3["passbk"])}
            # correction for updating into table passbook from [10000.0, 10000.0, -3000.0, 0.9, 2000.0, -1000.0, -1000.0, -1000.0],-100.0 to [10000.0, 10000.0, -3000.0, 0.9, 2000.0, -1000.0, -1000.0, -1000.0, -100.0]
            passbok[(li_req[0])] = str(list(map(float, passbok[(li_req[0])][1:-1].split(", "))) + [-Amount])
            passbok[(li_req[1])] = str(list(map(float, passbok[(li_req[1])][1:-1].split(", "))) + [Amount])
            cursor.execute("update passbook set passbk=%s where account_number=%s ;",[f"{passbok[li_req[0]]}", li_req[0]])
            cursor.execute("update passbook set passbk=%s where account_number=%s ;",[f"{passbok[li_req[1]]}", li_req[1]])
            mycon.commit()
            mycon.close()
            return redirect(url_for('fundtc', ft_val="fundt_success"))
    elif not accFrom_valid:
        return redirect(url_for('fundtc', ft_val="fundt_accfInvalid"))
    elif not accTo_valid:
        return redirect(url_for('fundtc', ft_val="fundt_acctInvalid"))
    elif not emp_valid:
        return redirect(url_for('fundtc', ft_val="fundt_empInvalid"))
    elif not senderBlk:
        return redirect(url_for('fundtc', ft_val="fundt_senderBlocked"))
    elif not receiverBlk:
        return redirect(url_for('fundtc', ft_val="fundt_receiverBlocked"))

UPLOAD_FOLDER = 'static/docs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/credit")
def credit():
    return render_template("credit.html")

@app.route("/credit", methods=["POST"])
def credit1():
    mycon=sqltor.connect(host="localhost",user="root",passwd="admin",database="bank_management")
    cur = mycon.cursor()
    accno = int(request.form["accno"])
    sec = request.form["sec"]
    name = request.form["name"]
    email = request.form["email"]
    cno = request.form["cno"]
    state = request.form["state"]
    zip = request.form["zip"]
    city = request.form["city"]
    adr = request.form["adr"]

    Aadhar = request.files['Aadhar']
    filename = secure_filename(Aadhar.filename)
    Aadhar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    pan = request.files['pan']
    filename = secure_filename(pan.filename)
    pan.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    poa = request.files['poa']
    filename = secure_filename(poa.filename)
    poa.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    poi = request.files['poi']
    filename = secure_filename(poi.filename)
    poi.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cur.execute("select account_holder,contact_number,email,security_code from accountdetails where account_number=%s",[accno])
    l=cur.fetchall()
    if (name, cno, email, sec) in l:
        # cur.execute("insert into creditcard values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (accno,sec,name,email,cno,state,zip,city,adr,Aadhar,pan,poa,poi))
        # mycon.commit()
        email_sender = "drdev.maill@gmail.com"
        email_password = "mmieeonadmnrylqz"
        email_receiver = ["srinivasadvaith05@gmail.com"]
        body = f"""
Dear Admin Team,

Account number {accno} has requested for a credit card. Details are as given below
accno = {accno}
sec = {sec}
name = {name}
email = {email}
cno = {cno}
state = {state}
zip = {zip}
city = {city}
adr = {adr}
Aadhar = {Aadhar}
pan = {pan}
poa = {poa}
poi = {poi}

Sincerely,
Your Bank
                """
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = "Credit Card request"
        em.set_content(body)
        import ssl
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        mycon.commit()
        cur.close()
        mycon.close()
        return redirect(url_for("statuscre",check="success"))
    else:
        return redirect(url_for("statuscre", check="fail"))

@app.route("/statuscre/<check>")
def statuscre(check):
    return render_template("credit.html",check=check)

if __name__ == '__main__':
    app.run(debug=True)
