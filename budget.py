import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("okichi`s-production")
        self.geometry("900x900")

        self.categories = ["продукти", "розваги", "житло", "подорожі", "одяг", 
                            "донати <3", "здоров'я","подарунки", "заощадження", "інше"]

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
        selected_date = self.date_entry.get_date()
        comment = self.comment_entry.get()

        if not amount or not category or not selected_date:
            messagebox.showwarning("Неповна інформація", "Будь ласка, заповніть всі поля.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Неправильна сума", "Будь ласка, введіть ще раз.")
            return

        year = selected_date.strftime('%Y')
        month = selected_date.strftime('%m')
        day = selected_date.strftime('%d')
        date = f"{year}-{month}-{day}"

        self.c.execute("INSERT INTO expenses (amount, category, date, comment) VALUES (?, ?, ?, ?)",
                       (amount, category, date, comment))
        self.conn.commit()
        messagebox.showinfo("Витрату додано!", "Вашу витрату успішно додано до історії.")
        self.clear_entries()
        self.update_total_expenses()

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_combobox.set("")
        self.date_entry.set_date(None)
        self.comment_entry.delete(0, tk.END)

    def update_total_expenses(self):
        self.c.execute("SELECT SUM(amount) FROM expenses")
        total = float(self.c.fetchone()[0])
        self.total_expenses_label.config(text=f"Cума витрат за сесію: {total}")

    def show_expenses(self):
        self.expenses_text.delete(1.0, tk.END)
        self.c.execute("SELECT * FROM expenses ORDER BY date DESC")
        expenses = self.c.fetchall()
        for expense in expenses:
            self.expenses_text.insert(tk.END, f"[{expense[3][8:10]}-{expense[3][5:7]}-{expense[3][0:4]}]  Сума: {expense[1]} грн     Категорія - {expense[2]}     КОМЕНТАР: {expense[4]}\n")

    def show_monthly_chart(self):
        if self.monthly_chart_frame.winfo_ismapped():
            # Видалення попереднього графіка
            for widget in self.monthly_chart_frame.winfo_children():
                widget.destroy()
        else:
            self.monthly_chart_frame.pack()

        if self.monthly_chart_frame.winfo_ismapped():
            self.monthly_chart_frame.pack_forget()
        else:
            self.monthly_chart_frame.pack()
            self.c.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%m', date) = (SELECT strftime('%m', date) FROM expenses ORDER BY date DESC LIMIT 1) AND strftime('%Y', date) = (SELECT strftime('%Y', date) FROM expenses ORDER BY date DESC LIMIT 1) GROUP BY category")
            data = self.c.fetchall()
            categories = [row[0] for row in data]
            expenses = [row[1] for row in data]

            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(expenses, labels=categories, autopct='%1.1f%%')
            ax.set_title('Графік витрат за останній місяць')

            canvas = FigureCanvasTkAgg(fig, master=self.monthly_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def show_yearly_chart(self):
        if self.yearly_chart_frame.winfo_ismapped():
            self.yearly_chart_frame.pack_forget()
        else:
            self.yearly_chart_frame.pack()

            # Очистити попередній графік
            for widget in self.yearly_chart_frame.winfo_children():
                widget.destroy()

            self.c.execute("SELECT strftime('%Y', date) AS year, SUM(amount) FROM expenses GROUP BY year")
            data = self.c.fetchall()
            years = [row[0] for row in data]
            expenses = [row[1] for row in data]

            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(years, expenses)
            ax.set_title('Річні витрати')
            ax.set_xlabel('Рік')
            ax.set_ylabel('Загальні витрати')

            canvas = FigureCanvasTkAgg(fig, master=self.yearly_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def create_widgets(self):
        title_label = tk.Label(self, text="БЮДЖЕТ ТРЕКЕР", fg='#00f', font=("Comic Sans MS",  26,"bold"), underline=6)
        title_label.pack(pady=10)

        # Додавання витрат
        expense_frame = tk.Frame(self)
        expense_frame.pack(pady=10)

        amount_label = tk.Label(expense_frame, text="сума: ")
        amount_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = tk.Entry(expense_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        category_label = tk.Label(expense_frame, text="категорія: ")
        category_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.category_combobox = ttk.Combobox(expense_frame, values=self.categories)
        self.category_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        date_label = tk.Label(expense_frame, text="дата: ")
        date_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = DateEntry(expense_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='y/mm/dd')
        self.date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        comment_label = tk.Label(expense_frame, text="коментар: ")
        comment_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.comment_entry = tk.Entry(expense_frame)
        self.comment_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")


        add_button = tk.Button(expense_frame, text="Додати витрату", command=self.add_expense)
        add_button.grid(row=4, columnspan=2, pady=5)

        # Cума витрат за сесію
        self.total_expenses_label = tk.Label(self, text="Cума витрат за сесію: 0", fg='darkblue', font=("Comic Sans MS", 12, "bold"),)
        self.total_expenses_label.pack()

        # Показати витрати, поле
        expenses_frame = tk.Frame(self)
        expenses_frame.pack(pady=10)

        show_expenses_button = tk.Button(expenses_frame, text="Історія витрат", command=self.show_expenses)
        show_expenses_button.pack(pady=5)

        self.expenses_text = scrolledtext.ScrolledText(expenses_frame, width=90, height=10)
        self.expenses_text.pack()

        # Місячні витрати
        self.monthly_chart_frame = tk.Frame(self)
        monthly_chart_button = tk.Button(self, text="Місячні витрати", command=self.show_monthly_chart)
        monthly_chart_button.pack(pady=5)

        # Річні витрати
        self.yearly_chart_frame = tk.Frame(self)
        yearly_chart_button = tk.Button(self, text="Річні витрати", command=self.show_yearly_chart)
        yearly_chart_button.pack(pady=5)

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()