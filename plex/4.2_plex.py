import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("800x600")

        self.categories = ["groceries", "entertainment", "gifts", "travels", "clothes", 
                           "rent", "donation", "health", "savings", "other"]

        self.months = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
                       "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]

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
        category = self.category_combobox.get()
        day = self.day_combobox.get()
        month = self.month_combobox.get()
        year = self.year_combobox.get()
        comment = self.comment_entry.get()

        if not amount or not category or not day or not month or not year:
            messagebox.showwarning("Incomplete Information", "Please fill all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Invalid Amount", "Please enter a valid amount.")
            return

        date = f"{year}-{self.months.index(month) + 1:02d}-{int(day):02d}"

        self.c.execute("INSERT INTO expenses (amount, category, date, comment) VALUES (?, ?, ?, ?)",
                    (amount, category, date, comment))
        self.conn.commit()
        messagebox.showinfo("Expense Added", "Expense has been added successfully.")
        self.clear_entries()
        self.update_total_expenses()

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_combobox.set("")
        self.day_combobox.set("")
        self.month_combobox.set("")
        self.year_combobox.set("")
        self.comment_entry.delete(0, tk.END)

    def update_total_expenses(self):
        self.c.execute("SELECT SUM(amount) FROM expenses")
        total = self.c.fetchone()[0]
        self.total_expenses_label.config(text=f"Total Expenses: {total}")

    def show_expenses(self):
        self.expenses_text.delete(1.0, tk.END)
        self.c.execute("SELECT * FROM expenses ORDER BY date DESC")
        expenses = self.c.fetchall()
        for expense in expenses:
            self.expenses_text.insert(tk.END, f"Date: {expense[3]}, Amount: {expense[1]}, Category: {expense[2]}, Comment: {expense[4]}\n")

    def show_monthly_chart(self):
        if self.monthly_chart_frame.winfo_ismapped():
            self.monthly_chart_frame.pack_forget()
        else:
            self.monthly_chart_frame.pack()
            self.c.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%m', date) = (SELECT strftime('%m', date) FROM expenses ORDER BY date DESC LIMIT 1) GROUP BY category")
            data = self.c.fetchall()
            categories = [row[0] for row in data]
            expenses = [row[1] for row in data]

            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(expenses, labels=categories, autopct='%1.1f%%')
            ax.set_title('Monthly Expenses by Category')

            canvas = FigureCanvasTkAgg(fig, master=self.monthly_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def show_yearly_chart(self):
        if self.yearly_chart_frame.winfo_ismapped():
            self.yearly_chart_frame.pack_forget()
        else:
            self.yearly_chart_frame.pack()
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

            canvas = FigureCanvasTkAgg(fig, master=self.yearly_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def update_days(self, *args):
        month = self.month_combobox.get()
        year = self.year_combobox.get()
        if month and year:
            month_index = self.months.index(month) + 1
            year = int(year)
            days_in_month = calendar.monthrange(year, month_index)[1]
            self.day_combobox['values'] = list(range(1, days_in_month + 1))
            self.day_combobox.set('')

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

        date_label = tk.Label(expense_frame, text="Date:")
        date_label.grid(row=2, column=0)

        self.day_combobox = ttk.Combobox(expense_frame, width=5)
        self.day_combobox.grid(row=2, column=1, sticky='w')

        self.month_combobox = ttk.Combobox(expense_frame, values=self.months, width=10)
        self.month_combobox.grid(row=2, column=1)

        self.year_combobox = ttk.Combobox(expense_frame, values=list(range(2000, 2101)), width=5)
        self.year_combobox.grid(row=2, column=1, sticky='e')

        self.month_combobox.bind("<<ComboboxSelected>>", self.update_days)
        self.year_combobox.bind("<<ComboboxSelected>>", self.update_days)

        comment_label = tk.Label(expense_frame, text="Comment:")
        comment_label.grid(row=3, column=0)
        self.comment_entry = tk.Entry(expense_frame)
        self.comment_entry.grid(row=3, column=1)

        add_button = tk.Button(expense_frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=4, columnspan=2, pady=5)

        # Total Expenses
        self.total_expenses_label = tk.Label(self, text="Total Expenses: 0")
        self.total_expenses_label.pack()

        # Show Expenses Section
        expenses_frame = tk.Frame(self)
        expenses_frame.pack(pady=10)

        show_expenses_button = tk.Button(expenses_frame, text="Show Expenses", command=self.show_expenses)
        show_expenses_button.pack(pady=5)

        self.expenses_text = scrolledtext.ScrolledText(expenses_frame, width=50, height=10)
        self.expenses_text.pack()

        # Monthly Chart Section
        self.monthly_chart_frame = tk.Frame(self)
        monthly_chart_button = tk.Button(self, text="Monthly Chart", command=self.show_monthly_chart)
        monthly_chart_button.pack(pady=5)

        # Yearly Chart Section
        self.yearly_chart_frame = tk.Frame(self)
        yearly_chart_button = tk.Button(self, text="Yearly Chart", command=self.show_yearly_chart)
        yearly_chart_button.pack(pady=5)

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()