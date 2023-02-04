import sqlite3

class Model:
    def __init__(self):
        self.con = sqlite3.connect('atm.db')
        self.cur = self.con.cursor()
        self.cur.execute(""" CREATE TABLE if not exists ATM(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Account_no integer type UNIQUE,
                                Name text,
                                Surname text,
                                Password integer,
                                Amount integer)
                                """)

    def addToTable(self, account_no, name, surname, password, amount):
        self.values = (int(account_no), str(name), str(surname), int(password), int(amount))
        self.cur.execute("INSERT INTO ATM (Account_no, Name, Surname, Password, Amount) "
                         "values (?,?,?,?,?)", self.values)
        #print(self.cur.fetchall())
        self.con.commit()

    def getAllData(self):
        self.cur.execute("SELECT * FROM ATM")
        result = self.cur.fetchall()
        #print(result)
        self.con.commit()
        return result

    def login(self, account_no, password):
        self.cur.execute(f"SELECT * FROM ATM WHERE Account_no = {account_no} and Password = {password}")
        result = self.cur.fetchone()
        self.con.commit()
        return result

    def update_balance(self, current_balance, account_no):
        self.cur.execute(f"UPDATE ATM SET Amount= {current_balance} WHERE Account_no = {account_no}")
        self.con.commit()

    def check_account_no(self, account_no):
        self.cur.execute("SELECT Account_no FROM ATM")
        result = self.cur.fetchall()
        self.con.commit()
        if account_no in result:
            return False
        else:
            return account_no
