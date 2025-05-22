import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
DB_FILE='transaction.db'
def init_db():
    conn=sqlite3.connect(DB_FILE)
    cursor=conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        credit REAL,
        debit REAL,
        running_balance REAL)
    """)
    conn.commit()
    conn.close()
def get_last_balance():
    conn=sqlite3.connect(DB_FILE)
    cursor=conn.cursor()
    cursor.execute("SELECT running_balance FROM transactions ORDER BY date DESC, id DESC LIMIT 1")
    row=cursor.fetchone()
    conn.close()
    return row[0] if row else 0



def insert_transaction(date,description,credit,debit,balance):
    conn=sqlite3.connect(DB_FILE)
    cursor=conn.cursor()
    cursor.execute("""
INSERT INTO transactions (date, description, credit, debit, running_balance)
                   VALUES(?,?,?,?,?)
                   """,(date, description, credit, debit, balance))
    conn.commit()
    conn.close()

def show_transactions():
    conn=sqlite3.connect(DB_FILE)

    df=pd.read_sql_query("SELECT * FROM transactions ORDER BY date DESC, id DESC",conn)
    conn.close()
    st.dataframe(df)

def add_transaction_form():
    st.header("Add transaction")
    t_type=st.selectbox("Transaction Type",["Credit","Debit"])
    amount=st.number_input("Amount", min_value=1.0)
    desc=st.text_input("Description")
    if st.button("Save"):
        if not desc or amount==0:
            st.warning("Description and amount are required.")
        else:
            last_balance=get_last_balance()
            if t_type=="Credit":
                credit,debit=amount,0.0
                balance=last_balance+amount
            else:
                credit,debit=0.0,amount
                balance=last_balance-amount
            today=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            insert_transaction(today, desc, credit,debit,balance)
            st.success("Transaction saved!")

def main():
    st.title("Office Transactions")
    m = ["View Transactions", "Add Transaction"]

    choice = st.sidebar.selectbox("Menu", m)
    init_db()
    if choice == "View Transactions":
        show_transactions()
    else:
        add_transaction_form()  

if __name__ == "__main__":
    main()
