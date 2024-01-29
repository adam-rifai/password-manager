from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

Font = ("Arial", 15, "normal")
json_path = "password.json"


# ----------------------------FUNCTIONS---------------------- #
def message_box():
    messagebox.showinfo(title=f"Item doesn't exist!",
                        message="There is no such name in your database")


def clear_window():
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    email_entry.delete(0, END)


def clear_dashboard():
    clear_window()


# ----------------------------FIND PASSWORD---------------- #
def find_password():
    target = website_entry.get().lower()
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except:
        message_box()

    else:
        if len(target) > 0:
            try:
                clear_window()
                website_entry.insert(0, target)
                email_entry.insert(0, data[target]["email"])
                password_entry.insert(0, data[target]["password"])
                website_password = password_entry.get()
                pyperclip.copy(website_password)
                messagebox.showinfo(title=target, message=f" {target.title()} exists more details on ""your dashboard ")
            except KeyError:
                message_box()


# -------------------- PASSWORD GENERATOR ----------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
               'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    # nr_letters = random.randint(8, 10)
    # nr_symbols = random.randint(2, 4)
    # nr_numbers = random.randint(2, 4)
    password_letters = [choice(letters) for _ in range(randint(8, 10))]

    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    y = len(password)
    messagebox.showinfo(title="Password length", message=f"your password is {y} character length")


# ----------------- SAVE PASSWORD ---------------------- #
def save_data():
    w = website_entry.get().lower()
    e = email_entry.get().lower()
    p = password_entry.get()
    new_data = {w: {"email": e, "password": p}}
    if len(w) < 1 or len(e) < 1 or len(p) < 1:
        messagebox.showinfo(title="Ops!", message="Please make sure there is no empty field!")
    else:
        try:
            with open(json_path, "r") as data_file:
                data = json.load(data_file)

        except:
            with open(json_path, "w") as data_file:
                # json.dump(new_data, data_file,indent=4)
                json.dump(new_data, data_file)
                # indent = 4 for example for indention

        else:
            is_save = messagebox.askokcancel(title="Save information?")
            if is_save:
                data.update(new_data)
                with open(json_path, "w") as data_file:
                    json.dump(data, data_file)
                    messagebox.showinfo(title="Successful", message="you data was stored "
                                                                    "Successfully")

        finally:
            clear_window()


window = Tk()
window.title("Password Manager")
# window.minsize(width=400, height=400)
window.resizable(False, False)
window.config(pady=50, padx=50)

# ---------------------------# CANVAS-------------------------------- #
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# --------------# WEBSITE LABELS AND ENTRIES----------------- #
website_label = Label(text="Website:", font=Font)
website_label.grid(row=1, column=0)
website_entry = Entry(width=21, font=Font)
website_entry.grid(row=1, column=1)
website_entry.focus()

# --------------- EMAIL LABEL AND ENTRIES.---------------- #
email_label = Label(text="Email/Username:", font=Font)
email_label.grid(row=2, column=0)
email_entry = Entry(width=21, font=Font)
email_entry.grid(row=2, column=1)
email_entry.insert(0, "example@gmail.com")

# -------------- PASSWORD LABEL AND ENTRIES.------------------ #
password_label = Label(text="Password:", font=Font)
password_label.grid(row=3, column=0)
password_entry = Entry(width=21, font=Font)
password_entry.grid(row=3, column=1)

# --------------------CREATE SPACE USING LABELS.---------------- #
space = Label(highlightthickness=0)
space.grid(row=3, column=2, pady=10)
space1 = Label(highlightthickness=0)
space1.grid(row=2, column=2, pady=10)
space2 = Label()
space2.grid(row=4, column=1, pady=10)

# ----------------------------BUTTONS ------------------------------- #
add_button = Button(text="Add", width=34, font=Font, fg="blue",
                    bg="#FFFF00", command=save_data)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", fg="blue", command=find_password,
                       font=("Arial", 11, "bold"), bg="#FFFF00", width=15)
search_button.grid(row=1, column=2)

generate_button = Button(text="Generate Password", fg="blue",
                         font=("Arial", 11, "bold"), width=15, bg="#FFFF00",
                         command=generate_password)
generate_button.grid(row=3, column=2)
clear_button = Button(text="Clear", font=("Arial", 11, "bold"), bg="#FFFF00",
                      width=15, fg="blue", command=clear_dashboard)
clear_button.grid(row=2, column=2)
window.mainloop()
