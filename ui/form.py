import tkinter as tk
from tkinter import ttk
import os
import json

CONFIG_FILE = "vetcontrol_config.json"

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
# CONFIG SAVE / LOAD
# =====================================================
def load_vetcontrol_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_vetcontrol_config(data: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


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

# =====================================================
# CARGO TAB
# =====================================================
def create_cargo_tab(notebook):
    tab = ttk.Frame(notebook)

    vars_dict = {
        # Перевезення
        "transport_num": tk.StringVar(),
        "checkpoint": tk.StringVar(),
        "goods_description": tk.StringVar(),
        "goods_code": tk.StringVar(),
        "animal_count": tk.StringVar(),

        # Ідентифікація тварин
        "animal_species": tk.StringVar(),
        "identification_system": tk.StringVar(),
        "chip_number": tk.StringVar(),

        # Заповнити за необхідності
        "cites_num": tk.StringVar(),
        "package_count": tk.StringVar(),
        "package_type": tk.StringVar(),
        "seal_number": tk.StringVar(),
        # ІІ.3
        "ii3_mode": tk.StringVar(value="birds"),
        "cb_isolated": tk.BooleanVar(value=True),
        "cb_vaccinated": tk.BooleanVar(value=False),
        "cb_tested": tk.BooleanVar(value=False),
        "cb_household": tk.BooleanVar(value=True),
        "cb_origin_isolated_or_vacc": tk.BooleanVar(value=True),

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
    # Перевезення
    # =================================================
    frame_transport = ttk.LabelFrame(scrollable_frame, text=" Перевезення ", padding=10)
    frame_transport.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_transport, text="Номер транспорту").grid(row=0, column=0, sticky="w")
    ttk.Entry(frame_transport, textvariable=vars_dict["transport_num"], width=20).grid(row=0, column=1, padx=10)

    ttk.Label(frame_transport, text="Пункт переходу").grid(row=1, column=0, sticky="w")
    cb_checkpoint = ttk.Combobox(frame_transport, textvariable=vars_dict["checkpoint"], width=42)
    cb_checkpoint.grid(row=1, column=1, padx=10)
    # setup_autocomplete(cb_checkpoint, CHECKPOINTS_LIST)

    ttk.Label(frame_transport, text="Опис товару").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame_transport, textvariable=vars_dict["goods_description"], width=45).grid(row=2, column=1, padx=10)

    ttk.Label(frame_transport, text="Код товару").grid(row=3, column=0, sticky="w")
    cb_goods_code = ttk.Combobox(frame_transport, textvariable=vars_dict["goods_code"], width=42)
    cb_goods_code.grid(row=3, column=1, padx=10)
    # setup_autocomplete(cb_goods_code, GOODS_CODE_LIST)

    ttk.Label(frame_transport, text="Кількість тварин").grid(row=4, column=0, sticky="w")
    cb_animal_count = ttk.Combobox(frame_transport, textvariable=vars_dict["animal_count"], width=10)
    cb_animal_count.grid(row=4, column=1, sticky="w", padx=10)
    # setup_autocomplete(cb_animal_count, ANIMAL_COUNT_LIST)

    # =================================================
    # Ідентифікація тварин
    # =================================================
    frame_id = ttk.LabelFrame(scrollable_frame, text=" Ідентифікація тварин ", padding=10)
    frame_id.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_id, text="Вид (наукова назва)").grid(row=0, column=0, sticky="w")
    cb_species = ttk.Combobox(frame_id, textvariable=vars_dict["animal_species"], width=42)
    cb_species.grid(row=0, column=1, padx=10)
    # setup_autocomplete(cb_species, SPECIES_LIST)

    ttk.Label(frame_id, text="С-ма ідентифікації").grid(row=1, column=0, sticky="w")
    cb_id_system = ttk.Combobox(frame_id, textvariable=vars_dict["identification_system"], width=42)
    cb_id_system.grid(row=1, column=1, padx=10)
    # setup_autocomplete(cb_id_system, ID_SYSTEM_LIST)

    ttk.Label(frame_id, text="№ чіпа і т.п.").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame_id, textvariable=vars_dict["chip_number"], width=30).grid(row=2, column=1, padx=10)


    # =================================================
    # Заповнити за необхідності
    # =================================================
    frame_optional = ttk.LabelFrame(scrollable_frame, text=" Заповнити за необхідності ", padding=10)
    frame_optional.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_optional, text="№ CITES").grid(row=0, column=0, sticky="w")
    ttk.Entry(frame_optional, textvariable=vars_dict["cites_num"], width=20).grid(row=0, column=1, padx=10)

    ttk.Label(frame_optional, text="К-ть упаковок (кліток)").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame_optional, textvariable=vars_dict["package_count"], width=10).grid(row=1, column=1, sticky="w", padx=10)

    ttk.Label(frame_optional, text="Тип упаковки (клітка тощо)").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame_optional, textvariable=vars_dict["package_type"], width=30).grid(row=2, column=1, padx=10)

    ttk.Label(frame_optional, text="Номер пломби (якщо опломбовано)").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame_optional, textvariable=vars_dict["seal_number"], width=30).grid(row=3, column=1, padx=10)

    # =================================================
    # ІІ.3 Умови
    # =================================================
    frame_ii3 = ttk.LabelFrame(scrollable_frame, text=" ІІ.3 Умови ", padding=10)
    frame_ii3.pack(fill="x", padx=10, pady=5)

    cb1 = ttk.Checkbutton(frame_ii3,
                          text="Ізольовані 30 днів",
                          variable=vars_dict["cb_isolated"])
    cb1.pack(anchor="w")

    cb2 = ttk.Checkbutton(frame_ii3,
                          text="Вакциновані (H5/H7)",
                          variable=vars_dict["cb_vaccinated"])
    cb2.pack(anchor="w")

    cb3 = ttk.Checkbutton(frame_ii3,
                          text="Пройшли тест (H5/H7)",
                          variable=vars_dict["cb_tested"])
    cb3.pack(anchor="w")

    cb4 = ttk.Checkbutton(frame_ii3,
                          text="До домогосподарства 30 днів",
                          variable=vars_dict["cb_household"])
    cb4.pack(anchor="w")

    cb5 = ttk.Checkbutton(frame_ii3,
                          text="Ізольовані або вакциновані",
                          variable=vars_dict["cb_origin_isolated_or_vacc"])
    cb5.pack(anchor="w")

    def toggle_checkboxes():
        state = "normal" if vars_dict["ii3_mode"].get() == "birds" else "disabled"
        for cb in (cb1, cb2, cb3, cb4, cb5):
            cb.configure(state=state)

    ttk.Radiobutton(frame_ii3,
                    text="ІІ.3 Птахи",
                    variable=vars_dict["ii3_mode"],
                    value="birds",
                    command=toggle_checkboxes).pack(anchor="w")

    ttk.Radiobutton(frame_ii3,
                    text="ІІ.3 Карантинний центр",
                    variable=vars_dict["ii3_mode"],
                    value="quarantine",
                    command=toggle_checkboxes).pack(anchor="w")

    toggle_checkboxes()


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
# =====================================================
# VETCONTROL TAB
# =====================================================
def create_vetcontrol_tab(notebook):

    tab = ttk.Frame(notebook)

    vars_dict = {
        "pik_department": tk.StringVar(),
        "pik_address": tk.StringVar(),
        "official_person": tk.StringVar(),

        "vet_login": tk.StringVar(),
        "vet_password": tk.StringVar(),
        "vet_department": tk.StringVar(),
    }

    # ---------- Завантаження з файлу ----------
    saved_data = load_vetcontrol_config()
    for key in vars_dict:
        if key in saved_data:
            vars_dict[key].set(saved_data[key])

    main_frame = ttk.Frame(tab, padding=15)
    main_frame.pack(fill="both", expand=True)

    # =================================================
    # Реквізити сертифікату
    # =================================================
    frame_cert = ttk.LabelFrame(main_frame, text=" Реквізити сертифікату ", padding=10)
    frame_cert.pack(fill="x", pady=10)

    ttk.Label(frame_cert, text="Відділ ПІК").grid(row=0, column=0, sticky="w")
    ttk.Entry(frame_cert, textvariable=vars_dict["pik_department"], width=50).grid(row=0, column=1, padx=10)

    ttk.Label(frame_cert, text="Адреса").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame_cert, textvariable=vars_dict["pik_address"], width=50).grid(row=1, column=1, padx=10)

    ttk.Label(frame_cert, text="Службова особа").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame_cert, textvariable=vars_dict["official_person"], width=50).grid(row=2, column=1, padx=10)

    # =================================================
    # ВетКонтроль
    # =================================================
    frame_vet = ttk.LabelFrame(main_frame, text=" ВетКонтроль ", padding=10)
    frame_vet.pack(fill="x", pady=10)

    ttk.Label(frame_vet, text="Логін ВетКонтролю").grid(row=0, column=0, sticky="w")
    ttk.Entry(frame_vet, textvariable=vars_dict["vet_login"], width=40).grid(row=0, column=1, padx=10)

    ttk.Label(frame_vet, text="Пароль ВетКонтролю").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame_vet, textvariable=vars_dict["vet_password"], show="*", width=40).grid(row=1, column=1, padx=10)

    ttk.Label(frame_vet, text="Підрозділ ВетКонтроль").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame_vet, textvariable=vars_dict["vet_department"], width=50).grid(row=2, column=1, padx=10)

    return tab, vars_dict

