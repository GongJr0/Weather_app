from backend import Backend
import customtkinter as ctk # type: ignore
from PIL import ImageTk, Image # type: ignore

class App(Backend):
    def __init__(self, master: ctk.CTk) -> None:
        # Initialize the backend
        super().__init__()
        
        # Initialize and configure the master window
        self.master = master
        self.master.title("Weather App")
        self.master.iconbitmap("./weather/icon.ico")
        
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        
        

        # Condition
        self.img = Image.open(self.get_current_icon())
        self.photo = ctk.CTkImage(self.img)
        self.photo.configure(size=(100, 100))
        
        self.condition_frame = ctk.CTkFrame(self.master)
        self.condition_image = ctk.CTkLabel(self.condition_frame, image=self.photo, text='')
        
        
        self.condition_text = ctk.CTkLabel(self.master, text=f"Condition: {self.get_condition()['text']}", font=("Helvetica", 20))
        
        self.condition_frame.pack()
        self.condition_image.pack()
        self.condition_text.pack()
        
        
        # Temperature
        self.temperature = ctk.CTkLabel(self.master, text=f"Temperature: {int(self.get_temperature())}\u2103", font=("Helvetica", 20))
        self.temperature.pack()
        
        

        
def main():
    root = ctk.CTk()
    app = App(root)
    app.master.mainloop()
    
if __name__ == "__main__":
    main()