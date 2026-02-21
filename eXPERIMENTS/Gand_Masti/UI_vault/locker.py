import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import time

from core.config_manager import config_exists, load_config
from core.auth import *
from core.vault_handler import *

AUTO_LOCK = 30

last_activity = time.time()
vault_open = False
current_password = None


# ---------------- ACTIVITY TRACKING ---------------- #

def update_activity(event=None):
    global last_activity
    last_activity = time.time()


# ---------------- SAFE LOCK FUNCTION ---------------- #

def force_lock():
    global vault_open

    if vault_open and current_password:
        try:
            lock_vault(current_password)
        except:
            pass

        vault_open = False


# ---------------- AUTO LOCK THREAD ---------------- #

def auto_lock_worker():
    global vault_open

    while True:
        time.sleep(1)

        if vault_open and (time.time() - last_activity > AUTO_LOCK):
            root.after(0, auto_lock_ui)


def auto_lock_ui():
    force_lock()
    messagebox.showwarning("Auto Lock", "Vault locked due to inactivity")
    show_main()


# ---------------- FIRST SETUP ---------------- #

def first_time_setup():
    while True:
        pw = simpledialog.askstring("Setup", "Create Password", show="*")
        cpw = simpledialog.askstring("Setup", "Confirm Password", show="*")

        if pw and pw == cpw:
            break

        messagebox.showerror("Error", "Passwords do not match")

    q = simpledialog.askstring("Recovery", "Security Question")
    a = simpledialog.askstring("Recovery", "Answer")

    setup_credentials(pw, q, a)
    ensure_vault()

    open_vault(pw)


# ---------------- VAULT CONTROL ---------------- #

def open_vault(pw):
    global vault_open, current_password

    unlock_vault(pw)

    vault_open = True
    current_password = pw
    update_activity()

    show_vault()


def lock_now():
    force_lock()
    show_main()


# ---------------- FLOWS ---------------- #

def unlock_flow():
    pw = simpledialog.askstring("Unlock", "Enter Password", show="*")

    if verify_password(pw):
        open_vault(pw)
    else:
        messagebox.showerror("Error", "Wrong password")


def forgot_password():
    config = load_config()

    ans = simpledialog.askstring("Recovery", config["question"])

    if verify_answer(ans):

        new_pw = simpledialog.askstring("Reset", "New Password", show="*")
        reset_password(new_pw)

        if messagebox.askyesno("Change", "Change recovery question?"):
            q = simpledialog.askstring("New", "New Question")
            a = simpledialog.askstring("New", "New Answer")
            update_recovery(q, a)

        messagebox.showinfo("Success", "Password reset complete")

    else:
        messagebox.showerror("Error", "Wrong answer")


# ---------------- UI ---------------- #

def clear():
    for w in root.winfo_children():
        w.destroy()


def show_main():
    clear()

    tk.Button(root, text="Unlock Folder", width=25, command=unlock_flow).pack(pady=10)
    tk.Button(root, text="Forget Password", width=25, command=forgot_password).pack(pady=10)
    tk.Button(root, text="Exit", width=25, command=on_exit).pack(pady=10)


def show_vault():
    clear()

    tk.Label(root, text="Vault Open").pack(pady=10)
    tk.Button(root, text="Lock Now", command=lock_now).pack(pady=10)


# ---------------- EXIT HANDLER (CRITICAL FIX) ---------------- #

def on_exit():
    force_lock()
    root.destroy()


# ---------------- APP INIT ---------------- #

root = tk.Tk()
root.title("Secure Vault")
root.geometry("320x240")

root.bind_all("<Key>", update_activity)
root.bind_all("<Motion>", update_activity)

root.protocol("WM_DELETE_WINDOW", on_exit)

threading.Thread(target=auto_lock_worker, daemon=True).start()

ensure_vault()

if not config_exists():
    first_time_setup()
else:
    show_main()

root.mainloop()