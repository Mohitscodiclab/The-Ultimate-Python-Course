import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import os
import pywhatkit  # pip install pywhatkit

#############################################
# Initialize Database and Create Tables
#############################################
def init_db():
    conn = sqlite3.connect("hindustan_beez_bhandar.db")
    cur = conn.cursor()
    # Customers table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            father_name TEXT,
            address TEXT,
            credit REAL DEFAULT 0
        )
    ''')
    # Stocks table (added "unit" column for measurement units)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_name TEXT NOT NULL,
            quantity INTEGER DEFAULT 0,
            cost_price REAL,
            selling_price REAL,
            unit TEXT
        )
    ''')
    # Invoices table – invoice header
    cur.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            date_time TEXT,
            total_amount REAL,
            payment_received REAL,
            credit_amount REAL,
            gst_applied INTEGER,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    ''')
    # Invoice items table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            stock_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY(invoice_id) REFERENCES invoices(id),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
        )
    ''')
    conn.commit()
    return conn, cur

conn, cur = init_db()

#############################################
# Global Lists & Helper Update Functions
#############################################
customer_names = []  # list of customer names
customer_dict = {}   # mapping of customer name to id

stock_names = []     # list of stock names (for invoice selection)
stock_dict = {}      # mapping of stock name to (id, selling_price)

def update_customer_list():
    global customer_names, customer_dict
    customer_names.clear()
    customer_dict.clear()
    for row in cur.execute("SELECT id, name FROM customers"):
        customer_names.append(row[1])
        customer_dict[row[1]] = row[0]
    combo_customers['values'] = customer_names

def update_stock_list():
    global stock_names, stock_dict
    stock_names.clear()
    stock_dict.clear()
    for row in cur.execute("SELECT id, stock_name, selling_price FROM stocks"):
        stock_names.append(row[1])
        stock_dict[row[1]] = (row[0], row[2])
    combo_stock['values'] = stock_names

#############################################
# Main Application Window Setup
#############################################
root = tk.Tk()
root.title("Hindustan Beez Bhandar - Management System")
root.geometry("1024x768")

notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill='both')

# Four Tabs: Customers, Stock, Invoice, Reports
tab_customers = ttk.Frame(notebook)
notebook.add(tab_customers, text="Customers")

tab_stocks = ttk.Frame(notebook)
notebook.add(tab_stocks, text="Stock Management")

tab_invoices = ttk.Frame(notebook)
notebook.add(tab_invoices, text="Invoice Management")

tab_reports = ttk.Frame(notebook)
notebook.add(tab_reports, text="Reports")

#############################################
# Tab 1 - Customer Management
#############################################
lbl_title = ttk.Label(tab_customers, text="Add New Customer", font=("Helvetica", 16))
lbl_title.pack(pady=10)

frame_form = ttk.Frame(tab_customers)
frame_form.pack(pady=10)

ttk.Label(frame_form, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_name = ttk.Entry(frame_form, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_form, text="Phone:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_phone = ttk.Entry(frame_form, width=30)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_form, text="Father's Name:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entry_father = ttk.Entry(frame_form, width=30)
entry_father.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_form, text="Address:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
entry_address = ttk.Entry(frame_form, width=30)
entry_address.grid(row=3, column=1, padx=5, pady=5)

def add_customer():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    father = entry_father.get().strip()
    address = entry_address.get().strip()
    if not name or not phone:
        messagebox.showerror("Error", "Name and Phone are required")
        return
    cur.execute("INSERT INTO customers (name, phone, father_name, address) VALUES (?, ?, ?, ?)",
                (name, phone, father, address))
    conn.commit()
    messagebox.showinfo("Success", f"Customer {name} added!")
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_father.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    load_customers()
    update_customer_list()  # refresh invoice tab customer list

btn_add_customer = ttk.Button(frame_form, text="Add Customer", command=add_customer)
btn_add_customer.grid(row=4, column=0, columnspan=2, pady=10)

separator = ttk.Separator(tab_customers, orient='horizontal')
separator.pack(fill='x', pady=10)

frame_search = ttk.Frame(tab_customers)
frame_search.pack(pady=10)

ttk.Label(frame_search, text="Search:").grid(row=0, column=0, padx=5)
entry_search = ttk.Entry(frame_search, width=40)
entry_search.grid(row=0, column=1, padx=5)

def search_customers():
    search_term = entry_search.get().strip()
    for row in tree_customers.get_children():
        tree_customers.delete(row)
    query = """
        SELECT id, name, phone, father_name, address, credit 
        FROM customers 
        WHERE name LIKE ? OR phone LIKE ? OR father_name LIKE ? OR address LIKE ?
    """
    term = "%" + search_term + "%"
    for row in cur.execute(query, (term, term, term, term)):
        tree_customers.insert("", tk.END, values=row)

btn_search = ttk.Button(frame_search, text="Search", command=search_customers)
btn_search.grid(row=0, column=2, padx=5)

columns = ("ID", "Name", "Phone", "Father", "Address", "Credit")
tree_customers = ttk.Treeview(tab_customers, columns=columns, show="headings")
for col in columns:
    tree_customers.heading(col, text=col)
tree_customers.pack(pady=10, fill='x')

def load_customers():
    for row in tree_customers.get_children():
        tree_customers.delete(row)
    for row in cur.execute("SELECT id, name, phone, father_name, address, credit FROM customers"):
        tree_customers.insert("", tk.END, values=row)

load_customers()

#############################################
# Tab 2 - Stock Management
#############################################
ttk.Label(tab_stocks, text="Add New Stock Item", font=("Helvetica", 16)).pack(pady=10)

frame_stock = ttk.Frame(tab_stocks)
frame_stock.pack(pady=10)

ttk.Label(frame_stock, text="Stock Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_stock_name = ttk.Entry(frame_stock, width=30)
entry_stock_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_stock, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_quantity = ttk.Entry(frame_stock, width=30)
entry_quantity.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_stock, text="Cost Price:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_cost_price = ttk.Entry(frame_stock, width=30)
entry_cost_price.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_stock, text="Selling Price:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_selling_price = ttk.Entry(frame_stock, width=30)
entry_selling_price.grid(row=3, column=1, padx=5, pady=5)

# New dropdown for selecting measurement unit
ttk.Label(frame_stock, text="Unit:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
unit_options = ["pack", "bag", "litre", "ml", "box", "pc", "dozen", "kg", "gm", "unit"]
combo_unit = ttk.Combobox(frame_stock, values=unit_options, width=28)
combo_unit.grid(row=4, column=1, padx=5, pady=5)
combo_unit.set("pack")  # default value

def add_stock():
    stock_name = entry_stock_name.get().strip()
    quantity = entry_quantity.get().strip()
    cost = entry_cost_price.get().strip()
    selling = entry_selling_price.get().strip()
    unit_val = combo_unit.get().strip()
    if not stock_name or not quantity or not selling:
        messagebox.showerror("Error", "Stock name, quantity and selling price are required")
        return
    try:
        quantity_val = int(quantity)
        cost_val = float(cost) if cost else 0.0
        selling_val = float(selling)
    except ValueError:
        messagebox.showerror("Error", "Enter valid numeric values")
        return
    cur.execute("INSERT INTO stocks (stock_name, quantity, cost_price, selling_price, unit) VALUES (?, ?, ?, ?, ?)",
                (stock_name, quantity_val, cost_val, selling_val, unit_val))
    conn.commit()
    messagebox.showinfo("Success", f"Stock {stock_name} added!")
    entry_stock_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_cost_price.delete(0, tk.END)
    entry_selling_price.delete(0, tk.END)
    combo_unit.set("pack")
    load_stocks()
    update_stock_list()  # refresh invoice tab stock list

btn_add_stock = ttk.Button(frame_stock, text="Add Stock", command=add_stock)
btn_add_stock.grid(row=5, column=0, columnspan=2, pady=10)

# Update the columns to include Unit
columns_stock = ("ID", "Stock Name", "Quantity", "Cost Price", "Selling Price", "Unit")
tree_stocks = ttk.Treeview(tab_stocks, columns=columns_stock, show="headings")
for col in columns_stock:
    tree_stocks.heading(col, text=col)
tree_stocks.pack(pady=10, fill='x')

def load_stocks():
    for row in tree_stocks.get_children():
        tree_stocks.delete(row)
    query = "SELECT id, stock_name, quantity, cost_price, selling_price, unit FROM stocks"
    for row in cur.execute(query):
        tree_stocks.insert("", tk.END, values=row)

load_stocks()

#############################################
# Tab 3 - Invoice Management
#############################################
# Top frame for customer selection, payment, GST, and totals.
frame_invoice_top = ttk.Frame(tab_invoices)
frame_invoice_top.pack(pady=10, fill='x')

ttk.Label(frame_invoice_top, text="Select Customer:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
combo_customers = ttk.Combobox(frame_invoice_top, values=customer_names, width=30)
combo_customers.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_invoice_top, text="Payment Received:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_payment = ttk.Entry(frame_invoice_top, width=30)
entry_payment.grid(row=1, column=1, padx=5, pady=5)

gst_var = tk.BooleanVar()
chk_gst = ttk.Checkbutton(frame_invoice_top, text="Apply GST (18%)", variable=gst_var)
chk_gst.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

total_bill_var = tk.DoubleVar(value=0.0)
credit_var = tk.DoubleVar(value=0.0)
ttk.Label(frame_invoice_top, text="Total Bill:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
lbl_total_bill = ttk.Label(frame_invoice_top, textvariable=total_bill_var)
lbl_total_bill.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
ttk.Label(frame_invoice_top, text="Credit:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
lbl_credit = ttk.Label(frame_invoice_top, textvariable=credit_var)
lbl_credit.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

# -----------------------------
# Customer Details Section
# -----------------------------
frame_customer_details = ttk.Frame(tab_invoices)
frame_customer_details.pack(pady=10, fill='x')

ttk.Label(frame_customer_details, text="Father's Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
label_father_val = ttk.Label(frame_customer_details, text="---")
label_father_val.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_customer_details, text="Address:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
label_address_val = ttk.Label(frame_customer_details, text="---")
label_address_val.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(frame_customer_details, text="Mobile:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
label_phone_val = ttk.Label(frame_customer_details, text="---")
label_phone_val.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_customer_details, text="Total Paid:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
label_total_paid_val = ttk.Label(frame_customer_details, text="0.0")
label_total_paid_val.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(frame_customer_details, text="Total Credit:").grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
label_credit_val = ttk.Label(frame_customer_details, text="0.0")
label_credit_val.grid(row=1, column=5, padx=5, pady=5)

# Function to load customer details into the invoice section upon selection
def fill_customer_details(event):
    cust_name = combo_customers.get().strip()
    if cust_name in customer_dict:
        cust_id = customer_dict[cust_name]
        cur.execute("SELECT father_name, address, phone, credit FROM customers WHERE id = ?", (cust_id,))
        row = cur.fetchone()
        if row:
            father_name, address, phone, credit = row
            label_father_val.config(text=father_name if father_name else "---")
            label_address_val.config(text=address if address else "---")
            label_phone_val.config(text=phone)
            label_credit_val.config(text=str(credit))
        cur.execute("SELECT SUM(payment_received) FROM invoices WHERE customer_id = ?", (cust_id,))
        total_paid = cur.fetchone()[0]
        label_total_paid_val.config(text=str(total_paid if total_paid else 0.0))

combo_customers.bind("<<ComboboxSelected>>", fill_customer_details)

# -----------------------------
# Invoice Items Section
# -----------------------------
frame_add_item = ttk.Frame(tab_invoices)
frame_add_item.pack(pady=10, fill='x')

ttk.Label(frame_add_item, text="Select Stock Item:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
combo_stock = ttk.Combobox(frame_add_item, values=stock_names, width=30)
combo_stock.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_add_item, text="Quantity:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
entry_item_quantity = ttk.Entry(frame_add_item, width=10)
entry_item_quantity.grid(row=0, column=3, padx=5, pady=5)

btn_add_item = ttk.Button(frame_add_item, text="Add Item")
btn_add_item.grid(row=0, column=4, padx=5, pady=5)

columns_inv_items = ("Stock ID", "Stock Name", "Quantity", "Unit Price", "Total Price")
tree_inv_items = ttk.Treeview(tab_invoices, columns=columns_inv_items, show="headings")
for col in columns_inv_items:
    tree_inv_items.heading(col, text=col)
tree_inv_items.pack(pady=10, fill='x')

invoice_items = []  # buffer for current invoice

def add_invoice_item():
    stock_name = combo_stock.get().strip()
    qty = entry_item_quantity.get().strip()
    if not stock_name or not qty:
        messagebox.showerror("Error", "Please select a stock item and specify quantity.")
        return
    try:
        qty_val = int(qty)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid quantity")
        return
    if stock_name not in stock_dict:
        messagebox.showerror("Error", "Stock item not found.")
        return
    stock_id, unit_price = stock_dict[stock_name]
    total_price = qty_val * unit_price
    invoice_items.append({
        "stock_id": stock_id,
        "stock_name": stock_name,
        "quantity": qty_val,
        "unit_price": unit_price,
        "total_price": total_price
    })
    tree_inv_items.insert("", tk.END, values=(stock_id, stock_name, qty_val, unit_price, total_price))
    total_bill_var.set(total_bill_var.get() + total_price)
    combo_stock.set('')
    entry_item_quantity.delete(0, tk.END)

btn_add_item.config(command=add_invoice_item)

def create_invoice():
    customer_name = combo_customers.get().strip()
    payment_received_str = entry_payment.get().strip()
    if not customer_name:
        messagebox.showerror("Error", "Please select a customer.")
        return
    try:
        payment_received = float(payment_received_str) if payment_received_str else 0.0
    except ValueError:
        messagebox.showerror("Error", "Enter a valid payment amount")
        return

    customer_id = customer_dict.get(customer_name)
    if not customer_id:
        messagebox.showerror("Error", "Customer not found.")
        return

    total_bill_raw = total_bill_var.get()
    if gst_var.get():
        gst_amount = total_bill_raw * 0.18
        total_bill_final = total_bill_raw + gst_amount
    else:
        total_bill_final = total_bill_raw
    credit = total_bill_final - payment_received
    credit_var.set(credit)

    dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO invoices (customer_id, date_time, total_amount, payment_received, credit_amount, gst_applied)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, dt_str, total_bill_final, payment_received, credit, int(gst_var.get())))
    invoice_id = cur.lastrowid

    for item in invoice_items:
        cur.execute("INSERT INTO invoice_items (invoice_id, stock_id, quantity, price) VALUES (?, ?, ?, ?)",
                    (invoice_id, item["stock_id"], item["quantity"], item["unit_price"]))
        cur.execute("UPDATE stocks SET quantity = quantity - ? WHERE id = ?",
                    (item["quantity"], item["stock_id"]))
    conn.commit()

    cur.execute("UPDATE customers SET credit = credit + ? WHERE id = ?", (credit, customer_id))
    conn.commit()

    invoice_text = []
    invoice_text.append("Hindustan Beez Bhandar")
    invoice_text.append("Invoice Number: {}".format(invoice_id))
    invoice_text.append("Date & Time: {}".format(dt_str))
    invoice_text.append("\nCustomer Details:")
    invoice_text.append("Name: {}".format(customer_name))
    invoice_text.append("Father's Name: {}".format(label_father_val.cget("text")))
    invoice_text.append("Address: {}".format(label_address_val.cget("text")))
    invoice_text.append("Mobile: {}".format(label_phone_val.cget("text")))
    invoice_text.append("Total Paid: {}".format(label_total_paid_val.cget("text")))
    invoice_text.append("Total Credit: {}".format(label_credit_val.cget("text")))
    invoice_text.append("-" * 40)
    invoice_text.append("{:<10} {:<20} {:<10} {:<10}".format("Stock ID", "Item", "Qty", "Price"))
    for item in invoice_items:
        invoice_text.append("{:<10} {:<20} {:<10} {:<10}".format(item["stock_id"], item["stock_name"],
                                                                 item["quantity"], item["unit_price"]))
    invoice_text.append("-" * 40)
    invoice_text.append("Total Bill: {}".format(total_bill_final))
    invoice_text.append("Payment Received: {}".format(payment_received))
    invoice_text.append("Credit: {}".format(credit))
    full_invoice = "\n".join(invoice_text)

    folder = filedialog.askdirectory(title="Select Folder to Save Invoice")
    if folder:
        invoice_filename = os.path.join(folder, f"Invoice_{invoice_id}.txt")
        with open(invoice_filename, "w") as f:
            f.write(full_invoice)
    
    cur.execute("SELECT phone FROM customers WHERE id = ?", (customer_id,))
    phone_row = cur.fetchone()
    if phone_row:
        phone_no = phone_row[0]
        try:
            pywhatkit.sendwhatmsg_instantly(phone_no, full_invoice, wait_time=10, tab_close=True)
            messagebox.showinfo("WhatsApp Message", "Invoice sent via WhatsApp!")
        except Exception as e:
            messagebox.showerror("WhatsApp Error", f"Error sending invoice: {e}")

    messagebox.showinfo("Invoice Created", f"Invoice {invoice_id} created successfully!")
    invoice_items.clear()
    for row in tree_inv_items.get_children():
        tree_inv_items.delete(row)
    combo_customers.set('')
    entry_payment.delete(0, tk.END)
    total_bill_var.set(0.0)
    credit_var.set(0.0)
    update_stock_list()

btn_create_invoice = ttk.Button(tab_invoices, text="Create Invoice", command=create_invoice)
btn_create_invoice.pack(pady=10)

#############################################
# Tab 4 - Reports & Extra Features
#############################################
frame_reports = ttk.Frame(tab_reports)
frame_reports.pack(pady=20)

def generate_daily_sales_report():
    today_str = datetime.now().strftime("%Y-%m-%d")
    query = """
       SELECT id, date_time, total_amount, payment_received, credit_amount 
       FROM invoices 
       WHERE date_time LIKE ?
    """
    report_data = cur.execute(query, (today_str + "%",)).fetchall()
    report_text = f"Daily Sales Report for {today_str}\n" 
    report_text += "-" * 40 + "\n"
    for row in report_data:
        report_text += (f"Invoice ID: {row[0]}, Time: {row[1]}, Total: {row[2]}, "
                        f"Payment: {row[3]}, Credit: {row[4]}\n")
    report_window = tk.Toplevel(root)
    report_window.title("Daily Sales Report")
    text_widget = tk.Text(report_window, width=80, height=20)
    text_widget.pack()
    text_widget.insert(tk.END, report_text)
    text_widget.config(state=tk.DISABLED)

def generate_stock_report():
    query = "SELECT id, stock_name, quantity, cost_price, selling_price, unit FROM stocks"
    report_data = cur.execute(query).fetchall()
    report_text = "Stock Report:\n" + "-" * 40 + "\n"
    for row in report_data:
        report_text += (f"Stock ID: {row[0]}, Name: {row[1]}, Quantity: {row[2]}, "
                        f"Cost Price: {row[3]}, Selling Price: {row[4]}, Unit: {row[5]}\n")
    report_window = tk.Toplevel(root)
    report_window.title("Stock Report")
    text_widget = tk.Text(report_window, width=80, height=20)
    text_widget.pack()
    text_widget.insert(tk.END, report_text)
    text_widget.config(state=tk.DISABLED)

btn_daily_report = ttk.Button(frame_reports, text="Daily Sales Report", command=generate_daily_sales_report)
btn_daily_report.pack(pady=10)

btn_stock_report = ttk.Button(frame_reports, text="Stock Report", command=generate_stock_report)
btn_stock_report.pack(pady=10)

def backup_database():
    backup_file = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite DB", "*.db")])
    if backup_file:
        backup_conn = sqlite3.connect(backup_file)
        conn.backup(backup_conn)
        backup_conn.close()
        messagebox.showinfo("Backup", f"Database backup saved to {backup_file}")

btn_backup = ttk.Button(frame_reports, text="Backup Database", command=backup_database)
btn_backup.pack(pady=10)

#############################################
# Initial Update for Invoice Tab Selections
#############################################
update_customer_list()
update_stock_list()

#############################################
# Run the Application
#############################################
root.mainloop()
