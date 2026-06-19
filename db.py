import mysql.connector as sql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import requests
# --- Global State ---
_currency_DATA = requests.get("https://api.frankfurter.dev/v2/rates?base=INR").json()
_currency = "INR"

# --- Database Connection ---
def _init_db():
    global mydb, cr
    try:
        mydb = sql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cr = mydb.cursor()
    except sql.errors.ProgrammingError:
        # Database doesn't exist yet, create it
        mydb = sql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cr = mydb.cursor()
        _create_database()

def _create_database():
    cr.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cr.execute(f"USE {DB_NAME}")
    _create_tables()
    mydb.commit()
    print("Database Initialised")

def _create_tables():
    cr.execute('''CREATE TABLE IF NOT EXISTS expense (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL,
        amount DECIMAL(10,2),
        transactionType VARCHAR(30),
        paymentMode VARCHAR(30),
        payee VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        description VARCHAR(10000),
        currencyType VARCHAR(10)
    )''')

    cr.execute('''CREATE TABLE IF NOT EXISTS auth (
        uname VARCHAR(50) PRIMARY KEY,
        psswd VARCHAR(50) NOT NULL
    )''')

    cr.execute('''CREATE TABLE IF NOT EXISTS currency (
        type VARCHAR(50) PRIMARY KEY,
        value DECIMAL(20,10)
    )''')

    cr.execute('''CREATE TABLE IF NOT EXISTS budget (
        type VARCHAR(50) PRIMARY KEY,
        amount DECIMAL(9,2) NOT NULL
    )''')

    # Only insert default currencies if table is empty
    cr.execute("SELECT COUNT(*) FROM currency")
    q = []
    for i in _currency_DATA:
        q.append(str((i["quote"],i["rate"])))
    p = ",".join(q)
    if cr.fetchone()[0] == 0:
        cr.execute(f"""
            INSERT INTO currency VALUES {p}
        """)

# --- Global State Functions ---
def get_currency():
    return _currency

def set_currency_state(new_currency):
    global _currency
    _currency = new_currency

def get_usr():
    cr.execute("SELECT * FROM auth")
    return cr.fetchall()
# --- Initialize ---
_init_db()