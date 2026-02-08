import tkinter as tk
from tkinter import ttk
import os

# =====================================================
# COUNTRIES
# =====================================================
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

# =====================================================
# AUTOCOMPLETE
# =====================================================
def setup_autocomplete(combobox, full_list):
    def check_input(event):
        if event.keysym in ("Down", "Up", "Return", "Escape", "Tab"):
            return
        value = combobox.get().lower()
        combobox["values"] = (
            full_list if value == "" else
            [c for c in full_list if value in c.lower()]
        )
        try:
            combobox.tk.call(combobox._w, "post")
        except tk.TclError:
            pass

    combobox.bind("<KeyRelease>", check_input)

# =====================================================
# AUTOFILL ON FOCUS OUT
# =====================================================
def autofill_on_focusout(source_var: tk.StringVar, entry_widget: tk.Entry):
    """Заповнює entry значенням source_var при виході з поля, якщо воно порожнє"""
    def handler(event):
        if not entry_widget.get().strip():
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, source_var.get())
    entry_widget.bind("<FocusOut>", handler)

# =====================================================
# MAIN TAB
# =====================================================
def create_main_tab(notebook):
    tab = ttk.Frame(notebook)

    vars_dict = {
        "series": tk.StringVar(value="ІВ"),
        "cert_num": tk.StringVar(),

        # Дані особи
        "first_name": tk.StringVar(),
        "last_name": tk.StringVar(),
        "home_address": tk.StringVar(),
        "phone": tk.StringVar(),

        # Довірена особа
        "rep_first_name": tk.StringVar(),
        "rep_last_name": tk.StringVar(),
        "rep_address": tk.StringVar(),
        "rep_phone": tk.StringVar(),

        # Маршрут
        "destination_address": tk.StringVar(),
        "postal_code": tk.StringVar(),
        "entry_country": tk.StringVar(),
        "dest_country": tk.StringVar(),

        # Місця
        "origin_name": tk.StringVar(),
        "origin_address": tk.StringVar(),
        "dest_name": tk.StringVar(),
        "dest_address": tk.StringVar(),
        "dest_postal": tk.StringVar(),
    }

    # ---------- Scroll ----------
    canvas = tk.Canvas(tab, highlightthickness=0)
    scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # =================================================
    # Основна інформація
    # =================================================
    frame_main = ttk.LabelFrame(scrollable_frame, text=" Основна інформація ", padding=10)
    frame_main.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_main, text="Серія:").grid(row=0, column=0, sticky="w")
    ttk.Combobox(
        frame_main, textvariable=vars_dict["series"],
        values=["ІВ", "ІБ", "ІА", "АІ"], width=7
    ).grid(row=0, column=1, sticky="w")

    ttk.Label(frame_main, text="Номер:").grid(row=0, column=2, sticky="w", padx=10)
    ttk.Entry(frame_main, textvariable=vars_dict["cert_num"], width=15).grid(row=0, column=3)

    # =================================================
    # Дані особи
    # =================================================
    frame_personal = ttk.LabelFrame(scrollable_frame, text=" Дані особи ", padding=10)
    frame_personal.pack(fill="x", padx=10, pady=5)

    personal_fields = [
        ("Ім'я", "first_name"),
        ("Прізвище", "last_name"),
        ("Домашня адреса", "home_address"),
        ("Телефон", "phone"),
    ]

    for i, (label, var) in enumerate(personal_fields):
        ttk.Label(frame_personal, text=label).grid(row=i, column=0, sticky="w")
        ttk.Entry(frame_personal, textvariable=vars_dict[var], width=45).grid(row=i, column=1, padx=10)

    # =================================================
    # Довірена особа
    # =================================================
    frame_rep = ttk.LabelFrame(scrollable_frame, text=" Довірена особа ", padding=10)
    frame_rep.pack(fill="x", padx=10, pady=5)

    rep_map = [
        ("Ім'я", "rep_first_name", "first_name"),
        ("Прізвище", "rep_last_name", "last_name"),
        ("Адреса", "rep_address", "home_address"),
        ("Телефон", "rep_phone", "phone"),
    ]

    for i, (label, target, source) in enumerate(rep_map):
        ttk.Label(frame_rep, text=label).grid(row=i, column=0, sticky="w")
        entry = ttk.Entry(frame_rep, textvariable=vars_dict[target], width=45)
        entry.grid(row=i, column=1, padx=10)
        autofill_on_focusout(vars_dict[source], entry)

    # =================================================
    # Маршрут
    # =================================================
    frame_geo = ttk.LabelFrame(scrollable_frame, text=" Маршрут та адреса призначення ", padding=10)
    frame_geo.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_geo, text="Адреса призначення").grid(row=0, column=0, sticky="w")
    ttk.Entry(frame_geo, textvariable=vars_dict["destination_address"], width=45).grid(row=0, column=1, padx=10)

    ttk.Label(frame_geo, text="Поштовий код").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame_geo, textvariable=vars_dict["postal_code"], width=15).grid(row=1, column=1, sticky="w", padx=10)

    ttk.Label(frame_geo, text="Країна в'їзду").grid(row=2, column=0, sticky="w")
    entry_c = ttk.Combobox(frame_geo, textvariable=vars_dict["entry_country"], values=COUNTRIES, width=42)
    entry_c.grid(row=2, column=1, padx=10)
    setup_autocomplete(entry_c, COUNTRIES)

    ttk.Label(frame_geo, text="Країна призначення").grid(row=3, column=0, sticky="w")
    dest_c = ttk.Combobox(frame_geo, textvariable=vars_dict["dest_country"], values=COUNTRIES, width=42)
    dest_c.grid(row=3, column=1, padx=10)
    setup_autocomplete(dest_c, COUNTRIES)

    # =================================================
    # Місце походження
    # =================================================
    frame_origin = ttk.LabelFrame(scrollable_frame, text=" Місце походження ", padding=10)
    frame_origin.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_origin, text="Назва / Ім'я").grid(row=0, column=0, sticky="w")
    e_origin_name = ttk.Entry(frame_origin, textvariable=vars_dict["origin_name"], width=45)
    e_origin_name.grid(row=0, column=1, padx=10)
    autofill_on_focusout(vars_dict["first_name"], e_origin_name)

    ttk.Label(frame_origin, text="Адреса").grid(row=1, column=0, sticky="w")
    e_origin_address = ttk.Entry(frame_origin, textvariable=vars_dict["origin_address"], width=45)
    e_origin_address.grid(row=1, column=1, padx=10)
    autofill_on_focusout(vars_dict["home_address"], e_origin_address)

    # =================================================
    # Місце призначення
    # =================================================
    frame_dest = ttk.LabelFrame(scrollable_frame, text=" Місце призначення ", padding=10)
    frame_dest.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_dest, text="Назва / Ім'я").grid(row=0, column=0, sticky="w")
    e_dest_name = ttk.Entry(frame_dest, textvariable=vars_dict["dest_name"], width=45)
    e_dest_name.grid(row=0, column=1, padx=10)
    autofill_on_focusout(vars_dict["first_name"], e_dest_name)

    ttk.Label(frame_dest, text="Адреса").grid(row=1, column=0, sticky="w")
    e_dest_address = ttk.Entry(frame_dest, textvariable=vars_dict["dest_address"], width=45)
    e_dest_address.grid(row=1, column=1, padx=10)
    autofill_on_focusout(vars_dict["destination_address"], e_dest_address)

    ttk.Label(frame_dest, text="Поштовий код").grid(row=2, column=0, sticky="w")
    e_dest_postal = ttk.Entry(frame_dest, textvariable=vars_dict["dest_postal"], width=15)
    e_dest_postal.grid(row=2, column=1, sticky="w", padx=10)
    autofill_on_focusout(vars_dict["postal_code"], e_dest_postal)

    # =================================================
    # BUTTON
    # =================================================
    def on_generate():
        from logic.collect import collect_form_data
        from logic.generator import generate_document
        from tkinter import messagebox

        data = collect_form_data(vars_dict)
        os.makedirs("templates", exist_ok=True)
        output = os.path.join("templates", "test_certificate.docx")
        generate_document(output, data)
        messagebox.showinfo("Готово", f"Документ створено:\n{output}")

    ttk.Button(scrollable_frame, text="Згенерувати документ", command=on_generate)\
        .pack(anchor="e", padx=10, pady=15)

    return tab, vars_dict
