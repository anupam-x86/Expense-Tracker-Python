from db import cr,mydb
from config import DB_NAME
# --- Authentication Management ---
def login():
    cr.execute("SELECT * FROM auth")
    usr = cr.fetchall()
    if not usr:
        return False
        
    logged_in = False
    while not logged_in:
        print("\nLogin")
        uname = input("Username: ")
        if uname == usr[0][0]:
            psswd = input("Password: ")
            if psswd == usr[0][1]:
                logged_in = True
                print("Logged In..")
                break
            else:
                print("Something went Wrong!")
        else:
            print("Something went Wrong!")
    return logged_in

def change_psswd(uname):
    global usr
    psswd = input("Old Password: ")
    if psswd == usr[0][1]:
        npsswd = input("New Password: ")
        if npsswd != psswd:
            cpsswd = input("Confirm Password: ")
            if npsswd == cpsswd:
                q = "UPDATE auth SET psswd = %s WHERE uname = %s"
                cr.execute(q, (npsswd, uname))
                mydb.commit()
                print("Password Updated Successfully!")
            else:
                print("Something went wrong!")
        else:
            print("Something went wrong!")
    else:
        print("Something went wrong!")

def delete_account():
    print("All the stored data will be deleted along with account deletion\n Are you Sure?")
    x = input(">>> ")
    if x.lower() == "yes":
        q = f"DROP DATABASE {DB_NAME}"
        cr.execute(q)
        mydb.commit()
        print("Account Deleted Successfully.")
        exit()
