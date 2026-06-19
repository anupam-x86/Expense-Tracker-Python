from db import mydb, cr, get_currency, get_usr
from auth import login, change_psswd, delete_account
from records import show_records, register_record, remove_record
from budget import show_budget, set_budget, remove_budget
from settings import set_currency, export_csv, backup, restore
import datetime
def signup():
    while True:
        print("Sign up")
        uname = input("Username: ").strip()
        if uname != "":
            psswd = input("Password: ")
            if len(psswd) >= 5:
                q = "INSERT INTO auth VALUES (%s, %s)"
                cr.execute(q, (uname, psswd))
                mydb.commit()
                return uname, True
            else:
                print("Password must be at least 5 characters!")
        else:
            print("Username cannot be empty!")

def main():
    usr = get_usr()
    
    if len(usr) == 0:
        uname, is_loggedin = signup()
    else:
        uname = usr[0][0]
        is_loggedin = login()

    while is_loggedin:
        print('''
1) Manage Records
2) Manage Budget
3) Settings
4) Exit''')
        inp = input("> ").strip()

        if inp == "1":
            records_menu()
        elif inp == "2":
            budget_menu()
        elif inp == "3":
            result = settings_menu(uname)
            if result == 'deleted':
                break
        elif inp == "4":
            confirm = input("Are you sure you want to exit? (yes/no): ")
            if confirm.lower() == "yes":
                break
        else:
            print("Invalid Choice")

    mydb.commit()
    mydb.close()

def records_menu():
    while True:
        print('''
1) Show Records
2) Add Records
3) Remove Records
4) Back''')
        inp = input("> ").strip()
        if inp == "1":
            try:
                print("Leave Blank for checking all data")
                payee = input("Payee: ")
                category = input("Category: ")
                if "," in category:
                    category = category.split(",")
                transaction_type = input("Transaction type: ")
                payment_mode = input("Payment Mode: ")
                
                x = [payee, category, transaction_type, payment_mode]
                for i in range(len(x)):
                    if isinstance(x[i], str) and len(x[i]) == 0:
                        x[i] = "%"
                payee, category, transaction_type, payment_mode = tuple(x)
                
                amount = input("Amount: ")
                if amount != "":
                    try:
                        amount = int(amount)
                    except ValueError:
                        print("Amount Should be a Number")
                        amount = 0
                else:
                    amount = 0
                    
                upper_limit, lower_limit, tdate, fdate = None, None, None, None
                if amount == 0:
                    amount = None
                    up_limit = input("Upper Limit: ")
                    low_limit = input("Lower Limit: ")
                    if up_limit != "": upper_limit = int(up_limit)
                    if low_limit != "": lower_limit = int(low_limit)
                    
                date = input("Date (YYYY-MM-DD): ")
                if date == "":
                    fdate_str = input("From Date (YYYY-MM-DD): ")
                    tdate_str = input("To Date (YYYY-MM-DD): ")
                    fdate = fdate_str if fdate_str != "" else None
                    tdate = tdate_str if tdate_str != "" else None
                else:
                    fdate = tdate = date
                    
                try:
                    show_records(payee, category, amount, transaction_type, payment_mode, fdate, tdate, upper_limit, lower_limit)
                except Exception:
                    mydb.rollback()
                    print("Something went wrong")
            except Exception as e:
                mydb.rollback()
                print(f"Something went wrong: {e}")       
        elif inp == "2":
            try:
                payee = input("Payee: ")
                category = input("Category: ")
                transaction_type = input("Transaction_type: ")
                payment_mode = input("Payment Mode: ")
                amount = int(input("Amount: "))
                date = input("Date (YYYY-MM-DD): ")
                if date == "":
                    date = datetime.datetime.now().date()
                description = input("Description (Optional): ")
                
                if payee != "" and category != "" and transaction_type != "" and payment_mode != "" and amount > 0:
                    register_record(payee, category, transaction_type, payment_mode, amount, date, description)
                else:
                    print("Something went wrong!")
            except Exception:
                print("Something went wrong!!")
        elif inp == "3":
            try:
                payee = input("Payee: ")
                category = input("Category: ")
                transaction_type = input("Transaction type: ")
                payment_mode = input("Payment Mode: ")
                amount_str = input("Amount: ")
                amount = int(amount_str) if amount_str != "" else None
                date = input("Date (YYYY-MM-DD): ")
                remove_record(payee, category, amount, transaction_type, payment_mode, date if date != "" else "%")
            except Exception:
                print("Something went wrong!")
        elif inp == "4":
            break
        else:
            print("Invalid Choice")

def budget_menu():
    while True:
        print('''
1) Show Budget
2) Add Budget
3) Remove Budget
4) Back''')
        inp = input("> ").strip()
        if inp == "1":
            try:
                typ = input("Name: ")
                if typ == "": typ = "%"
                amount_str = input("Amount: ")
                amount = int(amount_str) if amount_str != "" else None
                
                upper_limit, lower_limit = None, None
                if amount is None or amount == 0:
                    amount = None
                    up_limit = input("Upper Limit: ")
                    low_limit = input("Lower Limit: ")
                    if up_limit != "": upper_limit = int(up_limit)
                    if low_limit != "": lower_limit = int(low_limit)
                show_budget(typ, amount, upper_limit, lower_limit)
            except Exception as e:
                print(f"Something went wrong: {e}")
        elif inp == "2":
                typ = input("Name: ")
                amount = int(input("Amount: "))
                if typ != "" and amount > 0:
                    set_budget(typ, amount)
                else:
                    print("Something went wrong!")
        elif inp == "3":
                typ = input("Name: ")
                if typ != "":
                    remove_budget(typ)
        elif inp == "4":
            break
        else:
            print("Invalid Choice")

def settings_menu(uname):
    while True:
        print('''
1) Current Currency Format
2) Change Currency Format
3) Export as CSV
4) Backup
5) Restore
6) Change Password
7) Delete Account
8) Back''')
        inp = input("> ").strip()
        if inp == "1":
            print(f"Currently Currency is in {get_currency()} format")
        elif inp == "2":
            cr.execute("SELECT * FROM currency;")
            options_avail = cr.fetchall()
            for i,j in options_avail:
                if i == get_currency():
                    print(i,"(SELECTED) ----> ",float(j))
                else:
                    print(i,"           ----> ", float(j))
            set_currency()
        elif inp == "3":
            fil = input("File Name: ")
            if fil != "":
                export_csv(fil)
        elif inp == "4":
            backup()
        elif inp == "5":
            restore()
        elif inp == "6":
            change_psswd(uname)
        elif inp == "7":
            delete_account()
            return "deleted"
        elif inp == "8":
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()