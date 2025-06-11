import tkinter as tk
from tkinter import ttk, messagebox
import requests

# --- API Configuration ---
API_KEY = "Your API Key"  # Replace with your actual API key
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

# --- Supported Currencies ---
CURRENCIES = ["USD", "INR", "EUR", "GBP", "JPY", "CAD", "AUD", "CNY", "NZD", "CHF", "SGD"]

# --- Currency Conversion Function ---
def convert_currency():
    try:
        from_curr = from_currency.get()
        to_curr = to_currency.get()
        amount = float(amount_entry.get())

        if from_curr == "" or to_curr == "":
            raise ValueError("Currency selection is missing.")
        
        url = BASE_URL + from_curr
        response = requests.get(url)
        data = response.json()

        if data['result'] != 'success':
            raise Exception("Failed to fetch exchange rates.")

        rate = data['conversion_rates'].get(to_curr)
        if not rate:
            raise Exception("Target currency not supported.")

        converted = round(amount * rate, 2)
        result_label.config(text=f"{amount} {from_curr} = {converted} {to_curr}")
        history_list.insert(tk.END, f"{amount} {from_curr} → {converted} {to_curr}")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("Currency Converter 💱")
root.geometry("420x450")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# --- Title Label ---
tk.Label(root, text="Currency Converter", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# --- Amount Entry ---
tk.Label(root, text="Enter Amount:", bg="#f0f0f0").pack()
amount_entry = tk.Entry(root, width=20, justify="center")
amount_entry.pack(pady=5)

# --- From Currency Dropdown ---
tk.Label(root, text="From Currency:", bg="#f0f0f0").pack()
from_currency = ttk.Combobox(root, values=CURRENCIES, state="readonly", width=15, justify="center")
from_currency.set("USD")
from_currency.pack(pady=5)

# --- To Currency Dropdown ---
tk.Label(root, text="To Currency:", bg="#f0f0f0").pack()
to_currency = ttk.Combobox(root, values=CURRENCIES, state="readonly", width=15, justify="center")
to_currency.set("INR")
to_currency.pack(pady=5)

# --- Convert Button ---
convert_button = tk.Button(root, text="Convert", command=convert_currency, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
convert_button.pack(pady=15)

# --- Result Display ---
result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0")
result_label.pack(pady=10)

# --- Conversion History ---
tk.Label(root, text="Conversion History", bg="#f0f0f0").pack(pady=5)
history_list = tk.Listbox(root, height=8, width=40)
history_list.pack(pady=5)

# --- Start the App ---
root.mainloop()
