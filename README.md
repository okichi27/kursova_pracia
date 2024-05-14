# budget app
**attempt to write at least something similar to the coursework 3 days before submission**

This repository features a personal expense tracking project.

Consists of 4 files:
1. **budget.py**;
2. **budget_angl_1.py**;
3. **budget_angl_2.py**;
4. **expenses.db**.
    
## budget_angl.py

The program is in English.
There are 2 versions of the same program: 
- **budget_angl_1.py** - old design;
- **budget_angl_2.py** - new design.

### **Launch**
1. Download git.
2. Run the code with the translation you need: budget_angl.py(English) or budget.py(Ukrainian).

### **Usage**
Let's consider the functionality of the program:
1. Amount - enter the cost amount (example: 100, 100.76);
2. Category - you need to choose the same category of expenses (it will be possible to specify more specifically later);
3. Date - during selection, a calendar appears with the current date for choosing the date of expenditure, you can change the year and month using the arrows, and the date must be selected on the calendar;
4. Comment - you can enter a specific reason for the expense.
5. "Add Expense" button - when pressed, the previous data is saved to the database, if any item is omitted (except for the comment), a window with an error message appears.
6. Total Expenses per session - the amount of expenses that you paid for this session of using the program;
7. button "Show Expense" - when clicked, data about all expenses (even previous sessions) appear in the field (under the button);
8. field - a field showing the history of expenses for all sessions. On the right side of the field, there is a ribbon to scroll the expenses;
9. Monthly Chart - after clicking the button, a pie chart by categories for the last specified month appears. When pressed again, the chart disappears.
10. Yearly Chart - after clicking the button, a schedule of expenses by year appears. When pressed again, the graph disappears.

## budget.py 

**Той же додаток**, але з український перекладом. Тому запуск і користування описано українською мовою.

### **Запуск**
1. Завантажуємо гіт.
2. Запускаємо код з потрібним вам перекладом: budget_angl.py(англійська мова) чи budget.py(українська мова).

### **Користування**
Розглянемо функціонал програми:
1. Сума - ввести суму витрати(приклад: 100, 100.76);
2. Категорія - потрібно обрати одну ж категорії витрат(пізніше можна буде вказати конкретніше);
3. Дата - під час вибору з'являється календар з теперішньою датою для вибору дати витрати, можна змінювати рік та місяць за допомогою стрілок а дату потрібно обрати на календарі;
4. Коментар - можна вписати конкретну причину витрати.
5. кнопка "Додати витрату" - при натиску попередні дані зберігаються до бази даних, при пропущені якогось пункту(окрім коментар) з'являється вікно з повідомленням про помилку.
6. Сума витрат за сесію - сума витрат, які ви внесли за цю сесію користування програмою;
7. кнопка "Історія витрат" - при натиску у полі(під кнопкою) з'являються дані про усі витрати (навіть попередні сесії);
8. поле - поле показу історії витрат за усі сесії. З правого боку поля, є стрічка аби прокрутити витрати;
9. Місячні витрати - після натискання кнопки з'являється кільцева діаграма за категоріями за останній вказаний місяць. При повторному натиску діаграма зникає.
10. Річні витрати - після натискання кнопки з'являється графік витрат за роками. При повторному натиску графік зникає.

## expenses.db

База даних з раніше доданими витратами, українською мовою! Це для того аби спершу спробувати як воно мало б виглядати.



**your okichi :)**
