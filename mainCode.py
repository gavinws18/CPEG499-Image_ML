import tkinter as tk
import subprocess
import os

os.chdir("/home/seniordesign/Documents/seniordesign")

def run_program1():
    # Run program 1
    subprocess.Popen(["python", "tkintertest.py"])

def run_program2():
    # Run program 2
    subprocess.Popen(["python", "blockText.py"])

def run_program3():
    # Run program 3
    subprocess.Popen(["python", "singleWord.py"])

def run_program4():
    # Run program 4
    subprocess.Popen(["python", "singleLine.py"])

def run_program5():
    # Run program 5
    subprocess.Popen(["python", "columnText.py"])

def stop_program():
    # Close the program
    root.destroy()

# Create the main Tkinter window
root = tk.Tk()
root.title("Program Selector")

# Set the window to full screen
root.attributes('-fullscreen', True)

# Create and pack the buttons
button1 = tk.Button(root, text="Default", command=run_program1)
button1.pack(side=tk.TOP, pady=(150, 10))

button2 = tk.Button(root, text="Block Text", command=run_program2)
button2.pack(side=tk.TOP, pady=10)

button3 = tk.Button(root, text="Single Word", command=run_program3)
button3.pack(side=tk.TOP, pady=10)

button4 = tk.Button(root, text="Single Line", command=run_program4)
button4.pack(side=tk.TOP, pady=10)

button5 = tk.Button(root, text="Column Text", command=run_program5)
button5.pack(side=tk.TOP, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_program)
stop_button.pack(side=tk.BOTTOM, pady=(10, 50))

# Run the Tkinter event loop
root.mainloop()
