from flask import Flask, request, jsonify, render_template, url_for,redirect
import mysql.connector as ms
import pandas as pd
app=Flask(__name__)
mycon=ms.connect(host="localhost",user="root",passwd="root",database="bank_management")
cur=mycon.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status/<check>")
def status(check):
    return render_template("change1.html",check=check)

@app.route("/change")
def change():
    return render_template("change1.html")

@app.route("/change",methods=["POST"])
def change1():
    global accno
    accno=int(request.form["Acc"])
    with open('temp.txt', 'w') as file:
        file.write(f"{accno}")
    empid=request.form["empid"]
    pin=request.form["empd"]
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
    cur = mycon.cursor()
    cur.execute("select account_number from accountdetails")
    lacc=cur.fetchall()
    cur.execute("select empid, pin from emp")
    lemp=cur.fetchall()
    mycon.commit()
    cur.close()
    mycon.close()
    if (accno,) in lacc and (empid,pin) in lemp:
        l=["cno","em","add","acchol","acctyp","accstat"]
        return redirect(url_for(l[int(request.form["sel"])]))
    else:
        return redirect(url_for("status",check="InvalidCredentials"))

@app.route("/cno")
def cno():
    return render_template("Contact number.html")

@app.route("/cno",methods=["POST"])
def contact():
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno=int(accno[0])
    con=int(request.form["con"])
    con1=int(request.form["con1"])
    if con==con1:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set contact_number={0} where account_number={1}".format(con,accno))
        mycon.commit()
        cur.close()
        mycon.close()
        
        return redirect(url_for("status",check='success'))
    else:
        return redirect(url_for("Statuscno",check='change_error'))

@app.route("/statusCn/<check>")
def Statuscno(check):
    return render_template("Contact number.html",check=check)

@app.route("/em")
def em():
    return render_template("email.html")

@app.route("/em",methods=["POST"])
def email():
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno=int(accno[0])
    email = request.form["email"]
    email1 = request.form["email1"]
    if email == email1:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set email=%s where account_number=%s",(email, accno))
        mycon.commit()
        cur.close()
        mycon.close()
        return redirect(url_for("status", check='success1'))
    else:
        return redirect(url_for("StatusEm", check='change_error'))

@app.route("/statusEm/<check>")
def StatusEm(check):
    return render_template("email.html",check=check)

@app.route("/add")
def add():
    return render_template("address.html")

@app.route("/add",methods=["POST"])
def address():
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno=int(accno[0])
    adr=request.form["adr"]
    if adr != "":
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set address=%s where account_number=%s",(adr, accno))
        mycon.commit()
        cur.close()
        mycon.close()
        return redirect(url_for("status", check='success2'))
    else:
        return redirect(url_for("StatusAdr", check='change_error'))

@app.route("/statusAdr/<check>")
def StatusAdr(check):
    return render_template("address.html",check=check)

@app.route("/acchol")
def acchol():
    return render_template("Account Holder.html")

@app.route("/accounthol",methods=["POST"])
def accounthol():
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno=int(accno[0])
    ach = request.form["ach"]
    ach1 = request.form["ach1"]
    if ach==ach1:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set account_holder=%s where account_number=%s",(ach, accno))
        mycon.commit()
        cur.close()
        mycon.close()
        return redirect(url_for("status", check='success3'))
    else:
        return redirect(url_for("StatusHol", check='change_error'))

@app.route("/statusHol/<check>")
def StatusHol(check):
    return render_template("Account Holder.html",check=check)

@app.route("/acctyp")
def acctyp():
    with open('temp.txt', 'r') as file:
        content = file.read().splitlines()
    if len(content) == 1:
        accno = content
    accno=int(accno[0])
    cur.execute("select account_type from accountdetails where account_number=%s",[accno])
    lacc = cur.fetchall()
    print(lacc)
    if ("Current",) in lacc:
        mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
        cur = mycon.cursor()
        cur.execute("update accountdetails set account_type='Savings' where account_number=%s",[accno])
        mycon.commit()
        cur.close()
        mycon.close()
        return redirect(url_for("status", check='success4'))
    else:
        cur.execute("update accountdetails set account_type='Current' where account_number=%s",[accno])
        mycon.commit()
        return redirect(url_for("status", check='success5'))

if __name__ == "__main__":
    app.run(debug=True)