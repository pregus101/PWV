import sounddevice as sd
import numpy as np

import pygame

import sounddevice as sd

import sounddevice as sd
import numpy as np
from scipy.fft import fft, fftfreq

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
        if "BlackHole" in device['name']:
            return i
    raise ValueError("Wavebar device not found. Did you install and set it up correctly?")

# --- CONFIGURATION ---
# Replace with the device ID of your loopback/stereo mix device
# Run 'print(sd.query_devices())' to find the correct device.
# For example, on Windows, it might be 'Stereo Mix' or 'Loopback'.
LOOPBACK_DEVICE_ID = get_Wavebar_device_id()  # Change this to your actual device ID

CHANNELS = 2             # Number of audio channels (e.g., stereo)
RATE = 96000             # Sample rate in Hz
BLOCKSIZE = 1024         # Number of frames per buffer
DURATION = 0.075
# ----------------------

print(f"Starting to capture audio from device ID: {LOOPBACK_DEVICE_ID}")

# Define the callback function that will be called for each audio block
def callback(indata, frames, time, status):
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
        nc = []
        if i == i:
            nc.append((int((i*20-20)*((1512/size)/20)), 870))
        else:
            nc.append((0,(i*20-20)*((1512/size)/20)))

        if i == i:
            nc.append((int((i*20-20)*((1512/size)/20)), nco))
        else:
            nc.append(((i*20-20)*((1512/size)/20),nco))

        for j in range(20*i,20*i+20+1):
            if int((j-20)*((1512/size)/20)) != 1436:
                nc.append((int((j-20)*((1512/size)/20)), 870-int(np.abs(yf[j]))))
                pass
            else:
                nc.append((int((j-20)*((1512/size)/20)), 870))
                pass

            nco = int(870-int(np.abs(yf[j])))
            # print(nc , j, (j-20)*((1512/size)/20), (i*20-20)*((1512/10)/20), i*20*((1512/10)/20))
        
        nc.append((int(i*20*((1512/size)/20)), 870))
        # print(nc, nco)
        # print("\n\n\n")

        try:
            pygame.display.update(wave = pygame.draw.polygon(screen, (122, 52, 235), nc, 0)) # 5 pixels thick outline
        except:
            pass
    pygame.display.flip()
    clock.tick(1920)


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