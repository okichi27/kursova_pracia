import tkinter as tk
from tkinter import messagebox
import sqlite3

# Створення бази даних та таблиці
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                date TEXT)''')
conn.commit()

# Функція для додавання витрат
def add_expense():
    try:
        amount = float(amount_entry.get())
        date = date_entry.get()

        # Додавання витрат до бази даних
        cursor.execute("INSERT INTO expenses (amount, date) VALUES (?, ?)", (amount, date))
        conn.commit()

        # Очищення полів вводу
        amount_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)

        # Виведення сповіщення про успішне додавання
        messagebox.showinfo("Успіх", "Витрату додано успішно!")
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть коректну суму витрат (число).")

# Створення головного вікна
ws = tk.Tk()
ws.title("Відстеження витрат")
ws.geometry("400x200")

# Створення віджетів
amount_label = tk.Label(ws, text="Сума витрат:")
amount_label.grid(row=0, column=0, padx=10, pady=10)
amount_entry = tk.Entry(ws)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

date_label = tk.Label(ws, text="Дата покупки:")
date_label.grid(row=1, column=0, padx=10, pady=10)
date_entry = tk.Entry(ws)
date_entry.grid(row=1, column=1, padx=10, pady=10)

add_button = tk.Button(ws, text="Додати витрату", command=add_expense)
add_button.grid(row=2, columnspan=2, padx=10, pady=10)

# Запуск головного циклу
ws.mainloop()

# Закриття бази даних
conn.close()
