import time

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
screen.title("wavebar")

# --- Configuration ---
# Set the sample rate. 44100 Hz is standard.
SAMPLE_RATE = 98000 # 176400 92000
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

    screen.update()

    canvas = Canvas(screen, width=1512, height=870, bg='black')
    canvas.pack()

    wave = []

    try:
        size = int(sizeV.get())
    except:
        size = 10
    global sizeO
    sizeO = size

    def callback(indata, frames, time, status):
        global sizeO

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
        global nco
        nco = 870

        try:
            size = int(sizeV.get())
        except:
            size = 10

        try:
            for i in range(0,size):
                wave.append(canvas.create_polygon(0,0,fill="#7f00e0", outline='#7f00e0', width=4))

            for i in range(0, size+1):
                nc = []
                if i == 0:
                    nc.append(0)
                else:
                    nc.append((i*20-20)*((1512/size)/20))
                
                nc.append(870)
                if i == 1:
                    nc.append(0)
                else:
                    nc.append((i*20-20)*((1512/size)/20))
                nc.append(nco)
                
                for j in range(20*i,20*i+20+1):
                    nc.append(int((j-20)*((1512/size)/20)))
                    nc.append(870-int(np.abs(yf[j])))
                    nco = 870-int(np.abs(yf[j]))
                    # print(nc , j, (j-20)*((1512/size)/20), (i*20-20)*((1512/size)/20), i*20*((1512/size)/20))
                
                nc.append(i*20*((1512/size)/20))
                nc.append(870)
                canvas.coords(wave[i-1], nc)
        except:
            pass

        if sizeO != size:
            for i in range(0,len(wave)):
                canvas.coords(wave[i], 0, 0)
        sizeO = size
        
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
            sd.sleep(0) #runs indefenitly
            screen.update()
        print("Streaming stopped.")

#Setting Screen Size
screen.geometry("740x740")

# bp = PhotoImage(file='apfp.png')

# bg_label = Label(screen, image=bp)
# bg_label.place(x=0, y=0, relwidth=1, relheight=1)


startB = Button(text='start',command=start)
startB.pack()

sizeV = StringVar()
sizeE = Entry(textvariable=sizeV)
sizeE.pack()

screen.grid_rowconfigure(0, weight=1)

screen.mainloop()