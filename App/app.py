"""
Init
"""
import customtkinter
from Logger.scripts import Logger


class Progress(customtkinter.CTkFrame):
    """
    teste
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.progress = customtkinter.CTkProgressBar(self)
        self.progress.grid(row=3, column=0, padx=20, pady=20,
                           sticky="nsew")

    def start(self):
        """Start the progress bar animation"""
        self.progress.start()

    def stop(self):
        """Stop the progress bar animation"""
        self.progress.stop()

    def set(self, value):
        """Set progress bar to specific value (0.0 to 1.0)"""
        self.progress.set(value)


class Text(customtkinter.CTkFrame):
    """
    teste
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.text = customtkinter.CTkLabel(self, text="", font=("Arial", 14))
        self.text.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    def insert(self, index, text):
        """Insert text at specified index"""
        self.text.configure(text=text)

    def set_text(self, text):
        """Set the text directly"""
        self.text.configure(text=text)


class TextBox(customtkinter.CTkFrame):
    """
    Custom TextBox wrapper for displaying script output
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.textbox = customtkinter.CTkTextbox(
            self,
            font=("Consolas", 11),
            wrap="word"
        )
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox.configure(state="disabled")

    def insert(self, text):
        """Insert text at the end"""
        self.textbox.configure(state="normal")
        self.textbox.insert("end", text)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def insert_line(self, text):
        """Insert text with newline"""
        self.insert(text + "\n")

    def clear(self):
        """Clear all text"""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")

    def set_text(self, text):
        """Replace all text"""
        self.clear()
        self.insert(text)

    def set_editable(self, editable=True):
        """Enable or disable editing"""
        state = "normal" if editable else "disabled"
        self.textbox.configure(state=state)


class App(customtkinter.CTk):
    """
    Main Application Class
    """

    def __init__(self):
        super().__init__()
        self.title("Flamingo App Logger")
        self.geometry("1000x500")
        self.grid_columnconfigure((0, 1), weight=1)

        self.logger = Logger()

        self.button = customtkinter.CTkButton(
            self, text="Start", command=self.adb, )
        self.button.place(relx=0.5, rely=0.5, anchor="center")

        self.progress = Progress(master=self)
        self.text = Text(master=self, fg_color='transparent')
        self.textbox = TextBox(master=self, fg_color='transparent')

    def adb(self):
        """
        Testing
        """
        self.button.place_forget()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        self.text.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0))
        self.text.insert("0.0", "Checking phone connection")
        self.progress.grid(row=1, column=0, columnspan=2,
                           padx=20, pady=(0, 20))

        self.progress.start()
        self.update()

        result = self.logger.start_adb()

        self.button.place_forget()
        self.progress.set(1)

        self.progress.grid_forget()

        self.text.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0))
        self.text.insert("0.0", "Phone connected successfully!")

        self.update()

        self.show_output(result)

    def show_output(self, result):
        """
        Output
        """
        self.text.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.textbox.grid(row=0, column=0, columnspan=2,
                          padx=20, pady=(20, 10), sticky="nsew")

        self.stop_button = customtkinter.CTkButton(
            self,
            text="Stop Logcat",
            command=self.stop_logging,
            fg_color="red"
        )
        self.stop_button.grid(row=1, column=0, columnspan=2,
                              padx=20, pady=(0, 20))

        if result:
            self.textbox.insert_line("=== Starting Logcat ===")
            self.textbox.insert_line(result.stdout)
            self.textbox.insert_line("=== Live Logs ===")

            self.logger.start_logcat(self.append_log)
        else:
            self.textbox.insert_line("=== Error ===")
            self.textbox.insert_line("Could not connect to device")

    def append_log(self, log_line):
        """
        Callback function to append logs to textbox
        """
        self.after(0, lambda: self.textbox.insert(log_line))

    def stop_logging(self):
        """
        Stop the logcat logging
        """
        self.logger.stop_logcat()
        self.textbox.insert_line("\n=== Logcat Stopped ===")
        self.stop_button.configure(state="disabled", text="Stopped")
