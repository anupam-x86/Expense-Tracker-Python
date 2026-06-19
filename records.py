from db import cr,mydb
from db import get_currency
import datetime
# --- Expense Records Engine ---
def show_records(payee="%", category="%", amount=None, transaction_type="%", payment_mode="%", fdate=None, tdate=None, upper_limit=None, lower_limit=None):
    p = f"SELECT * FROM expense WHERE payee LIKE '{payee}' AND transactionType LIKE '{transaction_type}' AND paymentMode LIKE '{payment_mode}'"

    # Fixed original logic gap: safely concatenating structural conditions to 'p'
    if category == "%":
        p += f" AND category LIKE '{category}'"
    else:
        if isinstance(category, (list, tuple)):
            p += f" AND category IN {tuple(category)}"
        else:
            p += f" AND category LIKE '{category}'"

    if amount is not None:
        p += f" AND CAST(amount AS DECIMAL) = CAST({amount} AS DECIMAL)"
    else:
        if upper_limit is not None and lower_limit is not None:
            p += f" AND amount BETWEEN {lower_limit} AND {upper_limit}"
        elif upper_limit is not None:
            p += f" AND amount < {upper_limit}"
        elif lower_limit is not None:
            p += f" AND amount > {lower_limit}"

    if tdate is None and fdate is None:
        pass
    else:
        if tdate is not None and fdate is not None:
            p += f" AND date BETWEEN '{fdate}' AND '{tdate}'"
        elif tdate is not None:
            p += f" AND date < '{tdate}'"
        elif fdate is not None:
            p += f" AND date > '{fdate}'"

    cr.execute(p)
    results = cr.fetchall()
    for i in results:
        formatted_date = i[1].strftime("%m/%d/%y") if isinstance(i[1], datetime.date) else i[1]
        print(f''' |
Name: {i[5]}
Category: {i[6]}
Payment Mode: {i[4]}
Transaction Type: {i[3]}
Amount: {i[2]}
Date: {formatted_date}
Description: {i[-2]}
Currency: {i[-1]}''')
        print("-" * 30)
    print("Total Results Found:", len(results))
    return results

def register_record(payee, category, transaction_type, payment_mode, amount, date, description):
    q = "INSERT INTO expense (date, amount, transactionType, paymentMode, payee, category, description, currencyType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    data = (date, amount, transaction_type, payment_mode, payee, category, description, get_currency())
    cr.execute(q, data)
    mydb.commit()
    print("Record Successfully Added")

def remove_record(payee="%", category="%", amount=None, transaction_type="%", payment_mode="%", date="%"):
    results = show_records(payee=payee, amount=amount, category=category, transaction_type=transaction_type, payment_mode=payment_mode, fdate=date if date != "%" else None, tdate=date if date != "%" else None)
    
    p = f"DELETE FROM expense WHERE payee LIKE '{payee}' AND category LIKE '{category}' AND transactionType LIKE '{transaction_type}' AND paymentMode LIKE '{payment_mode}' AND date LIKE '{date}'"
    if amount is not None:
        p += f" AND CAST(amount AS DECIMAL) = CAST({amount} AS DECIMAL)"
        
    if len(results) != 0:
        print("Are You Sure??")
        x = input(">>> ")
        if x.lower() == "yes":
            cr.execute(p)
            mydb.commit()
            print("Successfully Removed")
    else:
        print("No Such DataBase Exists")

