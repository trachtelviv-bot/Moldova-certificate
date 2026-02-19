import tkinter as tk
from tkinter import ttk
from ui.form import (
    create_main_tab,
    create_cargo_tab,
    create_vetcontrol_tab,
    save_vetcontrol_config
)




root = tk.Tk()
root.title("Форма сертифікату")
root.geometry("900x700")  # можна підкоригувати

notebook = ttk.Notebook(root)

def on_closing():
    data_to_save = {k: v.get() for k, v in vetcontrol_vars.items()}
    save_vetcontrol_config(data_to_save)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)


# Перша вкладка
main_tab, main_vars = create_main_tab(notebook)
notebook.add(main_tab, text="Основна інформація")

# Друга вкладка
cargo_tab, cargo_vars = create_cargo_tab(notebook)
notebook.add(cargo_tab, text="Вантаж")

# Третя вкладка
vet_tab, vetcontrol_vars = create_vetcontrol_tab(notebook)
notebook.add(vet_tab, text="Ветконтроль")


notebook.pack(fill="both", expand=True)

root.mainloop()
