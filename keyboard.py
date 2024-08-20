import tkinter as tk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("Virtual Keyboard")
root.geometry("800x400")

# Create a text field to display the output
text_field = tk.Entry(root, font=("Helvetica", 24), width=50)
text_field.grid(row=0, column=0, columnspan=10)

# Function to update the text field when a key is pressed
def on_key_press(key):
    current_text = text_field.get()
    text_field.delete(0, tk.END)
    text_field.insert(0, current_text + key)

# Function to handle special keys like backspace
def on_backspace():
    current_text = text_field.get()
    text_field.delete(0, tk.END)
    text_field.insert(0, current_text[:-1])

# Function to clear the text field
def on_clear():
    text_field.delete(0, tk.END)

# Function to show a message box when Enter is pressed
def on_enter():
    messagebox.showinfo("Virtual Keyboard", f"You entered: {text_field.get()}")
    on_clear()

# Create the buttons for the keyboard
keys = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Enter'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space']
]

# Add buttons to the grid layout
for row, key_row in enumerate(keys):
    for col, key in enumerate(key_row):
        if key == 'Backspace':
            button = tk.Button(root, text=key, width=10, height=2, command=on_backspace)
        elif key == 'Enter':
            button = tk.Button(root, text=key, width=10, height=2, command=on_enter)
        elif key == 'Space':
            button = tk.Button(root, text=key, width=40, height=2, command=lambda: on_key_press(' '))
        else:
            button = tk.Button(root, text=key, width=10, height=2, command=lambda key=key: on_key_press(key))
        
        button.grid(row=row+1, column=col, padx=5, pady=5)

# Run the Tkinter main loop
root.mainloop()
