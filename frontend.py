from backend import Backend

import os
import customtkinter as ctk # type: ignore
from PIL import Image, ImageTk # type: ignore
import datetime as dt # type: ignore

class App(Backend):
    def __init__(self, master: ctk.CTk) -> None:
        # Initialize the backend
        super().__init__()  
        # Initialize and configure the master window
        self.master = master
        self.master.title("Weather App")
        
        if os.environ.get('OS', '') == 'Windows_NT':
            self.master.iconbitmap("./weather/icon.ico")
            
        else:
            self.master.iconphoto(False, ImageTk.PhotoImage(Image.open("./weather/icon.png")))
            
        self.master.geometry("525x625")
        self.master.resizable(False, True)
        
        self.redner_info()
        self.render_additional_info()
        self.render_14_day_forecast()
        
    def redner_info(self) -> None:
        # Condition
        self.img = Image.open(self.get_current_icon())
        self.photo = ctk.CTkImage(self.img)
        self.photo.configure(size=(100, 100))
        
        self.today_title_frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.today_title_frame.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.today_title = ctk.CTkLabel(self.today_title_frame, text="Today's Forecast", font=("Helvetica", 20))
        self.today_title.grid(row=0, column=0, padx=5, pady=5)
        
        self.today_frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.today_frame.grid(row=1, column=0)
        
        self.condition_img_frame = ctk.CTkFrame(self.today_frame, corner_radius=10)
        self.condition_image = ctk.CTkLabel(self.condition_img_frame, image=self.photo, text='', corner_radius=10)
        
        self.condition_img_frame.grid(row=0, column=0, padx=5, pady=5)
        self.condition_image.grid(row=0, column=0, padx=5, pady=5)
        
        self.loc_obj = self.get_forecast()['location']
        self.loc = ctk.CTkLabel(self.condition_img_frame, text=f"{self.loc_obj['name']}, {self.loc_obj['country']}", font=("Helvetica", 10))
        self.loc.grid(row=1, column=0)
        
        self.info_frame = ctk.CTkFrame(self.today_frame, corner_radius=10)
        self.info_frame.grid(row=0, column=1)
        
        self.condition_text = ctk.CTkLabel(self.info_frame, text=f"{self.get_condition()['text']}", font=("Helvetica", 10))
        self.condition_text.grid(row=0, column=0)
        
        self.temperature = ctk.CTkLabel(self.info_frame, text=f"{int(self.get_temperature())}\u2103", font=("Helvetica", 25))
        self.temperature.grid(row=1, column=0)
        
        self.wind = ctk.CTkLabel(self.info_frame, text=f"Current Average Wind Speed: {self.get_wind()} km/h", font=("Helvetica", 10))
        self.wind.grid(row=2, column=0)
        
        
        
        return None
    
    def render_additional_info(self) -> None:
        self.additional_info_frame = ctk.CTkFrame(self.today_frame, corner_radius=10)
        self.additional_info_frame.grid(row=0, column=2, padx=5, pady=5)
        
        self.sunrise = ctk.CTkLabel(self.additional_info_frame, text=f"Sunrise: {self.get_sunrise()}", font=("Helvetica", 10), padx=5, pady=5)
        self.sunrise.grid(row=0, column=0)
        
        self.sunset = ctk.CTkLabel(self.additional_info_frame, text=f"Sunset: {self.get_sunset()}", font=("Helvetica", 10), padx=5, pady=5)
        self.sunset.grid(row=1, column=0)
        
        self.humidity = ctk.CTkLabel(self.additional_info_frame, text=f"Humidity: {self.get_humidity()}%", font=("Helvetica", 10), padx=5, pady=5)
        self.humidity.grid(row=0, column=1, sticky='e')
        
        self.gusts = ctk.CTkLabel(self.additional_info_frame, text=f"Gusts: {self.get_gusts()} km/h", font=("Helvetica", 10), padx=5, pady=5)
        self.gusts.grid(row=1, column=1, sticky='e')
        
        return None
        
        
        
    def render_14_day_forecast(self) -> None:    
        self.forecast_frame = ctk.CTkFrame(self.master)
        self.forecast_frame.grid(row=3, column=0, columnspan=7)
        self.forecasts = self.get_14_days_forecast()
        
        self.forecast_title_frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.forecasts_title = ctk.CTkLabel(self.forecast_title_frame, text="14-Day Forecast", font=("Helvetica", 20))
        
        self.forecast_title_frame.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.forecasts_title.grid(row=0, column=0, padx=5, pady=5)
        
        
        
        for i, (day, forecast) in enumerate(self.forecasts.items()):
            day_frame = ctk.CTkFrame(self.forecast_frame, corner_radius=10)
            
            day_image = Image.open(self.get_image("https:"+ forecast['icon']))
            day_photo = ctk.CTkImage(day_image)
            day_photo.configure(size=(50, 50))
            
            day_htemp = ctk.CTkLabel(day_frame, text=f"High: {int(forecast['maxtemp_c'])}\u2103", font=("Helvetica", 10))
            day_ltemp = ctk.CTkLabel(day_frame, text=f"Low: {int(forecast['mintemp_c'])}\u2103", font=("Helvetica", 10))
            
            day_image_label = ctk.CTkLabel(day_frame, image=day_photo, text='')
            
            day_title = ctk.CTkLabel(day_frame, text=dt.datetime.strptime(day, '%Y-%m-%d').strftime('%b %d'), font=("Helvetica", 15))
            
            if i < 7:
                day_title.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
                day_frame.grid(row=1, column=i, padx=5, pady=5, sticky='ew')
                day_image_label.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
                day_htemp.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
                day_ltemp.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
            else :
                day_title.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
                day_frame.grid(row=2, column=i-7, padx=5, pady=5, sticky='ew')
                day_image_label.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
                day_htemp.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
                day_ltemp.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        
        return None
        
def main():
    root = ctk.CTk()
    app = App(root)
    app.master.mainloop()
    
if __name__ == "__main__":
    main()