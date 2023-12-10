from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import mysql.connector as sqltor
from processing import *
from datetime import datetime
import random

app = Flask(__name__)

mycon = sqltor.connect(host="localhost", user="root", passwd="6649a3so4", database="bank_management")

dfa = pd.read_sql(f"select * from accountdetails;", mycon)


@app.route('/')
def home():
    return render_template("index.html")



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
                    email_receiver = ["a101reasons@gmail.com"]
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


@app.route("/balanceenq/<check>")
def balenq(check):
    return render_template("balanceenq.html", check=check)

@app.route("/balanceenq/<check>", methods=["POST"])
def balenq2(check):
    otp = request.form["otp"]
    print(t, otp)
    balance = dfa["balance"][findIndex(dfa, 'email', t)]
    check = "success"
    return render_template("balanceenq.html", check=check, balances=balance)

@app.route("/balenceenq", methods=["POST"])
def balenq1():
    a = request.form["accname"]
    b = request.form["email"]
    mycon = sqltor.connect(host="localhost", user="root", passwd="6649a3so4", database="bank_management")
    dfa = pd.read_sql(f"select * from accountdetails;", mycon)
    if a in list(dfa["account_holder"].values):
        print(a, type(a), dfa["account_holder"][0], type(dfa["account_holder"][0]))
        if b == dfa["email"][findIndex(dfa, "email", a)]:
            global t
            t = b
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
                try:
                    otp = request.form["otp"]
                    if d == t:
                        return redirect(url_for('balenq', check="success"))
                except:
                    pass
            return redirect(url_for('balenq', check="otp"))


        else:
            return redirect(url_for('balenq', check="noemail"))
    else:
        return redirect(url_for('balenq', check="noacc"))


if __name__ == '__main__':
    app.run(debug=True)
