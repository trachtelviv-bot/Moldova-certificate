def collect_form_data(vars_dict):
    return {k: v.get() for k, v in vars_dict.items()}

# {
  # "certificate_header": "Сертифікат: ІВ 12345",
  # "full_name": "ПЕТРЕНКО ІВАН",
  # "home_address": "...",
  # "phone": "...",
  # "entry_country": "...",
  # "dest_country": "..."
# }
