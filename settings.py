from db import cr, mydb, get_currency, set_currency_state
import csv,datetime


# --- Global Configuration Settings ---
def set_currency():
    # currency = get_currency()
    cr.execute("SELECT * FROM currency;") 
    currency_DATA = cr.fetchall() 
    new_currency = input("Enter the currency (USD, INR, EUR): ").strip().upper()
    print(new_currency)
    x = 0
    for i in currency_DATA:
        print(currency_DATA.index(i),i)
        if i[0] == new_currency:
            print("TRUE")
            x = float(i[1])
            
    if x == 0:
        print("Invalid currency selected.")
        return
        
    for j in currency_DATA:
        j_list = list(j)
        j_list[1] = float(j_list[1]) / x
        q = f"UPDATE currency SET value = {j_list[1]} WHERE type='{j_list[0]}';"
        cr.execute(q)
    try:
        cr.execute("SELECT * FROM expense")
        data = cr.fetchall()
        for i in data:
            i_list = list(i)
            i_list[2] = float(i_list[2])
            i_list[2] *= x
            i_list[-1] = new_currency
            q = f"UPDATE expense SET amount = {i_list[2]}, currencyType='{i_list[-1]}' WHERE id={i_list[0]};"
            cr.execute(q)
    except:
        pass

    set_currency_state(new_currency)        
    mydb.commit()
    print("Currency Setup Completed.")

def export_csv(name):
    cr.execute("SELECT * FROM expense")
    data = cr.fetchall()
    csv_file = f"{name}.csv"
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        for i in data:
            writer.writerow(list(i))
    print(f"Data exported to {csv_file} successfully")

def backup():
    export_csv("backup")
    print("Backup Successfully Created")

def restore():
    csv_file = "backup.csv"
    try:
        with open(csv_file, "r", newline="") as file:
            reader = csv.reader(file)
            data = []
            for i in reader:
                i[1] = datetime.datetime.strptime(i[1], '%Y-%m-%d').date()
                i.remove(i[0])  # Remove auto-increment primary ID tracking key
                data.append(tuple(i))
            q = "INSERT INTO expense (date, amount, transactionType, paymentMode, payee, category, description, currencyType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cr.executemany(q, data)
            mydb.commit()
            print("Data Restored successfully")
    except FileNotFoundError:
        print("No such backup file found")
