
def keysExtractions(s):
    """
    :param s: Value from Dataframe for a list object in the form of a string
    :return: list of keys
    """
    s=s[1:-1]
    print(s)
    t=""
    for x in s:
        if x.isalpha() or x.isdigit():
            t+=x
        if x==",":
            t+=x
    return t.split(",")

def reason(s):
    """
    :param s: Value from column account_status from table account_details
    :return: Reason for account block
    """
    s=(s.split(": "))
    s=(s[1].split(","))
    return (s[0][1:-1])

def AccountValidity(t,df):
    """
    :param t: Account no who's presence in database will be verified
    :param df: DataFrame of Table to be checked in
    :return: TRUE if account is present in Database | False if account isn't present
    """
    if not(int(t) in (list(map(int,list(df["account_number"].values))))):
        return False
    else:
        return True

def findIndex(emp,column,empID):
    """
    :param emp: Dataframe to parsed through
    :param column: The column index
    :param empID: The value that must be found in the column
    :return: type: int The INDEX of the value in the Series object
    """
    ind1=0
    for x in range(len(emp[column])):
        if empID == emp[column][x]:
            ind1 = x
    return ind1

def findNameIndex(emp,empID):
    """
    :param emp: Dataframe to parsed through
    :param column: The column index
    :param empID: The value that must be found in the column
    :return: type: int The INDEX of the value in the Series object
    """
    ind1=0
    for x in range(len(emp['account_holder'])):
        if empID.upper() == emp['account_holder'][x].upper():
            ind1 = x
    return ind1

def refreshBalanceFromPassBook(passBook):
    """
    :param passBook: Dataframe for the table passbook
    :return: Refreshes the change in balance in the table passbook into the table accountDetails
    """
    import mysql.connector as sqltor
    mycon = sqltor.connect(host="localhost", user="root", passwd="admin", database="bank_management")
    cursor = mycon.cursor()
    for x, y in zip(passBook['passbk'], passBook['account_number']):
        t = (sum(list(map(float, ((x[1:-1]).split(", "))))))
        query = "UPDATE accountDetails SET balance = %s WHERE account_number = %s;"
        cursor.execute(query, (t, y))
    mycon.commit()
    cursor.close()
    mycon.close()

def checkFBalance(amount, df, f):


    """
    :param amount: The amount to be debited from the account f
    :param df: Dataframe of the table accountDetails
    :param f: The account no. from whom the funds are being transferred from
    :return: A Tuple with the first value being a boolean (True if transaction is possible | False if transaction isn't possible), the second value being (Remaining balance | Missing Funds)
    """
    ind1=None
    for x in range(len(df["account_number"])):
        if f == df["account_number"][x]:
            ind1 = x
    diff=(df['balance'][ind1]) - amount
    if diff> 0:
        return (True)
    else:
        return (False)

def GETpassbk(tInd,passBook):
    """
    :param tInd: Index for which you need the value of passbk  in the table passbook
    :param passBook: The dataframe for the table passbook
    :return: The value for the tInd in passbk
    """
    return list(map(float,((passBook['passbk'][tInd])[1:-1].split(", "))))