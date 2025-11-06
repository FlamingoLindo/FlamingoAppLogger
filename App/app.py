"""
Init
"""
import customtkinter
from Logger.scripts import Logger


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
            self, text="Start", command=self.start_adb, )
        self.button.place(relx=0.5, rely=0.5, anchor="center")

    def start_adb(self):
        """
        Testing
        """
        self.logger.start_adb()
        self.button.place_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
