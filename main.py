import tkinter as tk
from tkinter import ttk
from ui.form import create_main_tab, create_cargo_tab  # твій файл form.py

root = tk.Tk()
root.title("Форма сертифікату")
root.geometry("900x700")  # можна підкоригувати

notebook = ttk.Notebook(root)

# Перша вкладка
main_tab, main_vars = create_main_tab(notebook)
notebook.add(main_tab, text="Основна інформація")

# Друга вкладка
cargo_tab, cargo_vars = create_cargo_tab(notebook)
notebook.add(cargo_tab, text="Вантаж")

notebook.pack(fill="both", expand=True)

root.mainloop()
