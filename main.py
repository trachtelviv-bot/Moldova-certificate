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

def generate_document_action():
    from logic.collect import collect_form_data
    from logic.generator import generate_document
    from tkinter import messagebox
    import os

    # Об'єднуємо всі дані
    all_vars = {}
    all_vars.update(main_vars)
    all_vars.update(cargo_vars)
    all_vars.update(vetcontrol_vars)

    data = collect_form_data(all_vars)

    os.makedirs("templates", exist_ok=True)
    output = os.path.join("templates", "test_certificate.docx")

    generate_document(output, data)

    messagebox.showinfo("Готово", f"Документ створено:\n{output}")

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
vet_tab, vetcontrol_vars = create_vetcontrol_tab(
    notebook,
    generate_callback=generate_document_action
)

notebook.add(vet_tab, text="Ветконтроль")


notebook.pack(fill="both", expand=True)

root.mainloop()
