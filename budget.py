from db import cr,mydb


# --- Budget Systems ---
def show_budget(typ="%", amount=None, upper_limit=None, lower_limit=None):
    p = f"SELECT * FROM budget WHERE type LIKE '{typ}'"
    if amount is not None:
        p += f" AND CAST(amount AS DECIMAL) = CAST({amount} AS DECIMAL)"
    else:
        if upper_limit is not None and lower_limit is not None:
            p += f" AND amount BETWEEN {lower_limit} AND {upper_limit}"
        elif upper_limit is not None:
            p += f" AND amount < {upper_limit}"
        elif lower_limit is not None:
            p += f" AND amount > {lower_limit}"
            
    cr.execute(p)
    results = cr.fetchall()
    for i in results:
        print(f''' Category: {i[0]}
Amount: {i[1]}''')
        print("-" * 30)
    print("Total Results Found:", len(results))
    return results

def set_budget(typ, amount):
    q = "INSERT INTO budget (type, amount) VALUES (%s, %s)"
    data = (typ, amount)
    cr.execute(q, data)
    mydb.commit()
    print("Budget Successfully Added")

def remove_budget(typ):
    p = f"DELETE FROM budget WHERE type LIKE '{typ}'"
    print("Are You Sure??")
    x = input(">>> ")
    if x.lower() == "yes":
        cr.execute(p)
        mydb.commit()
        print("Successfully Removed")