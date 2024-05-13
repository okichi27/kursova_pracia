import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("600x400")

        self.categories = ["groceries", "entertainment", "gifts", "travels", "clothes", 
                           "rent", "donation", "health", "savings", "other"]

        self.current_month = None
        self.current_year = None

        self.create_database()
        self.create_widgets()

    def create_database(self):
        self.conn = sqlite3.connect("expenses.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        amount REAL,
                        category TEXT,
                        date DATE,
                        comment TEXT
                        )""")
        self.conn.commit()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_combobox.get()  # Get the selected category from the combobox
        date = self.date_entry.get()
        comment = self.comment_entry.get()

        if not amount or not category or not date:
            messagebox.showwarning("Incomplete Information", "Please fill all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Invalid Amount", "Please enter a valid amount.")
            return

        self.c.execute("INSERT INTO expenses (amount, category, date, comment) VALUES (?, ?, ?, ?)",
                    (amount, category, date, comment))
        self.conn.commit()
        messagebox.showinfo("Expense Added", "Expense has been added successfully.")
        self.clear_entries()

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_combobox.set("")
        self.date_entry.delete(0, tk.END)
        self.comment_entry.delete(0, tk.END)

    def show_expenses(self):
        self.expenses_text.delete(1.0, tk.END)
        self.c.execute("SELECT SUM(amount) FROM expenses")
        total = self.c.fetchone()[0]
        self.expenses_text.insert(tk.END, f"Total Expenses: {total}\n\n")

        self.c.execute("SELECT * FROM expenses")
        expenses = self.c.fetchall()
        for expense in expenses:
            self.expenses_text.insert(tk.END, f"Amount: {expense[1]}, Category: {expense[2]}, Date: {expense[3]}, Comment: {expense[4]}\n")

    def show_monthly_chart(self):
        self.c.execute("SELECT strftime('%m', date) AS month, SUM(amount) FROM expenses GROUP BY month")
        data = self.c.fetchall()
        months = [row[0] for row in data]
        expenses = [row[1] for row in data]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(expenses, labels=months, autopct='%1.1f%%')
        ax.set_title('Monthly Expenses')

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_yearly_chart(self):
        self.c.execute("SELECT strftime('%Y', date) AS year, SUM(amount) FROM expenses GROUP BY year")
        data = self.c.fetchall()
        years = [row[0] for row in data]
        expenses = [row[1] for row in data]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(years, expenses)
        ax.set_title('Yearly Expenses')
        ax.set_xlabel('Year')
        ax.set_ylabel('Total Expenses')

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def create_widgets(self):
        title_label = tk.Label(self, text="Expense Tracker", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Adding Expense Section
        expense_frame = tk.Frame(self)
        expense_frame.pack(pady=10)

        amount_label = tk.Label(expense_frame, text="Amount:")
        amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(expense_frame)
        self.amount_entry.grid(row=0, column=1)

        category_label = tk.Label(expense_frame, text="Category:")
        category_label.grid(row=1, column=0)
        self.category_combobox = ttk.Combobox(expense_frame, values=self.categories)
        self.category_combobox.grid(row=1, column=1)

        date_label = tk.Label(expense_frame, text="Date (YYYY-MM-DD):")
        date_label.grid(row=2, column=0)
        self.date_entry = tk.Entry(expense_frame)
        self.date_entry.grid(row=2, column=1)

        comment_label = tk.Label(expense_frame, text="Comment:")
        comment_label.grid(row=3, column=0)
        self.comment_entry = tk.Entry(expense_frame)
        self.comment_entry.grid(row=3, column=1)

        add_button = tk.Button(expense_frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=4, columnspan=2, pady=5)

        # Show Expenses Section
        expenses_frame = tk.Frame(self)
        expenses_frame.pack(pady=10)

        show_expenses_button = tk.Button(expenses_frame, text="Show Expenses", command=self.show_expenses)
        show_expenses_button.pack(pady=5)

        self.expenses_text = scrolledtext.ScrolledText(expenses_frame, width=50, height=10)
        self.expenses_text.pack()

        # Visualization Section
        visualization_frame = tk.Frame(self)
        visualization_frame.pack(pady=10)

        monthly_chart_button = tk.Button(visualization_frame, text="Monthly Chart", command=self.show_monthly_chart)
        monthly_chart_button.grid(row=0, column=0, padx=10)

        yearly_chart_button = tk.Button(visualization_frame, text="Yearly Chart", command=self.show_yearly_chart)
        yearly_chart_button.grid(row=0, column=1, padx=10)


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()