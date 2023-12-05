import pandas as pd
df=pd.read_csv("accDeets.csv",header=None,sep="|")
# t=789012345
# for x in df['Account_No']:
#     if x == 789012345:
#         ind=df['Account_No'].index(x)
# print(df['Signature_Path'][x])
# print(df['Account_No'])
df.columns=['account_number', 'signature', 'contact_number', 'email','security_code', 'address', 'account_holder', 'balance', 'account_type','account_status', 'transaction_code', 'keys_array', 'amount']


# print(df.head())
# for x in range(len(df["account_number"])):
#     if df['account_number'][x]==789901234:
#         ind=x
# print(df['signature'][ind])

print("key3" in ["key33", "key34"])