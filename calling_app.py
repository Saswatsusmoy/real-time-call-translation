import tkinter as tk
from tkinter import messagebox
from fonoster.sdk import Fonoster
import re

class CallingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calling App")
        self.root.geometry("300x200")
        
        # Phone number input
        self.phone_label = tk.Label(root, text="Enter Phone Number:")
        self.phone_label.pack(pady=10)
        
        self.phone_entry = tk.Entry(root)
        self.phone_entry.pack(pady=5)
        
        # Call button
        self.call_button = tk.Button(root, text="Call", command=self.make_call)
        self.call_button.pack(pady=20)
        
        # Initialize Fonoster client
        self.call_manager = Fonoster.CallManager()
        
    def validate_phone_number(self, phone):
        # Basic phone number validation
        pattern = re.compile(r'^\+?1?\d{10,12}$')
        return bool(pattern.match(phone))
    
    def make_call(self):
        phone_number = self.phone_entry.get().strip()
        
        if not self.validate_phone_number(phone_number):
            messagebox.showerror("Error", "Please enter a valid phone number")
            return
        
        try:
            # Make the call using Fonoster
            self.call_manager.call({
                "from": "YOUR_FONOSTER_NUMBER",  # Replace with your Fonoster number
                "to": phone_number,
                "webhook": "YOUR_WEBHOOK_URL",   # Replace with your webhook URL
                "ignoreE164Validation": True
            }).then(
                lambda result: messagebox.showinfo("Success", "Call initiated successfully")
            ).catch(
                lambda error: messagebox.showerror("Error", f"Call failed: {str(error)}")
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = CallingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
