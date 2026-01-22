import tkinter as tk
from tkinter import ttk
#from generator import generate_document
#from collect import collect_form_data
# from generator import generate_document
# from tkinter import messagebox
import os



# Повний список країн світу
COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
    "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark",
    "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece",
    "Grenada", "Guatemala", "Guinea", "Guyana", "Haiti", "Honduras", "Hungary",
    "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
    "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North",
    "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon",
    "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Mauritania",
    "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro",
    "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway",
    "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru",
    "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
    "Saint Kitts and Nevis", "Saint Lucia", "Samoa", "San Marino", "Saudi Arabia",
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
    "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain",
    "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
    "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga",
    "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda",
    "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay",
    "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen",
    "Zambia", "Zimbabwe"
]

def setup_autocomplete(combobox, full_list):
    """Налаштовує розумний пошук, який не вибиває курсор з поля."""
    def check_input(event):
        # Не реагуємо на клавіші керування
        if event.keysym in ("Down", "Up", "Return", "Escape", "Tab", "Shift_L", "Control_L"):
            return

        value = combobox.get().lower()
        
        if value == '':
            combobox['values'] = full_list
        else:
            filtered_list = [item for item in full_list if value in item.lower()]
            combobox['values'] = filtered_list
        
        # Відкриваємо список без перехоплення фокусу
        try:
            combobox.tk.call(combobox._w, "post")
        except tk.TclError:
            pass

    combobox.bind('<KeyRelease>', check_input)

def create_main_tab(notebook):
    tab = ttk.Frame(notebook)
    
    vars_dict = {
        "series": tk.StringVar(value="ІВ"),
        "cert_num": tk.StringVar(),
        "first_name": tk.StringVar(),
        "last_name": tk.StringVar(),
        "home_address": tk.StringVar(),
        "phone": tk.StringVar(),
        "destination_address": tk.StringVar(),
        "postal_code": tk.StringVar(),
        "entry_country": tk.StringVar(),
        "dest_country": tk.StringVar()
    }

    # Налаштування прокрутки
    canvas = tk.Canvas(tab, highlightthickness=0)
    scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    #canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # --- Секція 1: Основні реквізити ---
    frame_main = ttk.LabelFrame(scrollable_frame, text=" Основна інформація ", padding=10)
    frame_main.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_main, text="Серія:").grid(row=0, column=0, sticky="w")
    series_cb = ttk.Combobox(frame_main, textvariable=vars_dict["series"], 
                             values=["ІВ", "ІБ", "ІА", "АІ"], width=7)
    series_cb.grid(row=0, column=1, sticky="w", padx=5)

    ttk.Label(frame_main, text="Номер:").grid(row=0, column=2, sticky="w", padx=10)
    ttk.Entry(frame_main, textvariable=vars_dict["cert_num"], width=15).grid(row=0, column=3, sticky="w")

    # --- Секція 2: Дані особи ---
    frame_personal = ttk.LabelFrame(scrollable_frame, text=" Дані особи ", padding=10)
    frame_personal.pack(fill="x", padx=10, pady=5)

    fields_personal = [
        ("Ім'я", "first_name"),
        ("Прізвище", "last_name"),
        ("Домашня адреса", "home_address"),
        ("Телефон", "phone"),
    ]

    for i, (label, var_name) in enumerate(fields_personal):
        ttk.Label(frame_personal, text=f"{label}:").grid(row=i, column=0, sticky="w", pady=2)
        ttk.Entry(frame_personal, textvariable=vars_dict[var_name], width=45).grid(row=i, column=1, sticky="w", padx=10, pady=2)

    # --- Секція 3: Адресація та логістика ---
    frame_geo = ttk.LabelFrame(scrollable_frame, text=" Маршрут та адреса призначення ", padding=10)
    frame_geo.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_geo, text="Адреса призначення:").grid(row=0, column=0, sticky="w", pady=2)
    ttk.Entry(frame_geo, textvariable=vars_dict["destination_address"], width=45).grid(row=0, column=1, sticky="w", padx=10, pady=2)

    ttk.Label(frame_geo, text="Поштовий код:").grid(row=1, column=0, sticky="w", pady=2)
    ttk.Entry(frame_geo, textvariable=vars_dict["postal_code"], width=15).grid(row=1, column=1, sticky="w", padx=10, pady=2)

    # Поле Країна в'їзду
    ttk.Label(frame_geo, text="Країна в'їзду:").grid(row=2, column=0, sticky="w", pady=2)
    entry_c_combo = ttk.Combobox(frame_geo, textvariable=vars_dict["entry_country"], values=COUNTRIES, width=42)
    entry_c_combo.grid(row=2, column=1, sticky="w", padx=10, pady=2)
    setup_autocomplete(entry_c_combo, COUNTRIES)

    # Поле Країна призначення
    ttk.Label(frame_geo, text="Країна призначення:").grid(row=3, column=0, sticky="w", pady=2)
    dest_c_combo = ttk.Combobox(frame_geo, textvariable=vars_dict["dest_country"], values=COUNTRIES, width=42)
    dest_c_combo.grid(row=3, column=1, sticky="w", padx=10, pady=2)
    setup_autocomplete(dest_c_combo, COUNTRIES)

    # Пакування Canvas
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def on_generate():
        from logic.collect import collect_form_data
        from logic.generator import generate_document
        import os
        from tkinter import messagebox
    
        data = collect_form_data(vars_dict)
    
        os.makedirs("templates", exist_ok=True)
        output_path = os.path.join("templates", "test_certificate.docx")
    
        generate_document(output_path, data)
    
        messagebox.showinfo(
            "Готово",
            f"Документ створено:\n{output_path}"
    )


    
    btn_frame = ttk.Frame(scrollable_frame)
    btn_frame.pack(fill="x", padx=10, pady=15)
    
    ttk.Button(
        btn_frame,
        text="Згенерувати документ",
        command=on_generate
    ).pack(anchor="e")
    
    return tab, vars_dict
