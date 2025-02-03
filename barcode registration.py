import tkinter as tk
from tkinter import messagebox

def get_country(barcode):
    country_codes = {
        "00": "USA",
        "01": "USA",
        "02": "USA",
        "03": "USA",
        "04": "USA",
        "05": "USA",
        "06": "USA",
        "07": "USA",
        "08": "Canada",
        "09": "USA or Canada",
        "30": "France",
        "31": "France",
        "32": "France",
        "33": "France",
        "34": "Spain",
        "35": "Spain",
        "36": "Hungary",
        "37": "Germany",
        "40": "Germany",
        "41": "Germany",
        "42": "Germany",
        "45": "Japan",
        "46": "Russia",
        "49": "Japan",
        "50": "United Kingdom",
        "60": "South Africa",
        "61": "South Africa",
        "64": "Finland",
        "70": "Norway",
        "73": "Sweden",
        "76": "Switzerland",
        "77": "Mexico",
        "80": "Italy",
        "81": "Italy",
        "84": "Spain",
        "87": "Netherlands",
        "89": "Brazil",
        "90": "Austria",
        "93": "Australia",
        "94": "New Zealand",
        "99": "Coupon Codes"
    }
    
    prefix = barcode[:2]  # Extract the first two digits
    return country_codes.get(prefix, "Unknown Country")

def lookup_country():
    barcode = entry.get()
    if not barcode.isdigit() or len(barcode) < 2:
        messagebox.showerror("Error", "Please enter a valid barcode number.")
        return
    
    country = get_country(barcode)
    messagebox.showinfo("Country Lookup", f"The barcode belongs to: {country}")

# Create GUI
root = tk.Tk()
root.title("Barcode Country Lookup")
root.geometry("300x150")

label = tk.Label(root, text="Enter Barcode Number:")
label.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

button = tk.Button(root, text="Lookup Country", command=lookup_country)
button.pack(pady=10)

root.mainloop()
