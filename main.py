import functions
import pandas as pd
import os

USERS_FILE = "users.csv"
TAX_DATA_FILE = "tax_data.csv"

def load_users():
    if os.path.exists(USERS_FILE):
        df = pd.read_csv(USERS_FILE, dtype={'IC Number': str})
        return dict(zip(df['User ID'], df['IC Number']))
    return {}

def save_user(user_id, ic_number):
    new_entry = pd.DataFrame([[user_id, ic_number]], columns=['User ID', 'IC Number'])
    if os.path.exists(USERS_FILE):
        new_entry.to_csv(USERS_FILE, mode='a', index=False, header=False)
    else:
        new_entry.to_csv(USERS_FILE, mode='w', index=False, header=True)

def main():
    print("=== Welcome to Malaysia Tax Calculator ===")
    users = load_users()
    user_id = input("Enter your User ID: ")

    if user_id not in users:
        print("\n--- New User Registration ---")
        while True:
            ic = input("Enter your 12-digit IC Number: ")
            password = input("Set your password (last 4 digits of IC): ")
            if functions.verify_user(ic, password):
                save_user(user_id, ic)
                users[user_id] = ic
                print("Registration successful.")
                break
            else:
                print("Invalid IC or password. Please try again.")

        # Prompt for login
        input_pwd = input("Re-enter your password to log in: ")
        if not functions.verify_user(ic, input_pwd):
            print("Login failed.")
            return
    else:
        ic = users[user_id]
        input_pwd = input("Enter your password (last 4 digits of IC): ")
        if not functions.verify_user(ic, input_pwd):
            print("Login failed.")
            return

    # Collect income and reliefs
    try:
        income = float(input("\nEnter your annual income (RM): "))
        relief = functions.gather_tax_reliefs()
    except ValueError:
        print("Invalid numeric input. Exiting.")
        return

    # Calculate and display tax
    tax = functions.calculate_tax(income, relief)
    print(f"\nYour calculated tax payable: RM{tax:.2f}")

    # Save data to CSV
    user_data = [ic, income, relief, tax]
    functions.save_to_csv(user_data, TAX_DATA_FILE)
    print("Your data has been saved to the tax data file.")

    # Display all tax records
    print("\n=== All Tax Records ===")
    records = functions.read_from_csv(TAX_DATA_FILE)
    if records is not None:
        print(records.to_string(index=False))
    else:
        print("No records found.")

if __name__ == "__main__":
    main()
