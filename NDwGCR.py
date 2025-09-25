import sounddevice as sd
import numpy as np

from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext

from tkinter import *
from tkinter import filedialog

from scipy.fft import fft, fftfreq

screen = Tk()
screen.title("New spotify downloader")

#Setting Screen Size
screen.geometry("540x740")

#setting up bars
freq1S = ttk.Style()
freq1S.theme_use('clam')
freq1S.configure("violet.Vertical.TProgressbar", foreground='black', background='violet', highlightbackground = "black")
freq1 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=300,mode="determinate",takefocus=True)
freq1.grid(row=0,column=0)

freq2S = ttk.Style()
freq2S.theme_use('clam')
freq2S.configure("violet.Vertical.TProgressbar", foreground='black', background='violet', highlightbackground = "black")
freq2 = ttk.Progressbar(screen,orient=VERTICAL, style='violet.Vertical.TProgressbar', length=300,mode="determinate",takefocus=True)
freq2.grid(row=0,column=1)

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

    def callback(indata, frames, time, status):
        """This function is called for each audio block."""
        if status:
            print(status, flush=True)
        
        # Perform FFT on the audio data.
        # The audio data is a numpy array.
        n = len(indata)
        yf = fft(indata[:, 0]) # Use the first channel
        xf = fftfreq(n, 1 / SAMPLE_RATE)

        # We only care about the positive frequencies.
        # The FFT result is symmetric.
        positive_frequencies = xf[:n//2]
        magnitude = np.abs(yf[:n//2])

        print('frequencies', xf)
        print('test', xf[1])
        print('magnatudes', yf)


        

        # Find the dominant frequency and its magnitude.
        dominant_frequency_index = np.argmax(magnitude)
        dominant_frequency = positive_frequencies[dominant_frequency_index]
        dominant_magnitude = magnitude[dominant_frequency_index]

        # print(f"Dominant Frequency: {dominant_frequency:.2f} Hz, Magnitude: {dominant_magnitude:.2f}")
        
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
            sd.sleep(10 * 1000) # Run for 10 seconds. Increase this for a longer period.
        print("Streaming stopped.")

    freq1.config(maximum=200)
    freq1['value']= yf[1]
    screen.update_idletasks()
    screen.after(0.0000000001)

startB = Button(command=start)
startB.grid()

screen.mainloop()