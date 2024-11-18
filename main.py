import tkinter as tk
from tkinter import messagebox, Menu, StringVar
from screen_capture import start_screen_recording, stop_screen_recording, set_display_callback

# Initialize main window
root = tk.Tk()
root.title("Sentiment Analysis Application")
root.geometry("500x400")

# Global variable for status
status_text = StringVar()
status_text.set("Ready")

def start_recording():
    # Start screen recording for live chat analysis
    start_screen_recording()
    status_text.set("Recording started...")

def stop_recording():
    # Stop screen recording
    stop_screen_recording()
    status_text.set("Recording stopped.")
    messagebox.showinfo("Recording", "Screen recording stopped.")

def display_sentiment(sentiment):
    print(f"Live Chat Sentiment: {sentiment}")  # Debug
    result_label.config(text=f"Live Chat Sentiment: {sentiment}")

# Set up the callback for displaying sentiment analysis results
set_display_callback(display_sentiment)

# Add menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Start Recording", command=start_recording)
file_menu.add_command(label="Stop Recording", command=stop_recording)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About")

# Add status bar
status_bar = tk.Label(root, textvariable=status_text, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Main content
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="Real-Time Chat Sentiment Analysis", font=("Helvetica", 16)).pack(pady=10)
record_button = tk.Button(frame, text="Start Screen Recording", command=start_recording, bg="green", fg="white", font=("Helvetica", 12))
record_button.pack(pady=5)
stop_button = tk.Button(frame, text="Stop Recording", command=stop_recording, bg="red", fg="white", font=("Helvetica", 12))
stop_button.pack(pady=5)

result_label = tk.Label(frame, text="", fg="blue", font=("Helvetica", 14))
result_label.pack(pady=20)

root.mainloop()
