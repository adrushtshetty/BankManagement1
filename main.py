from flask import Flask, request, jsonify, render_template, url_for, redirect
import pandas as pd
app = Flask(__name__)
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
                            if len(df['account_status'][findIndex(df, "account_number", f)])>14 and len(df['account_status'][findIndex(df, "account_number", t)])>14:

                                mainblk="Both Accounts"
                                blockedAccount1=f
                                rsn1=reason(df['account_status'][findIndex(df, "account_number", f)])
                                blockedAccount2=t
                                rsn2=reason(df['account_status'][findIndex(df, "account_number", t)])


                            elif len(df['account_status'][findIndex(df, "account_number", t)])>14:

                                blockedAccount1,mainblk=f,str(f)+" Account "
                                rsn1=reason(df['account_status'][findIndex(df, "account_number", f)])
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

    df1 = df.copy()
    df2 = emp.copy()
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
            cursor.execute("update passbook set passbk=%s where account_number=%s ;",[f"{passbok[li_req[0]]},-{Amount}", li_req[0]])
            cursor.execute("update passbook set passbk=%s where account_number=%s ;",[f"{passbok[li_req[1]]},{Amount}", li_req[1]])
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
        l = ["cno", "em", "add", "acchol", "acctyp", "accstat"]
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
    email = request.form["email"]
    email1 = request.form["email1"]
    if email == email1:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set email=%s where account_number=%s", (email, accno))
        mycon.commit()
        cur.close()
        mycon.close()
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
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno = int(accno[0])
    cur.execute("select account_type from accountdetails where account_number=%s", [accno])
    lacc = cur.fetchall()
    print(lacc)
    if ("Current",) in lacc:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
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

if __name__ == "__main__":
    app.run(debug=True)




if __name__ == '__main__':
    app.run(debug=True)