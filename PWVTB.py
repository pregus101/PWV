import sounddevice as sd
import numpy as np

import pygame

import sounddevice as sd

import sounddevice as sd
import numpy as np
from scipy.fft import fft, fftfreq

import time

import pygame

import subprocess

def get_current_spotify_track():
    script = """
    tell application "Spotify"
        if it is running then
            if player state is playing then
                set trackName to name of current track
                set artistName to artist of current track
                return trackName & " by " & artistName
            else
                return "Spotify is paused or stopped."
            end if
        else
            return "Spotify is not running."
        end if
    end tell
    """
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing AppleScript: {e}"
    except FileNotFoundError:
        return "osascript command not found. macOS is required."

if __name__ == "__main__":
    current_track_info = get_current_spotify_track()
    print(f"Currently playing on Spotify: {current_track_info}")

# Initialize Pygame
pygame.init()
pygame.font.init() # Initialize the font module

font = pygame.font.SysFont('Arial', 30)

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

global get
get = 0

global gotton
gotton = get_current_spotify_track()

global trailer
trailer = []

for i in range(1, size+1):
        for j in range(20*i-20,20*i+20+1):
            trailer.append(870)
            print(j, len(trailer)+1)

global mainb
mainb = []

for i in range(1, size+1):
        for j in range(20*i-20,20*i+20+1):
            mainb.append(870)
            print(j, len(mainb)+1)

# Define the callback function that will be called for each audio block
def callback(indata, frames, time, status):
    global times
    global get
    global gotton
        
    yf = fft(indata[:, 0])

    pygame.draw.rect(screen, (0,0,0), (0, 0, 1512, 900), 0) 

    for i in range(1, size+1):

        for j in range(20*i,20*i+20+1):

            print(int((j-20)*((1512/size)/20))+2, (870-int(np.abs(yf[j]))), -(int((j-20)*((1512/size)/20))-int((j-20)*((1512/size)/20))-2), 870-(870-int(np.abs(yf[j]))), j, len(trailer))

            pygame.draw.rect(screen, (122, 52, 235), (int((j-20)*((1512/size)/20))+2, (870-int(np.abs(yf[j]))), -(int((j-20)*((1512/size)/20))-int((j-20)*((1512/size)/20))-2), 870-(870-int(np.abs(yf[j])))))
            
            print(trailer[j])
            if  (870-int(np.abs(yf[j]))) <= trailer[j]:
                trailer[j] = (870-int(np.abs(yf[j])))
            else:
                try:
                    trailer[j] += 8
                    pass
                except:
                    pass
                pass
            try:
                pygame.draw.rect(screen, (122, 255, 235), (int((j-20)*((1512/size)/20))+2, 870-(870-trailer[j])-1, -(int((j-20)*((1512/size)/20))-int((j-20)*((1512/size)/20))-2), 2))
                print(((870-trailer[j])-1, 2))
            except:
                pass

    text = font.render(gotton, True, (122, 52, 235))
    screen.blit(text, (50, 50))

    try:
        if pygame.time.get_ticks()/(60*times) >= 1:
            global get
            get += 1
            if get == 120:
                # global gotton
                gotton = get_current_spotify_track()
                get = 0
    except:
        print("fail")

    pygame.display.flip()
    try:
        print(pygame.time.get_ticks(), int(pygame.time.get_ticks()/(60*times)), get, times)
    except:
        print(pygame.time.get_ticks(), pygame.time.get_ticks()/60)
    clock.tick(1920)
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