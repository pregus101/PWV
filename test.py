import sounddevice as sd
import numpy as np
from scipy.fft import fft, fftfreq

import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1512
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Pygame Polygon Example")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define polygon points (a triangle)
# triangle_points = [(400, 100), (200, 400), (600, 400)]

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

# Fill the background
screen.fill(WHITE)
# Draw a filled polygon (red triangle)
# pygame.draw.polygon(screen, RED, triangle_points)

# Draw an outlined polygon (blue rectangle)
# Define rectangle points
# rectangle_points = [(100, 100), (300, 100), (300, 200), (100, 200)]

# --- Configuration ---
# Set the sample rate. 44100 Hz is standard.
SAMPLE_RATE = 44100
# Duration of each audio buffer in seconds.
DURATION = 0.09

clock = pygame.time.Clock()

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

size = 10

wave = pygame.draw.polygon(screen, (100, 0, 120), [(0, 870), (756, 870), (1512, 870)], 5)

def callback(indata, frames, time, status):
    """This function is called for each audio block."""
    if status:
        print(status, flush=True)
    
    # Perform FFT on the audio data.
    # The audio data is a numpy array.
    n = len(indata)
    yf = fft(indata[:, 0]) # Use the first channel
    xf = fftfreq(n, 1 / SAMPLE_RATE)

    print(xf[:n//2])
    print(yf[:n//2])

    # We only care about the positive frequencies.
    # The FFT result is symmetric.
    positive_frequencies = xf[:n//2]
    magnitude = np.abs(yf[:n//2])

        # for i in range(0,size):
        #         wave.append(canvas.create_polygon(0,0,fill="#7f00e0", outline='#7f00e0', width=4))

    nco = 870

    for i in range(0, 900):
        pygame.draw.rect(screen, (0,0,0), (0, 0, 1512, 900), 0) 

    for i in range(1, size+1):
        nc = []
        if i == i:
            nc.append((0, 870))
        else:
            nc.append((0,(i*20-20)*((1512/size)/20)))

        if i == i:
            nc.append((int((i*20-20)*((1512/size)/20)), nco))
        else:
            nc.append(((i*20-20)*((1512/size)/20),nco))

        for j in range(20*i,20*i+20+1):
            if int((j-20)*((1512/size)/20)) != 1436:
                nc.append((int((j-20)*((1512/size)/20)), 870-int(np.abs(yf[j]))))
            else:
                nc.append((int((j-20)*((1512/size)/20)), 870))
                pass

            nco = int(870-int(np.abs(yf[j])))
            # print(nc , j, (j-20)*((1512/size)/20), (i*20-20)*((1512/10)/20), i*20*((1512/10)/20))
        
        nc.append((int(i*20*((1512/size)/20)), 870))
        print(nc, nco)
        print("\n\n\n")

        try:
            pygame.display.update(wave = pygame.draw.polygon(screen, (100, 0, 120), nc, 0)) # 5 pixels thick outline
        except:
            pass
    pygame.display.flip()

    # clock.tick(60) # Limit to 60 frames per second

    # Update the display

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
        # screen.fill((0, 0, 0))
        sd.sleep(0)
    print("Streaming stopped.")

