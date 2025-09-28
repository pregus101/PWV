import sounddevice as sd
import numpy as np

import pygame

import sounddevice as sd

import sounddevice as sd
import numpy as np
from scipy.fft import fft, fftfreq

import time

import pygame

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()

# Set up the display
screen_width = 1512
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Polygon Example")

size = 10

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

print(sd.query_devices())

def get_Wavebar_device_id():
    """Finds the device ID for Wavebar."""
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if "Wavebar" in device['name']:
            return i
    raise ValueError("Wavebar device not found. Did you install and set it up correctly?")

# --- CONFIGURATION ---
# Replace with the device ID of your loopback/stereo mix device
# Run 'print(sd.query_devices())' to find the correct device.
# For example, on Windows, it might be 'Stereo Mix' or 'Loopback'.
LOOPBACK_DEVICE_ID = get_Wavebar_device_id()  # Change this to your actual device ID
LOOPBACK_DEVICE_ID = 0

CHANNELS = 2             # Number of audio channels (e.g., stereo)
RATE = 96000             # Sample rate in Hz
BLOCKSIZE = 1024         # Number of frames per buffer
DURATION = 0.075
# ----------------------

print(f"Starting to capture audio from device ID: {LOOPBACK_DEVICE_ID}")

global times
times = 0

global trailer
trailer = []

for i in range(1, size+1):
        for j in range(20*i-20,20*i+20+1):
            trailer.append(870)
            print(j, len(trailer)+1)

# Define the callback function that will be called for each audio block
def callback(indata, frames, time, status):
    global times
    # if status:
        # print(status)\
        
    yf = fft(indata[:, 0])
    
    # Process the audio data here
    # `indata` is a NumPy array of shape (frames, channels)
    # The data is raw audio data (e.g., amplitude values)
    # print(f"Captured a block of audio data with shape: {indata.shape}")
    # print(f"Sample data (first 10 frames): {indata[:10, 0]}") # Print first channel

    nco = 870

    pygame.draw.rect(screen, (0,0,0), (0, 0, 1512, 900), 0) 

    for i in range(1, size+1):

        for j in range(20*i,20*i+20+1):
            # nc.append((int((j-20)*((1512/size)/20)), 870-int(np.abs(yf[j]))))

            print(int((j-20)*((1512/size)/20))+2, (870-int(np.abs(yf[j]))), -(int((j-20)*((1512/size)/20))-int((j-20)*((1512/size)/20))-2), 870-(870-int(np.abs(yf[j]))), j, len(trailer))

            pygame.draw.rect(screen, (122, 52, 235), (int((j-20)*((1512/size)/20))+2, (870-int(np.abs(yf[j]))), -(int((j-20)*((1512/size)/20))-int((j-20)*((1512/size)/20))-2), 870-(870-int(np.abs(yf[j])))))
            
            print(trailer[j])
            if  (870-int(np.abs(yf[j]))) <= trailer[j]:
                trailer[j] = (870-int(np.abs(yf[j])))
            else:
                try:
                    # if int(pygame.time.get_ticks()/(60*times)) >= 0.5:
                    #     if trailer[j] < 870:
                    #         trailer[j] += 1
                    trailer[j] += 10
                    pass
                except:
                    pass
                pass
            try:
                pygame.draw.rect(screen, (122, 255, 235), (int((j-20)*((1512/size)/20))+2, 870-(870-trailer[j])-1, -(int((j-20)*((1512/size)/20))-int((j-20)*((1512/size)/20))-2), 2))
                print(((870-trailer[j])-1, 2))
            except:
                pass

    pygame.display.flip()
    try:
        print(pygame.time.get_ticks(), int(pygame.time.get_ticks()/(60*times)))
    except:
        print(pygame.time.get_ticks(), pygame.time.get_ticks()/60)
    clock.tick(240)
    times += 1


try:
    with sd.InputStream(
        device=LOOPBACK_DEVICE_ID,
        samplerate=RATE,
        channels=CHANNELS,
        blocksize=int(RATE*DURATION),
        callback=callback
    ):
        print("\nCapturing... Press Ctrl+C to stop.")
        sd.sleep(999999)  # Keep the stream open indefinitely
except Exception as e:
    print(f"\nError: {e}")