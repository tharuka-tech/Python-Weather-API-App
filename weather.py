from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

# Initialize the main window
root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)
root.configure(bg='lightblue')  # Set the desired background color



def get_weather_data(city):
    api_key = 'replace your api key'
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(api_url, timeout=20)
        response.raise_for_status() #If sucessful request
        return response.json()
    except requests.exceptions.Timeout:
        messagebox.showerror("Error", "Request timed out. Please try again later.")
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            messagebox.showerror("Error", "City not found in the weather API.")
        elif response.status_code == 401:
            messagebox.showerror("Error", "Invalid API key.")
        elif response.status_code == 403:
            messagebox.showerror("Error", "Access forbidden. Check your API key and its restrictions.")
        else:
            messagebox.showerror("Error", f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        messagebox.showerror("Error", f"Error occurred: {req_err}")    
    return None





def getweather():
    try:
        city = textfield.get()
        
        # Geolocation
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city, language='en', timeout=10)
        if not location:
            messagebox.showerror("Error", "City Not Found.")
            return

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        
        # Timezone and local time
        home = pytz.timezone(result)
        localTime = datetime.now(home)
        currentTime = localTime.strftime("%I:%M %p")
        currentDay = localTime.strftime("%A")
        
        clock.config(text=currentTime)
        day_label.config(text=f"Today is {currentDay}")
        name.config(text="CURRENT WEATHER", font=("Helvetica", 18, "bold")) 

        
        

        # Fetch weather data
        weather_data = get_weather_data(city)
        
        if weather_data:
            condition = weather_data['weather'][0]['main'] if 'weather' in weather_data and weather_data['weather'] else 'N/A'
            description = weather_data['weather'][0]['description'] if 'weather' in weather_data and weather_data['weather'] else 'N/A'
            temp = int(weather_data['main']['temp'] - 273.15) if 'main' in weather_data and 'temp' in weather_data['main'] else 'N/A'
            pressure = weather_data['main']['pressure'] if 'main' in weather_data and 'pressure' in weather_data['main'] else 'N/A'
            humidity = weather_data['main']['humidity'] if 'main' in weather_data and 'humidity' in weather_data['main'] else 'N/A'
            wind = weather_data['wind']['speed'] if 'wind' in weather_data and 'speed' in weather_data['wind'] else 'N/A'

            tmp.config(text=f"{temp}°C")
            con.config(text=f"{condition} | FEELS LIKE {temp}°C")

            wi.config(text=wind)
            hm.config(text=humidity)
            ds.config(text=description)
            pr.config(text=pressure)
        else:
            messagebox.showerror("Error", "Failed to retrieve weather data try again.")
    

    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")




# Search box
searchImage = PhotoImage(file="search.png")
myImage = Label(root, image=searchImage, bg='lightblue')
myImage.place(x=20, y=50)

textfield = tk.Entry(root, justify="center", width=20, font=("poppins", 18, "bold"), bg="goldenrod1", border=0, fg="white")
textfield.place(x=76, y=60)
textfield.focus()

searchIcon = PhotoImage(file="sicon.png")
myImageIcon = Button(root, image=searchIcon, borderwidth=0, cursor="hand2", bg="lightblue", command=getweather)
myImageIcon.place(x=20, y=51)

# Logo
logoImg = PhotoImage(file="main.png")
logo = Label(root, image=logoImg, bg='lightblue')
logo.place(x=110, y=120)


# Time and Date
name = Label(root, font=("Helvetica", 15, "bold"), bg='lightblue')
name.place(x=600, y=50)

clock = Label(root, font=("Helvetica", 18), bg='lightblue')
clock.place(x=600, y=80)

day_label = Label(root, font=("Helvetica", 18), bg='lightblue')
day_label.place(x=600, y=110)


# Bottom Box
frameImg = PhotoImage(file="footer.png")
botomImg = Label(root, image=frameImg, bg='#0F52BA')
botomImg.pack(padx=5, pady=1, side=BOTTOM)


# Labels
label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

tmp = Label(root, font=("arial", 60, "bold"), fg="#EE666D", bg='lightblue')
tmp.place(x=600, y=160)

con = Label(root, font=("arial", 15, 'bold'), bg='lightblue')
con.place(x=600, y=250)

wi = Label(root, text=" ... ", font=("arial", 20, "bold"), bg="#1ab5ef")
wi.place(x=120, y=430)

hm = Label(root, text=" ... ", font=("arial", 20, "bold"), bg="#1ab5ef")
hm.place(x=280, y=430)

ds = Label(root, text="         ...", font=("arial", 20, "bold"), bg="#1ab5ef")
ds.place(x=400, y=430)

pr = Label(root, text=" ... ", font=("arial", 20, "bold"), bg="#1ab5ef")
pr.place(x=680, y=430)

# Start the Tkinter main loop
root.mainloop()
