import tkinter as tk
from tkinter import ttk
from ui.form import create_main_tab  # Імпортуємо твою функцію

root = tk.Tk()
root.title("Сертифікати")
root.geometry("600x700")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Виклик функції з form.py
tab_main, form_vars = create_main_tab(notebook)
notebook.add(tab_main, text="Основні дані")

root.mainloop() # Це тримає вікно відкритим
