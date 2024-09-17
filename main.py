import tkinter as tk
from tkinter import ttk
import sv_ttk
import pyautogui
import threading
import keyboard  # New import for hotkey detection

class RocketLeagueMacro:
    def __init__(self, root):
        self.root = root
        self.is_enabled = False
        self.macros = {}  # Store key-message pairs
        self.team_chat_key = None
        self.public_chat_key = None

        # Set up the main window
        self.setup_window()

        # Set the dark theme
        sv_ttk.set_theme("dark")

        # Create the frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Add widgets to the frame
        self.create_widgets()

    def setup_window(self):
        # Calculate the window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = screen_width // 4
        window_height = screen_height // 3  # Adjust height to fit new elements
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Window settings
        self.root.title("Rocket League Macro")
        self.root.resizable(False, False)

    def create_widgets(self):
        # Create text entry fields for shortcut keys and chat messages
        self.entries = []
        for i in range(1, 6):
            # Entry for the shortcut key
            shortcut_key = ttk.Entry(self.frame, width=4)
            shortcut_key.grid(row=i, column=0, sticky=tk.W, padx=8, pady=8)
            shortcut_key.insert(0, f"F{i}")

            # Entry for the chat message
            chat_message = ttk.Entry(self.frame, width=40)
            chat_message.grid(row=i, column=1, columnspan=3, padx=8, pady=8)
            chat_message.insert(0, f"Chat Message {i}")

            self.entries.append((shortcut_key, chat_message))

        # Add a line to separate the chat macros from the team and public chat keys
        separator = ttk.Separator(self.frame, orient="horizontal", style="TSeparator")
        separator.grid(row=6, column=0, columnspan=4, sticky="ew", padx=8, pady=8)

        # Add team chat key entry
        team_chat_label = ttk.Label(self.frame, text="Team Chat Key:")
        team_chat_label.grid(row=7, column=0, sticky=tk.W, padx=0, pady=8)
        self.team_chat_entry = ttk.Entry(self.frame, width=4)
        self.team_chat_entry.grid(row=7, column=1, padx=8, pady=0)
        self.team_chat_entry.insert(0, "T")

        # Add public chat key entry
        public_chat_label = ttk.Label(self.frame, text="Public Chat Key:")
        public_chat_label.grid(row=8, column=0, sticky=tk.W, padx=0, pady=8)
        self.public_chat_entry = ttk.Entry(self.frame, width=4)
        self.public_chat_entry.grid(row=8, column=1, padx=8, pady=0)
        self.public_chat_entry.insert(0, "Y")

        # Separator for the chat keys
        separator2 = ttk.Separator(self.frame, orient="horizontal", style="TSeparator")
        separator2.grid(row=9, column=0, columnspan=4, sticky="ew", padx=8, pady=8)

        # Define custom styles for the toggle button
        style = ttk.Style()
        style.configure("Enabled.TButton", background="green")
        style.configure("Disabled.TButton", background="red")

        # Create a toggle button to enable/disable the chat macros
        self.toggle_button = ttk.Button(
            self.frame, text="Enable Macros", style="Disabled.TButton", command=self.change_status
        )
        self.toggle_button.grid(row=10, column=0, columnspan=4, padx=8, pady=8)

    def change_status(self):
        # Toggle the status
        self.is_enabled = not self.is_enabled

        # Update button text and style based on the status
        if self.is_enabled:
            self.toggle_button.config(text="Disable Macros", style="Enabled.TButton")
            self.load_macros()
            self.start_macro_listener()
        else:
            self.toggle_button.config(text="Enable Macros", style="Disabled.TButton")

    def load_macros(self):
        # Load the key-message pairs from the entries
        self.macros.clear()
        for key_entry, message_entry in self.entries:
            key = key_entry.get().strip()
            message = message_entry.get().strip()
            if key and message:
                self.macros[key] = message

        # Load the team and public chat keys
        self.team_chat_key = self.team_chat_entry.get().strip()
        self.public_chat_key = self.public_chat_entry.get().strip()

    def start_macro_listener(self):
        # Run the background listener on a separate thread
        listener_thread = threading.Thread(target=self.background_listener, daemon=True)
        listener_thread.start()

    def background_listener(self):
        # Listen for key presses and execute macros if enabled
        while self.is_enabled:
            for key, message in self.macros.items():
                if keyboard.is_pressed(key):
                    # Determine chat mode
                    chat_key = self.team_chat_key if self.is_team_only else self.public_chat_key
                    pyautogui.press(chat_key)
                    pyautogui.write(message)
                    pyautogui.press('enter')

            # Sleep for a short interval to avoid high CPU usage
            self.root.after(100)

def main():
    root = tk.Tk()
    app = RocketLeagueMacro(root)
    root.mainloop()

if __name__ == "__main__":
    main()
