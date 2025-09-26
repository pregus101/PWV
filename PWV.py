import sounddevice as sd
import numpy as np

from PIL import Image, ImageTk

from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext

from tkinter import *
from tkinter import filedialog

from scipy.fft import fft, fftfreq

screen = Tk()
screen.title("New spotify downloader")

# --- Configuration ---
# Set the sample rate. 44100 Hz is standard.
SAMPLE_RATE = 96000
# Duration of each audio buffer in seconds.
DURATION = 0.09

def start():
    def get_blackhole_device_id():
        """Finds the device ID for BlackHole."""
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if "BlackHole" in device['name']:
                return i
        raise ValueError("BlackHole device not found. Did you install and set it up correctly?")

    try:
        blackhole_id = get_blackhole_device_id()
    except ValueError as e:
        print(e)
        exit()

    print(f"Using BlackHole device with ID: {blackhole_id}")

    global intial
    intial = True

    def callback(indata, frames, time, status):
        """This function is called for each audio block."""
        if status:
            print(status, flush=True)
        
        # Perform FFT on the audio data.
        # The audio data is a numpy array.
        n = len(indata)
        yf = fft(indata[:, 0]) # Use the first channel
        xf = fftfreq(n, 1 / SAMPLE_RATE)

        positive_frequencies = xf[:n//2]
        magnitude = np.abs(yf[:n//2])

        print('frequencies', xf)
        # print('test', yf[:n])
        print('magnatudes', yf)

        global intial

        if intial == True:
            global freqtest
            freqtest = []
            for i in range(0,85):
                if i > 42:
                    freqtest.append(ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600))
                    freqtest[i].grid(row=0,column=(85-(i)))
                    freqtest[i]['value']= np.abs(yf[i])
                else:
                    freqtest.append(ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600))
                    freqtest[i].grid(row=0,column=(85-(i-1)))
                    freqtest[i]['value']= np.abs(yf[i])
                    
            intial = False

        else:
            for i in range(0,85):
                freqtest[i]['value']= np.abs(yf[i])
        
    # Start the audio stream.
    with sd.InputStream(
        device=blackhole_id,
        samplerate=SAMPLE_RATE,
        channels=1, # BlackHole is a multi-channel device, but we can read from one channel.
        callback=callback,
        blocksize=int(SAMPLE_RATE * DURATION)
    ):
        
        print("Streaming started. Press Ctrl+C to stop.")
        while True:
            sd.sleep(0) # Run for 10 seconds. Increase this for a longer period.
            screen.update()
        print("Streaming stopped.")

#Setting Screen Size
screen.geometry("740x740")

# bg = PhotoImage(file='Tardis.png')

# bg_label = Label(screen, image=bg)
# bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#setting up bars

freq1S = ttk.Style()
freq1S.theme_use('clam')
freq1S.configure("violet.Vertical.TProgressbar", foreground='black', background='violet', highlightbackground = "black")
# freq1 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq1.grid(row=0,column=0)

# freq2 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq2.grid(row=0,column=1)

# freq3 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq3.grid(row=0,column=2)

# freq4 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq4.grid(row=0,column=3)

# freq5 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq5.grid(row=0,column=4)

# freq6 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq6.grid(row=0,column=5)

startB = Button(text='start',command=start)
startB.grid(row=1,column=43)

# freq7 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq7.grid(row=0,column=7)

# freq8 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq8.grid(row=0,column=8)

# freq9 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq9.grid(row=0,column=9)

# freq10 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq10.grid(row=0,column=10)

# freq11 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq11.grid(row=0,column=11)

# freq12 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=600,mode="determinate",takefocus=True, maximum=1600)
# freq12.grid(row=0,column=12)

screen.grid_columnconfigure(0, weight=1) 
screen.grid_columnconfigure(1, weight=1)   
screen.grid_columnconfigure(2, weight=1)  
screen.grid_columnconfigure(3, weight=1)  
screen.grid_columnconfigure(4, weight=1)  
screen.grid_columnconfigure(5, weight=1)  
screen.grid_columnconfigure(6, weight=1)  
screen.grid_columnconfigure(7, weight=1)  
screen.grid_columnconfigure(8, weight=1)  
screen.grid_columnconfigure(9, weight=1)  
screen.grid_columnconfigure(10, weight=1)  
screen.grid_columnconfigure(11, weight=1)  
screen.grid_columnconfigure(12, weight=1)  
screen.grid_rowconfigure(0, weight=1)  

screen.mainloop()