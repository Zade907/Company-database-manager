import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ---------------- Database Connection ----------------
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # replace with your MySQL password
            database="company_db",
            port=3306
        )
        return conn
    except Error as e:
        messagebox.showerror("DB Error", f"Error: {e}")
        return None

# ---------------- Employee Functions ----------------
def add_employee():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    name = emp_name_var.get()
    designation = emp_desig_var.get()
    salary = emp_salary_var.get()
    dept = emp_dept_var.get()

    if not name or not salary:
        messagebox.showwarning("Input Error", "Name and Salary required")
        return

    try:
        cursor.execute("INSERT INTO employee_data (emp_name, emp_designation, emp_salary, emp_department) VALUES (%s,%s,%s,%s)",
                       (name, designation, salary, dept))
        conn.commit()
        messagebox.showinfo("Success", f"Employee {name} added!")
        emp_name_var.set('')
        emp_desig_var.set('')
        emp_salary_var.set('')
        emp_dept_var.set('')
    except Error as e:
        messagebox.showerror("DB Error", f"Error: {e}")
    finally:
        conn.close()

def view_employees():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee_data")
    rows = cursor.fetchall()
    emp_table.delete(*emp_table.get_children())
    for row in rows:
        emp_table.insert('', tk.END, values=row)
    conn.close()

# ---------------- Customer Functions ----------------
def add_customer():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    name = cust_name_var.get()
    contact = cust_contact_var.get()
    address = cust_address_var.get()

    if not name or not contact:
        messagebox.showwarning("Input Error", "Name and Contact required")
        return

    try:
        cursor.execute("INSERT INTO customer_data (customer_name, customer_contact, customer_address) VALUES (%s,%s,%s)",
                       (name, contact, address))
        conn.commit()
        messagebox.showinfo("Success", f"Customer {name} added!")
        cust_name_var.set('')
        cust_contact_var.set('')
        cust_address_var.set('')
    except Error as e:
        messagebox.showerror("DB Error", f"Error: {e}")
    finally:
        conn.close()

def view_customers():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer_data")
    rows = cursor.fetchall()
    cust_table.delete(*cust_table.get_children())
    for row in rows:
        cust_table.insert('', tk.END, values=row)
    conn.close()

# ---------------- Transactions Functions ----------------
def add_transaction():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    cust_id = trans_cust_id_var.get()
    emp_id = trans_emp_id_var.get()
    amount = trans_amount_var.get()
    trans_type = trans_type_var.get()
    date = trans_date_var.get()

    if not cust_id or not emp_id or not amount:
        messagebox.showwarning("Input Error", "Customer ID, Employee ID, and Amount required")
        return

    try:
        cursor.execute(
            "INSERT INTO financial_data (customer_id, emp_id, amount, transaction_type, date) VALUES (%s,%s,%s,%s,%s)",
            (cust_id, emp_id, amount, trans_type, date)
        )
        conn.commit()
        messagebox.showinfo("Success", "Transaction added!")
        trans_cust_id_var.set('')
        trans_emp_id_var.set('')
        trans_amount_var.set('')
        trans_type_var.set('')
        trans_date_var.set('')
    except Error as e:
        messagebox.showerror("DB Error", f"Error: {e}")
    finally:
        conn.close()

def view_transactions():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM financial_data")
    rows = cursor.fetchall()
    trans_table.delete(*trans_table.get_children())
    for row in rows:
        trans_table.insert('', tk.END, values=row)
    conn.close()

# ---------------- Main GUI ----------------
root = tk.Tk()
root.title("Company Database Management")
root.geometry("800x600")

tab_control = ttk.Notebook(root)

# -------- Employee Tab --------
emp_tab = ttk.Frame(tab_control)
tab_control.add(emp_tab, text='Employees')

emp_name_var = tk.StringVar()
emp_desig_var = tk.StringVar()
emp_salary_var = tk.StringVar()
emp_dept_var = tk.StringVar()

tk.Label(emp_tab, text="Name").grid(row=0, column=0)
tk.Entry(emp_tab, textvariable=emp_name_var).grid(row=0, column=1)
tk.Label(emp_tab, text="Designation").grid(row=1, column=0)
tk.Entry(emp_tab, textvariable=emp_desig_var).grid(row=1, column=1)
tk.Label(emp_tab, text="Salary").grid(row=2, column=0)
tk.Entry(emp_tab, textvariable=emp_salary_var).grid(row=2, column=1)
tk.Label(emp_tab, text="Department").grid(row=3, column=0)
tk.Entry(emp_tab, textvariable=emp_dept_var).grid(row=3, column=1)
tk.Button(emp_tab, text="Add Employee", command=add_employee).grid(row=4, column=0, pady=5)
tk.Button(emp_tab, text="View Employees", command=view_employees).grid(row=4, column=1, pady=5)

emp_table = ttk.Treeview(emp_tab, columns=("ID","Name","Designation","Salary","Department"), show='headings')
for col in ("ID","Name","Designation","Salary","Department"):
    emp_table.heading(col, text=col)
emp_table.grid(row=5, column=0, columnspan=2, pady=10)

# -------- Customer Tab --------
cust_tab = ttk.Frame(tab_control)
tab_control.add(cust_tab, text='Customers')

cust_name_var = tk.StringVar()
cust_contact_var = tk.StringVar()
cust_address_var = tk.StringVar()

tk.Label(cust_tab, text="Name").grid(row=0, column=0)
tk.Entry(cust_tab, textvariable=cust_name_var).grid(row=0, column=1)
tk.Label(cust_tab, text="Contact").grid(row=1, column=0)
tk.Entry(cust_tab, textvariable=cust_contact_var).grid(row=1, column=1)
tk.Label(cust_tab, text="Address").grid(row=2, column=0)
tk.Entry(cust_tab, textvariable=cust_address_var).grid(row=2, column=1)
tk.Button(cust_tab, text="Add Customer", command=add_customer).grid(row=3, column=0, pady=5)
tk.Button(cust_tab, text="View Customers", command=view_customers).grid(row=3, column=1, pady=5)

cust_table = ttk.Treeview(cust_tab, columns=("ID","Name","Contact","Address"), show='headings')
for col in ("ID","Name","Contact","Address"):
    cust_table.heading(col, text=col)
cust_table.grid(row=4, column=0, columnspan=2, pady=10)

# -------- Transactions Tab --------
trans_tab = ttk.Frame(tab_control)
tab_control.add(trans_tab, text='Transactions')

trans_cust_id_var = tk.StringVar()
trans_emp_id_var = tk.StringVar()
trans_amount_var = tk.StringVar()
trans_type_var = tk.StringVar()
trans_date_var = tk.StringVar()

tk.Label(trans_tab, text="Customer ID").grid(row=0, column=0)
tk.Entry(trans_tab, textvariable=trans_cust_id_var).grid(row=0, column=1)
tk.Label(trans_tab, text="Employee ID").grid(row=1, column=0)
tk.Entry(trans_tab, textvariable=trans_emp_id_var).grid(row=1, column=1)
tk.Label(trans_tab, text="Amount").grid(row=2, column=0)
tk.Entry(trans_tab, textvariable=trans_amount_var).grid(row=2, column=1)
tk.Label(trans_tab, text="Transaction Type").grid(row=3, column=0)
tk.Entry(trans_tab, textvariable=trans_type_var).grid(row=3, column=1)
tk.Label(trans_tab, text="Date (YYYY-MM-DD)").grid(row=4, column=0)
tk.Entry(trans_tab, textvariable=trans_date_var).grid(row=4, column=1)
tk.Button(trans_tab, text="Add Transaction", command=add_transaction).grid(row=5, column=0, pady=5)
tk.Button(trans_tab, text="View Transactions", command=view_transactions).grid(row=5, column=1, pady=5)

trans_table = ttk.Treeview(trans_tab, columns=("ID","Customer ID","Employee ID","Amount","Type","Date"), show='headings')
for col in ("ID","Customer ID","Employee ID","Amount","Type","Date"):
    trans_table.heading(col, text=col)
trans_table.grid(row=6, column=0, columnspan=2, pady=10)

tab_control.pack(expand=1, fill='both')

root.mainloop()
