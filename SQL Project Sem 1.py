import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------
def create_database():
    conn = sqlite3.connect("BankDB.db")
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Customers (
      CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
      Name TEXT,
      Gender CHAR(1),
      Age INTEGER,
      City TEXT,
      Phone TEXT
    );

    CREATE TABLE IF NOT EXISTS Branches (
      BranchID INTEGER PRIMARY KEY AUTOINCREMENT,
      BranchName TEXT,
      City TEXT
    );

    CREATE TABLE IF NOT EXISTS Accounts (
      AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
      CustomerID INTEGER,
      BranchID INTEGER,
      AccountType TEXT,
      Balance DECIMAL(12,2),
      FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
      FOREIGN KEY (BranchID) REFERENCES Branches(BranchID)
    );

    CREATE TABLE IF NOT EXISTS Transactions (
      TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
      AccountID INTEGER,
      Date TEXT,
      Type TEXT,
      Amount DECIMAL(10,2),
      FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
    );
    """)
    conn.commit()
    conn.close()
    messagebox.showinfo("Database", "Database ready to use!")

# ---------------------------------------
# ADD DATA FORMS
# ---------------------------------------
def add_customer():
    form = tk.Toplevel(root)
    form.title("Add Customer")
    form.geometry("400x300")

    labels = ["Name", "Gender (M/F)", "Age", "City", "Phone"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(form, text=label, font=("Arial", 11)).grid(row=i, column=0, pady=5, padx=10, sticky="w")
        entries[label] = tk.Entry(form, width=25)
        entries[label].grid(row=i, column=1, pady=5)

    def save_customer():
        conn = sqlite3.connect("BankDB.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Customers (Name, Gender, Age, City, Phone) VALUES (?, ?, ?, ?, ?)",
                       (entries["Name"].get(), entries["Gender (M/F)"].get(),
                        entries["Age"].get(), entries["City"].get(), entries["Phone"].get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Customer added successfully!")
        form.destroy()

    tk.Button(form, text="Save", bg="#28a745", fg="white", command=save_customer).grid(row=len(labels), column=1, pady=15)

def add_branch():
    form = tk.Toplevel(root)
    form.title("Add Branch")
    form.geometry("400x200")

    tk.Label(form, text="Branch Name").grid(row=0, column=0, pady=5, padx=10)
    tk.Label(form, text="City").grid(row=1, column=0, pady=5, padx=10)
    bname = tk.Entry(form, width=25)
    city = tk.Entry(form, width=25)
    bname.grid(row=0, column=1, pady=5)
    city.grid(row=1, column=1, pady=5)

    def save_branch():
        conn = sqlite3.connect("BankDB.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Branches (BranchName, City) VALUES (?, ?)", (bname.get(), city.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Branch added successfully!")
        form.destroy()

    tk.Button(form, text="Save", bg="#28a745", fg="white", command=save_branch).grid(row=2, column=1, pady=15)

def add_account():
    form = tk.Toplevel(root)
    form.title("Add Account")
    form.geometry("400x300")

    tk.Label(form, text="Customer ID").grid(row=0, column=0, pady=5, padx=10)
    tk.Label(form, text="Branch ID").grid(row=1, column=0, pady=5, padx=10)
    tk.Label(form, text="Account Type").grid(row=2, column=0, pady=5, padx=10)
    tk.Label(form, text="Balance").grid(row=3, column=0, pady=5, padx=10)

    cid = tk.Entry(form, width=25)
    bid = tk.Entry(form, width=25)
    atype = tk.Entry(form, width=25)
    bal = tk.Entry(form, width=25)
    cid.grid(row=0, column=1)
    bid.grid(row=1, column=1)
    atype.grid(row=2, column=1)
    bal.grid(row=3, column=1)

    def save_account():
        conn = sqlite3.connect("BankDB.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Accounts (CustomerID, BranchID, AccountType, Balance) VALUES (?, ?, ?, ?)",
                       (cid.get(), bid.get(), atype.get(), bal.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Account added successfully!")
        form.destroy()

    tk.Button(form, text="Save", bg="#28a745", fg="white", command=save_account).grid(row=4, column=1, pady=15)

def add_transaction():
    form = tk.Toplevel(root)
    form.title("Add Transaction")
    form.geometry("400x300")

    tk.Label(form, text="Account ID").grid(row=0, column=0, pady=5, padx=10)
    tk.Label(form, text="Date (YYYY-MM-DD)").grid(row=1, column=0, pady=5, padx=10)
    tk.Label(form, text="Type (Deposit/Withdraw)").grid(row=2, column=0, pady=5, padx=10)
    tk.Label(form, text="Amount").grid(row=3, column=0, pady=5, padx=10)

    aid = tk.Entry(form, width=25)
    date = tk.Entry(form, width=25)
    ttype = tk.Entry(form, width=25)
    amt = tk.Entry(form, width=25)
    aid.grid(row=0, column=1)
    date.grid(row=1, column=1)
    ttype.grid(row=2, column=1)
    amt.grid(row=3, column=1)

    def save_transaction():
        conn = sqlite3.connect("BankDB.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Transactions (AccountID, Date, Type, Amount) VALUES (?, ?, ?, ?)",
                       (aid.get(), date.get(), ttype.get(), amt.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Transaction added successfully!")
        form.destroy()

    tk.Button(form, text="Save", bg="#28a745", fg="white", command=save_transaction).grid(row=4, column=1, pady=15)

# ---------------------------------------
# REPORT WINDOW
# ---------------------------------------
def show_reports():
    conn = sqlite3.connect("BankDB.db")
    queries = {
        "a) Total Transactions per Customer": """
        SELECT c.Name, COUNT(t.TransactionID) AS TotalTransactions
        FROM Customers c
        JOIN Accounts a ON c.CustomerID = a.CustomerID
        JOIN Transactions t ON a.AccountID = t.AccountID
        GROUP BY c.Name
        """,

        "b) Deposits and Withdrawals by Branch": """
        SELECT b.BranchName,
               SUM(CASE WHEN t.Type='Deposit' THEN t.Amount ELSE 0 END) AS TotalDeposits,
               SUM(CASE WHEN t.Type='Withdraw' THEN t.Amount ELSE 0 END) AS TotalWithdrawals
        FROM Branches b
        JOIN Accounts a ON b.BranchID = a.BranchID
        JOIN Transactions t ON a.AccountID = t.AccountID
        GROUP BY b.BranchName
        """,

        "c) Top Customer by Transaction Volume": """
        SELECT c.Name, SUM(t.Amount) AS TotalAmount
        FROM Customers c
        JOIN Accounts a ON c.CustomerID = a.CustomerID
        JOIN Transactions t ON a.AccountID = t.AccountID
        GROUP BY c.Name
        ORDER BY TotalAmount DESC LIMIT 1
        """,

        "d) Average Account Balance per Branch": """
        SELECT b.BranchName, AVG(a.Balance) AS AvgBalance
        FROM Branches b
        JOIN Accounts a ON b.BranchID = a.BranchID
        GROUP BY b.BranchName
        """,

        "e) Suspicious Transactions (> ₹20,000)": """
        SELECT t.TransactionID, c.Name, t.Type, t.Amount, t.Date
        FROM Transactions t
        JOIN Accounts a ON t.AccountID = a.AccountID
        JOIN Customers c ON a.CustomerID = c.CustomerID
        WHERE t.Amount > 20000
        """
    }

    win = tk.Toplevel(root)
    win.title("Bank Reports")
    win.geometry("900x700")

    for title, q in queries.items():
        df = pd.read_sql_query(q, conn)
        tk.Label(win, text=title, font=("Arial", 12, "bold")).pack(pady=5)
        tree = ttk.Treeview(win, columns=list(df.columns), show="headings", height=5)
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
        for row in df.itertuples(index=False):
            tree.insert("", "end", values=row)
        tree.pack(pady=3)

    conn.close()

# ---------------------------------------
# MAIN WINDOW
# ---------------------------------------
root = tk.Tk()
root.title("🏦 BankDB Interactive Manager")
root.geometry("420x420")
root.config(bg="#e6f2ff")

tk.Label(root, text="Bank Database Manager", font=("Helvetica", 16, "bold"), bg="#e6f2ff").pack(pady=15)

tk.Button(root, text="Create Database", bg="#007acc", fg="white", width=25, command=create_database).pack(pady=5)
tk.Button(root, text="Add Customer", bg="#4caf50", fg="white", width=25, command=add_customer).pack(pady=5)
tk.Button(root, text="Add Branch", bg="#4caf50", fg="white", width=25, command=add_branch).pack(pady=5)
tk.Button(root, text="Add Account", bg="#4caf50", fg="white", width=25, command=add_account).pack(pady=5)
tk.Button(root, text="Add Transaction", bg="#4caf50", fg="white", width=25, command=add_transaction).pack(pady=5)
tk.Button(root, text="View Reports", bg="#ff9800", fg="white", width=25, command=show_reports).pack(pady=5)
tk.Button(root, text="Exit", bg="#d9534f", fg="white", width=25, command=root.destroy).pack(pady=5)

root.mainloop()
