import pandas as pd
import os

def verify_user(ic_number, password):
    return len(ic_number) == 12 and password == ic_number[-4:]

def calculate_tax(income, tax_relief):
    chargeable_income = max(0, income - tax_relief)

    if chargeable_income <= 5000:
        tax = 0
    elif chargeable_income <= 20000:
        tax = (chargeable_income - 5000) * 0.01
    elif chargeable_income <= 35000:
        tax = 150 + (chargeable_income - 20000) * 0.03
    elif chargeable_income <= 50000:
        tax = 600 + (chargeable_income - 35000) * 0.08
    elif chargeable_income <= 70000:
        tax = 1800 + (chargeable_income - 50000) * 0.14
    elif chargeable_income <= 100000:
        tax = 4600 + (chargeable_income - 70000) * 0.21
    else:
        tax = 10900 + (chargeable_income - 100000) * 0.24

    return round(tax, 2)

def save_to_csv(data, filename):
    columns = ['IC Number', 'Income', 'Tax Relief', 'Tax Payable']
    df = pd.DataFrame([data], columns=columns)

    if os.path.exists(filename):
        df.to_csv(filename, mode='a', index=False, header=False)
    else:
        df.to_csv(filename, mode='w', index=False, header=True)

def read_from_csv(filename):
    if os.path.exists(filename):
        return pd.read_csv(filename, dtype={'IC Number': str})
    return None

def gather_tax_reliefs():
    print("\n--- Tax Relief Categories ---")

    try:
        individual = 9000  # fixed

        spouse = float(input("Spouse Relief (max RM4000): ") or 0)
        children = int(input("Number of children (max 12): ") or 0)
        child_relief = min(children, 12) * 8000

        medical = float(input("Medical Expenses (max RM8000): ") or 0)
        lifestyle = float(input("Lifestyle (max RM2500): ") or 0)
        education = float(input("Education Fees (max RM7000): ") or 0)
        parental = float(input("Parental Care (max RM5000): ") or 0)

        total_relief = (
            individual +
            min(spouse, 4000) +
            child_relief +
            min(medical, 8000) +
            min(lifestyle, 2500) +
            min(education, 7000) +
            min(parental, 5000)
        )

        print(f"\nTotal Tax Relief Claimed: RM{total_relief:.2f}")
        return total_relief

    except ValueError:
        print("Invalid input detected. Using default RM9000 individual relief only.")
        return 9000
