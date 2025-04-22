import tkinter as tk
from tkinter import messagebox
import time


class TypingSpeed:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.start_time = None
        self.selected_key = None
        self.text = None

        # Set desired window size
        window_width = 700
        window_height = 700

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position for centering
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # Set geometry and position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Load texts from file
        self.texts_dict = self.load_texts_from_file("texts.txt")
        self.option_list = list(self.texts_dict.keys())

        # Label dropdown menu
        text_entry_label = tk.Label(
            self.root,
            text="Choose the text you want to use in your test:",
            font=("Arial", 14)
        )
        text_entry_label.pack(pady=(15, 5))

        # Dropdown menu
        self.selected_option = tk.StringVar(root)
        self.selected_option.set(self.option_list[0])
        self.dropdown = tk.OptionMenu(root, self.selected_option, *self.option_list)
        self.dropdown.config(width=9, font=("Arial", 16))
        self.dropdown.pack(pady=15)

        # Show selected text
        self.button_show_selected_text = tk.Button(text="Show Text", command=self.show_selected_text, width=10)
        self.button_show_selected_text.pack(pady=10)

        # Show the selected text
        self.text_display = tk.Text(self.root, height=6, width=100, font=("Arial", 14), wrap="word")
        self.text_display.configure(state="disabled")  # Initially disabled
        self.text_display.pack(pady=15)

        # Label input box
        text_entry_label = tk.Label(
            self.root,
            text="Press 'enter' or click the 'Submit' button to submit your test.",
            font=("Arial", 14)
        )
        text_entry_label.pack(pady=(15, 5))

        # Create typing input box
        self.typing_box = tk.Text(self.root, height=6, width=100, font=("Courier New", 12))
        self.typing_box.pack(pady=10)
        self.typing_box.bind("<KeyPress>", self.start_timer)
        self.typing_box.bind("<Return>", self.submit_on_enter)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_typing_result, width=10)
        self.submit_button.pack(pady=10)

        # Reset button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_test, width=10)
        self.reset_button.pack(pady=10)

        # Results label
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), fg="green")
        self.result_label.pack(pady=10)

    def load_texts_from_file(self, filename):
        texts = {}
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if '|' in line:
                    key, text = line.strip().split('|', 1)
                    texts[key] = text
        return texts

    def show_selected_text(self):
        self.selected_key = self.selected_option.get()
        self.text = self.texts_dict[self.selected_key]

        self.text_display.configure(state="normal")  # Allow editing so we can insert
        self.text_display.delete("1.0", tk.END)  # Clear existing text
        self.text_display.insert(tk.END, self.text)  # Insert the new paragraph
        self.text_display.configure(state="disabled")  # Disable again to prevent user editing

    def start_timer(self, event):
        if self.start_time is None:
            self.start_time = time.time()
            print("Timer started at:", self.start_time)  # Debug line

    def check_typing_result(self):
        end_time = time.time()
        time_taken = end_time - self.start_time if self.start_time else 0

        typed_text = self.typing_box.get("1.0", tk.END).strip()
        original_text = self.text.strip()

        # Words per minute
        word_count = len(typed_text.split())
        word_per_minute = word_count / (time_taken / 60) if time_taken > 0 else 0

        # Accuracy = how many words match
        original_words = original_text.split()
        typed_words = typed_text.split()

        correct = sum(ow == tw for ow, tw in zip(original_words, typed_words))
        accuracy = (correct / len (original_words)) * 100 if original_words else 0

        # Show result
        result = f"Time: {round(time_taken, 2)}s\n Words per Minute: {int(word_per_minute)}\nAccuracy: {int(accuracy)}%"
        result = (
            f"Time: {round(time_taken, 2)}s\n"
            f"Words per Minute: {int(word_per_minute)}\n"
            f"Accuracy: {int(accuracy)}%"
        )
        self.result_label.config(text=result)

        # Reset timer after submission
        # self.start_time = None

    def submit_on_enter(self, event):
        self.check_typing_result()
        return "break"

    def reset_test(self):
        # Clear typing box
        self.typing_box.delete("1.0", tk.END)

        # Reset timer
        self.start_time = None

        # Reset results
        self.result_label.config(text="")

        # Optionally clear the text that was shown
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.configure(state="disabled")

        # Reset selected text (optional — if you want to allow picking a new one)
        self.selected_key = None
        self.text = None



def run_app():
    window = tk.Tk()   # Create the main window
    app = TypingSpeed(window)   # Pass the window to our class
    window.mainloop()   # Start the interface loop

