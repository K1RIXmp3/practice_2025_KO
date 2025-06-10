import tkinter as tk
from tkinter import messagebox
import random
import os

DATA_FILE = "finance_data.txt"

# Примеры советов по финансовой грамотностиЫ
FINANCE_TIPS = [
    "Всегда откладывай 10% от дохода.",
    "Веди учёт расходов — это поможет контролировать бюджет.",
    "Избегай импульсивных покупок.",
    "Плати себе первым — сначала отложи, потом трать.",
    "Инвестируй в самообразование.",
    "Старайся не брать кредиты на потребление.",
    "Планируй крупные покупки заранее.",
    "Используй правило 50/30/20 для бюджета: 50% — нужды, 30% — желания, 20% — накопления.",
]

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_data(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        for entry in entries:
            file.write(entry + "\n")

def calculate_balance(entries):
    balance = 0
    for entry in entries:
        parts = entry.split("|", 1)
        if parts[0].startswith("+"):
            balance += float(parts[0][1:])
        elif parts[0].startswith("-"):
            balance -= float(parts[0][1:])
    return balance

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый калькулятор с комментариями")

        self.entries = load_data()

        # Поле ввода суммы
        tk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Поле ввода комментария
        tk.Label(root, text="Комментарий:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.comment_entry = tk.Entry(root)
        self.comment_entry.grid(row=1, column=1, padx=5, pady=5)

        # Кнопки дохода и расхода
        tk.Button(root, text="Добавить доход", command=self.add_income).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(root, text="Добавить расход", command=self.add_expense).grid(row=2, column=1, padx=5, pady=5)

        # Кнопка показать баланс
        tk.Button(root, text="Показать баланс", command=self.show_balance).grid(row=3, column=0, columnspan=2, pady=5)

        # Кнопка показать историю
        tk.Button(root, text="Показать историю", command=self.show_history).grid(row=4, column=0, columnspan=2, pady=5)

        # Кнопка очистки файла
        tk.Button(root, text="Очистить данные", fg="red", command=self.clear_data).grid(row=5, column=0, columnspan=2, pady=5)

        # Текстовое поле истории
        self.history_text = tk.Text(root, height=12, width=50)
        self.history_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Закрытие с сохранением
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_income(self):
        self.add_entry(income=True)

    def add_expense(self):
        self.add_entry(income=False)

    def add_entry(self, income):
        amount = self.amount_entry.get().strip()
        comment = self.comment_entry.get().strip()

        if self.validate_amount(amount):
            sign = "+" if income else "-"
            full_entry = f"{sign}{amount}|{comment if comment else 'Без комментария'}"
            self.entries.append(full_entry)
            self.amount_entry.delete(0, tk.END)
            self.comment_entry.delete(0, tk.END)
            messagebox.showinfo("Успех", "Операция добавлена.")

    def show_balance(self):
        balance = calculate_balance(self.entries)
        tip = random.choice(FINANCE_TIPS)
        messagebox.showinfo("Баланс", f"Текущий баланс: {balance:.2f} руб.\n\n💡 Совет: {tip}")

    def show_history(self):
        self.history_text.delete("1.0", tk.END)
        if not self.entries:
            self.history_text.insert(tk.END, "История пуста.")
        else:
            for i, entry in enumerate(self.entries, 1):
                parts = entry.split("|", 1)
                if parts[0].startswith("+"):
                    self.history_text.insert(tk.END, f"{i}. Доход: +{parts[0][1:]} руб. — {parts[1]}\n")
                elif parts[0].startswith("-"):
                    self.history_text.insert(tk.END, f"{i}. Расход: -{parts[0][1:]} руб. — {parts[1]}\n")

    def clear_data(self):
        answer = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить все данные?")
        if answer:
            self.entries.clear()
            save_data(self.entries)
            self.history_text.delete("1.0", tk.END)
            messagebox.showinfo("Готово", "Все данные удалены.")

    def validate_amount(self, amount):
        try:
            float(amount)
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму.")
            return False

    def on_close(self):
        save_data(self.entries)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
