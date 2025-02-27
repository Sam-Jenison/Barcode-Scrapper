import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import requests
import tkinter as tk
from tkinter import messagebox

# Create a hidden Tkinter root so we can show message boxes later without a blank window.
root = tk.Tk()
root.withdraw()

def lookup_open_food_facts(barcode):
    """
    Queries the Open Food Facts API for the given barcode.
    Returns a dict with product information if found, or None if not found.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            status = data.get('status')
            if status == 1:
                product_info = data.get('product', {})
                return product_info
    except requests.exceptions.RequestException as e:
        print(f"Error calling Open Food Facts: {e}")
    return None

def show_popup(product_name, brands, manufacturing_places, origins):
    """
    Show a blocking popup (message box) with product details.
    """
    info_text = (
        f"Name: {product_name}\n"
        f"Brand(s): {brands}\n"
        f"Manufacturing Places: {manufacturing_places}\n"
        f"Origins: {origins}"
    )
    messagebox.showinfo("Product Information", info_text)

def main():
    # Force DirectShow backend (often more reliable on Windows than MSMF).
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Cannot open webcam.")
        return

    print("Webcam opened. Press 'q' in the OpenCV window to quit.")

    # Keep track of barcodes we've already processed to avoid repetitive API calls.
    scanned_barcodes = set()

    # Restrict to barcode types you actually need (excluding PDF417 to avoid that bug).
    desired_symbols = [
        ZBarSymbol.EAN13,
        ZBarSymbol.EAN8,
        ZBarSymbol.UPCA,
        ZBarSymbol.UPCE,
        ZBarSymbol.CODE128,
        ZBarSymbol.CODE39,
        ZBarSymbol.QRCODE,
    ]

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        # Decode barcodes in the current frame, excluding PDF417.
        barcodes = decode(frame, symbols=desired_symbols)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8').strip()
            barcode_type = barcode.type

            # Only handle each unique barcode once
            if barcode_data not in scanned_barcodes:
                scanned_barcodes.add(barcode_data)
                print(f"Detected {barcode_type} barcode: {barcode_data}")

                # Lookup product info from Open Food Facts
                product_info = lookup_open_food_facts(barcode_data)
                if product_info:
                    product_name = product_info.get("product_name", "Unknown Product Name")
                    brands = product_info.get("brands", "Unknown Brand")
                    
                    # Check for optional fields:
                    manufacturing_places = product_info.get("manufacturing_places", "Not specified")
                    origins = product_info.get("origins", "Not specified")

                    # Pop out a window with the info
                    show_popup(product_name, brands, manufacturing_places, origins)
                else:
                    # If we found no info, still show a popup or handle gracefully
                    messagebox.showinfo("Product Information", "No product info found on Open Food Facts.")

        # Display the frame in an OpenCV window (optional)
        cv2.imshow('Press "q" to Quit', frame)

        # Press 'q' in the OpenCV window to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

