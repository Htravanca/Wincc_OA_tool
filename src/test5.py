import tkinter as tk
from tkinter import messagebox

# Function to protect input (limit to 255.255.255.255 or lower)
def validate_input(input_text):
    try:
        if '.' in input_text:  # Byte format
            parts = list(map(int, input_text.split('.')))
            if all(0 <= part <= 255 for part in parts):
                return True
        else:  # Integer format
            number = int(input_text)
            if 0 <= number <= 4294967295:  # 255.255.255.255 in decimal
                return True
        return False
    except ValueError:
        return False

# Function to convert integer to 3 or 4-byte format
def int_to_bytes_format(num):
    if num <= 65535:  # 3-byte format
        byte1 = num // 256
        byte2 = num % 256
        result = f"{byte1}.{byte2:03}"
        return result
    elif num <= 4294967295:  # 4-byte format
        byte1 = (num >> 24) & 0xFF
        byte2 = (num >> 16) & 0xFF
        byte3 = (num >> 8) & 0xFF
        byte4 = num & 0xFF
        # Display in a more concise format (e.g., 1.4.106)
        if byte1 == 0:
            result = f"{byte2}.{byte3}.{byte4}"
        else:
            result = f"{byte1}.{byte2}.{byte3}.{byte4}"
        return result
    else:
        return None

# Function to convert 3 or 4-byte format back to integer
def bytes_to_int(byte_str):
    parts = list(map(int, byte_str.split('.')))
    if len(parts) == 2:  # 3-byte format
        byte1, byte2 = parts
        return byte1 * 256 + byte2
    elif len(parts) == 4:  # 4-byte format
        byte1, byte2, byte3, byte4 = parts
        return (byte1 << 24) + (byte2 << 16) + (byte3 << 8) + byte4
    elif len(parts) == 3:  # Custom format 1.4.106
        byte1, byte2, byte3 = parts
        return (byte1 << 16) + (byte2 << 8) + byte3
    else:
        return None

# Function to handle conversion when button is clicked or Enter is pressed
def on_convert(event=None):
    input_text = entry.get()
    if validate_input(input_text):
        if '.' in input_text:
            result = bytes_to_int(input_text)
        else:
            result = int_to_bytes_format(int(input_text))
        if result is not None:
            result_label.config(text=f"Result: {result}")
            copy_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Invalid Input", "Conversion failed. Please check the input.")
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid integer or byte format within range.")

# Function to copy the result to clipboard without pop-up
def copy_to_clipboard():
    result_text = result_label.cget("text").replace("Result: ", "")
    root.clipboard_clear()
    root.clipboard_append(result_text)

# Function to clear the input field
def clear_input():
    entry.delete(0, tk.END)
    result_label.config(text="Result: ")
    copy_button.config(state=tk.DISABLED)

# Function to exit the program when ESC is pressed
def on_exit(event=None):
    root.destroy()

# Create main window
root = tk.Tk()
root.title("Int to IEC WinCC OA")
root.geometry("450x250")

# Add label and entry for input
label = tk.Label(root, text="Enter an Integer or Byte (e.g., 3050 or 1.4.106):", font=("Arial", 12))
label.pack(pady=10)

# Create frame for entry and clear button
entry_frame = tk.Frame(root)
entry_frame.pack(pady=4)

# Entry for user input
entry = tk.Entry(entry_frame, font=("Arial", 12), width=20)
entry.pack(side=tk.LEFT, padx=5)

# Add a button with a cross to clear the entry
clear_button = tk.Button(entry_frame, text="✕", font=("Arial", 11), command=clear_input)
clear_button.pack(side=tk.RIGHT, padx=4)

# Bind the Enter key to trigger the on_convert function
entry.bind('<Return>', on_convert)

# Bind the ESC key to exit the program
root.bind('<Escape>', on_exit)

# Add a button to trigger conversion
convert_button = tk.Button(root, text="Convert", command=on_convert, font=("Arial", 10), bg="lightblue", width=12)
convert_button.pack(pady=10)

# Add a label to show the result with a larger font size
result_label = tk.Label(root, text="Result: ", font=("Helvetica", 16), fg="black")
result_label.pack(pady=10)

# Add a copy button to copy the result to the clipboard without popup
copy_button = tk.Button(root, text="Copy", command=copy_to_clipboard, state=tk.DISABLED, font=("Arial", 10), bg="lightgreen", width=12)
copy_button.pack(pady=10)

# Run the application
root.mainloop()

