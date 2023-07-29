import tkinter as tk
from tkinter import *
from tkinter import font
import sqlite3
from PIL import Image, ImageTk


# Connect to the database
conn = sqlite3.connect('budget.db')
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT,
               password TEXT
            )
        ''')
conn.commit()
# Create purchases table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purchase TEXT,
        category TEXT,
        price INTEGER
    )
''')
conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS savings (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               amount INTEGER,
               category TEXT
    )
''')
conn.commit()


def budget_calulator():
    def calculate():
        ## Convert all the necessities to integers so that the calculations can be performed
        imonthly = int(monthly_salary_entry.get())
        ibills = int(bills_entry.get())
        iinsurance = int(insurance_entry.get())
        irent_mortgage = int(rent_mortgage_entry.get())
        icar_payment = int(car_payment_entry.get())
        # Calculations
        necessities = ibills + iinsurance + irent_mortgage + icar_payment
        spending_cash = imonthly - necessities
        totalSavings = (spending_cash / 2)
        totalInvestments = (totalSavings / 2) 
        totalSpending =  totalInvestments

        ## Output
        greeting_label = Label(calculator_window, text="This budget calculator splits your income 50|25|25 after paying off necessities", font=label_font, bg="yellow")
        greeting_label.pack()
        necessities_label = Label(calculator_window, text="Total amount of money spent on necessities: $" + str(necessities), font=label_font, bg="green")
        necessities_label.pack()
        budget_label = Label(calculator_window, text="Savings: $" + str(totalSavings) + "\n Investments: $" + str(totalInvestments) + "\n Spening: $" + str(totalSpending), font=label_font, bg="green") 
        budget_label.pack()
    label_font = font.Font(weight="bold")
    calculator_window = Toplevel(root)
    calculator_window.title("Budget Calculator")
    calculator_window.geometry("500x500")

    monthly_salary = Label(calculator_window, text="Monthly Salary: $")
    monthly_salary.pack()

    monthly_salary_entry = Entry(calculator_window)
    monthly_salary_entry.pack()
    
    car_payment = Label(calculator_window, text="Car Payment: $")
    car_payment.pack()
    
    car_payment_entry = Entry(calculator_window)
    car_payment_entry.pack()
    
    rent_mortgage = Label(calculator_window, text="Rent/Mortgage: $")
    rent_mortgage.pack()

    rent_mortgage_entry = Entry(calculator_window)
    rent_mortgage_entry.pack()
    
    insurance = Label(calculator_window, text="Insurance: $" )
    insurance.pack()
    
    insurance_entry = Entry(calculator_window)
    insurance_entry.pack()
    
    bills = Label(calculator_window, text="Bills: $")
    bills.pack()

    
    bills_entry = Entry(calculator_window)
    bills_entry.pack()

    calculate_button = Button(calculator_window, text="Calculate", command=calculate)
    calculate_button.pack()

    #def calculate():
    #   necessities = bills_entry + insurance_entry + rent_mortgage_entry + car_payment_entry 
    #    spending_cash = necessities - monthly_salary_entry
    #    spending_cash_label = Label(calculator_window, text="Total amount of money for spending/saving after necessities" + spending_cash)
    #   spending_cash_label.pack()
         

    

def sign_up():
    sign_up_window = Toplevel(root)
    sign_up_window.title("Add User")
    sign_up_window.geometry("300x150")

    # Savings amount label and entry
    username_label = Label(sign_up_window, text="Username: ")
    username_label.pack()

    username_entry = Entry(sign_up_window)
    username_entry.pack()

    # Savings category label and entry
    password_label = Label(sign_up_window, text="Password: ")
    password_label.pack()

    password_entry = Entry(sign_up_window)
    password_entry.pack()

    def save_user():
        # Get the entered amount and category
        username = username_entry.get()
        password = password_entry.get()

        # Insert the savings entry into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        # Close the add savings window
        sign_up_window.destroy()

    # Save button
    save_button = Button(sign_up_window, text="Save", command=save_user)
    save_button.pack() 


def login():
    username = username_entry.get()
    password = password_entry.get()
    
    cursor.execute('SELECT username FROM users')
    users = cursor.fetchall()

    cursor.execute('SELECT password FROM users')
    passwords = cursor.fetchall()

    authenticate_user = False
    
    for p in passwords:
        if p[0] == password:
            authenticate_user = True
            break 

    if authenticate_user:
        for u in users:
            if u[0] == username:
                authenticate_user = True
                break  # Exit the loop if username is found
            else:
                authenticate_user = False

    if authenticate_user:
        show_budgeting_interface()
    else:
        error_label = Label(root, text="Incorrect username/password")
        error_label.pack()

#____________________________________________________________________________________________________________________________________________________________________________#
def show_budgeting_interface(): ## Create window as well as design window geometry, color, etc.
    budgetting = Toplevel(root)
    budgetting.title("Budgeting APP")
    budgetting.configure(background="grey")
    budgetting.minsize(200, 200)
    budgetting.maxsize(750, 400)
    budgetting.geometry("500x400")

#____________________________________________________________________________________________________________________________________________________________________________#
# Setting up Purchases Frame
    purchase_frame = Frame(budgetting, width=300, height=400)
    purchase_frame.grid(row=0, column=0, padx=10, pady=10)
    purchase_listbox = Listbox(purchase_frame, width=50, height=5)
    purchase_listbox.grid(row=0, column=1, padx=10, pady=10)
    cursor.execute("SELECT purchase, category, price FROM purchases ORDER BY id DESC LIMIT 5")
    purchases = cursor.fetchall()
    for purchase in purchases:
        purchase_text = f"Purchase: {purchase[0]}, Category: {purchase[1]}, Price: ${purchase[2]}"
        purchase_listbox.insert(END, purchase_text)


    Label(purchase_frame, text="Spending").grid(row=0, column=0, padx=0, pady=0)

    # Add purchase button
    add_purchase = Button(purchase_frame, text="+", command=new_purchase)
    add_purchase.grid(row=1, column=0, padx=0, pady=0)


#_____________________________________________________________________________________________________________________________________________________________________________#

# Savings FRAME, Widget, Label, and Listbox 
    savings_frame = Frame(budgetting, width=300, height=400)
    savings_frame.grid(row=1, column=0, padx=10, pady=10)

    savings_listbox = Listbox(savings_frame, width=50, height=5)
    savings_listbox.grid(row=1, column=1, padx=10, pady=10)

    cursor.execute("SELECT amount, category FROM savings ORDER BY id DESC LIMIT 5")
    savings = cursor.fetchall()
    for saving in savings:
        saving_text = f"Saving: ${saving[0]} Category: {saving[1]}"
        savings_listbox.insert(END, saving_text)

    Label(savings_frame, text="Savings").grid(row=1, column=0, padx=0, pady=0)

    # Add savings button
    add_savings = Button(savings_frame, text="+", command=new_savings)
    add_savings.grid(row=2, column=0, padx=0, pady=0)

#_____________________________________________________________________________________________________________________________________________________________________________#

# Monthly Review button
    review_button = Button(budgetting, text="Monthly Review", command=MonthlyReview, height=3, width=20)
    review_button.grid(row=1, column=1, padx=10, pady=10)

    budgetCalculator_button = Button(budgetting, text="Budget Calculator", command=budget_calulator, height=3, width=20)
    budgetCalculator_button.grid(row=0, column=1, padx=10, pady=10)



def MonthlyReview():
    # Retrieve purchases from the database and display them
    cursor.execute("SELECT purchase, category, price FROM purchases")
    purchases = cursor.fetchall()

    cursor.execute("SELECT amount FROM savings")
    savings = cursor.fetchall()
    savings_total = sum(amount[0] for amount in savings)
    strSavings_total = str(savings_total)
    # Create a new window for the monthly review
    review_window = Toplevel(root)
    review_window.title("Monthly Review")
    review_window.geometry("300x300")

    
    category_totals = {}

    # Iterate over the purchases and calculate the category totals
    for purchase in purchases:
        category = purchase[1]
        price = purchase[2]
        
        # Add the price to the category total
        if category in category_totals:
            category_totals[category] += price
        else:
            category_totals[category] = price

    # Display the purchases and category totals in the new window
    for category, total in category_totals.items():
        category_label = Label(review_window, text="Category: " + category)
        category_label.pack()

        total_label = Label(review_window, text="Total Price: $" + str(total))
        total_label.pack()

        separator = Label(review_window, text="-----------------------------")
        separator.pack()
        
    savings_label = Label(review_window, text="Total amount saved: $" + strSavings_total)
    savings_label.pack()
   
def new_savings():
    # Create a new window for adding savings
    add_savings_window = Toplevel(root)
    add_savings_window.title("Add Savings")
    add_savings_window.geometry("300x150")

    # Savings amount label and entry
    amount_label = Label(add_savings_window, text="Amount:")
    amount_label.pack()

    amount_entry = Entry(add_savings_window)
    amount_entry.pack()

    # Savings category label and entry
    category_label = Label(add_savings_window, text="Category:")
    category_label.pack()

    category_entry = Entry(add_savings_window)
    category_entry.pack()

    def save_savings():
        # Get the entered amount and category
        amount = int(amount_entry.get())
        category = category_entry.get()

        # Insert the savings entry into the database
        cursor.execute("INSERT INTO savings (amount, category) VALUES (?, ?)", (amount, category))
        conn.commit()

        # Close the add savings window
        add_savings_window.destroy()

    # Save button
    save_button = Button(add_savings_window, text="Save", command=save_savings)
    save_button.pack() 

def new_purchase():
    add_purchase_window = Toplevel(root)
    add_purchase_window.title("Add Purchase")
    add_purchase_window.geometry("300x150")

    purchase_label = Label(add_purchase_window, text="What was purchased: ")
    purchase_label.pack()

    purchase_entry = Entry(add_purchase_window)
    purchase_entry.pack()

    category_label = Label(add_purchase_window, text="Category: ")
    category_label.pack()

    category_entry = Entry(add_purchase_window)
    category_entry.pack()

    price_label = Label(add_purchase_window, text="Price: ")
    price_label.pack()

    price_entry = Entry(add_purchase_window)
    price_entry.pack()

    def save_purchase():
        newPurchase = purchase_entry.get()
        newCategory = category_entry.get()
        newPrice = price_entry.get()

        cursor.execute("INSERT INTO purchases (purchase, category, price) VALUES (?, ?, ?)", (newPurchase, newCategory, newPrice))
        conn.commit()

        add_purchase_window.destroy()

    save_button = Button(add_purchase_window, text="Save", command=save_purchase)
    save_button.pack()

#____________________________________________________________________________________________________________________________________________________________________________#

#MAIN LOGIN/SIGNUP SCREEN
root = Tk()
root.title("Login")
root.geometry("600x500")
root.configure(background="white")

# Load the image
image = Image.open("/home/jacksonperez/Projects/pythonProjects/budgetapp/template.jpg")
background_image = ImageTk.PhotoImage(image)

# Create a Canvas widget
canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.pack()

# Set the background image
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
# Create and position the username label and entry field
username_label = Label(root, text="Username:")
username_label.pack()
username_entry = Entry(root)
username_entry.pack()

# Create and position the password label and entry field
password_label = Label(root, text="Password:")
password_label.pack()
password_entry = Entry(root, show="*")  # Show asterisks instead of actual characters
password_entry.pack()

# Create and position the login button
login_button = Button(root, text="Login", command=login)
login_button.pack()

signup_button = Button(root, text="Sign Up", command=sign_up)
signup_button.pack()

root.mainloop()


