import sounddevice as sd
import numpy as np
from scipy.fft import fft
import time
import pygame
import subprocess
import urllib.request
from urllib.parse import urlparse, parse_qs
from youtubesearchpython import VideosSearch
import os
from PIL import Image
import threading 
import platform # <-- New Import
import sys      # <-- New Import

# Conditional imports for Windows/Linux
# On Windows, we need 'win32gui' for window title, but 'pygetwindow' is often cleaner.
# Since we are focusing on minimal changes, I'll use a simple window title check for Windows.
if platform.system() == "Windows":
    try:
        import win32gui
    except ImportError:
        print("Note: On Windows, you might need to install 'pywin32' (pip install pywin32) for the Spotify check to work reliably.")
        win32gui = None
elif platform.system() == "Linux":
    # Placeholder for Linux dependencies if needed later
    pass
    

# Initialize a lock for thread-safe data access
data_lock = threading.Lock() 

# ... (Original utility functions remain the same) ...

def get_youtube_id(url, ignore_playlist=True):
    # ... (content remains the same) ...
    if 'youtu.be' in url:
        path = urlparse(url).path
        return path.lstrip('/')
    elif 'youtube.com' in url:
        query = urlparse(url).query
        if query:
            query_params = parse_qs(query)
            if 'v' in query_params:
                video_id = query_params['v'][0]
                if ignore_playlist and '&list=' in url:
                    return video_id.split('&')[0]
                return video_id
    return None

def search(term):
    searcher = VideosSearch(term, 1)
    result = searcher.result()
    video = []
    for video_data in result['result']:
        video.append(video_data['link'])
    return video

# Global variables for shared state
global Song, gotton, color, mainb, trailer, wait1, wait2, size, times
Song = ''
gotton = ''
color = (0, 0, 0) # Default color
times = 0
size = 10

def get_song_image():
    # ... (content remains the same) ...
    global Song
    global gotton
    image_out = str(os.getcwd()) + "/temp.jpg"

    if Song != gotton and gotton not in ["Spotify is paused or stopped.", "Spotify is not running.", "Error executing AppleScript: 1:47: execution error: Application failed to initialize. (-10810)", "Spotify not playing."]:
        try:
            video_url = search(gotton)[0]
            video_id = get_youtube_id(video_url)
            print(f"Fetching image for: {gotton}")

            if video_id:
                try:
                    # Try high resolution first
                    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
                    urllib.request.urlretrieve(thumbnail_url, image_out)
                except:
                    # Fallback to default resolution
                    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/default.jpg'
                    urllib.request.urlretrieve(thumbnail_url, image_out)

                try:
                    image = Image.open(image_out)
                    new_size = (1512, 900)
                    resized_image = image.resize(new_size)
                    resized_image.save(image_out)
                except Exception as e:
                    print(f"Error resizing image: {e}")
            
            Song = gotton
        except Exception as e:
            print(f"Error during image fetch/resize: {e}")
            Song = gotton # Still mark as 'gotten' to avoid re-running immediately
    # else:
    #     print("skip")

def get_avg_img_col():
    # ... (content remains the same) ...
    try:
        image = Image.open(str(os.getcwd()) + "/temp.jpg")
        image_array = np.array(image)

        average_color_per_channel = np.average(image_array, axis=(0, 1))
        
        average_color = tuple(map(int, average_color_per_channel))

        return (255-average_color[0], 255-average_color[1], 255-average_color[2])
    except:
        return (122, 255, 235) # Default text color if image fails

# -------------------------------------------------------------
# 🌟 CROSS-PLATFORM SPOTIFY TRACK FUNCTION 🌟
# -------------------------------------------------------------
def get_current_spotify_track():
    """Gets the current Spotify track title based on the operating system."""
    system = platform.system()
    
    if system == "Darwin": # macOS
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
        except Exception:
            return "Spotify is not running."

    elif system == "Windows":
        # Check the window title for the song name
        if win32gui:
            window_name = win32gui.GetWindowText(win32gui.FindWindow("SpotifyMainWindow", None))
            # The window title is usually "Artist - Song Name" or just "Spotify" if paused/stopped
            if window_name and ' - ' in window_name:
                return window_name
            elif window_name == "Spotify":
                return "Spotify is paused or stopped."
            else:
                return "Spotify is not running."
        return "Spotify is not running." # Fallback if win32gui failed to import

    else:
        # Default for other systems (Linux, etc.)
        return "Spotify status unavailable on this OS."

# -------------------------------------------------------------
# 🌟 CROSS-PLATFORM AUDIO DEVICE FUNCTION 🌟
# -------------------------------------------------------------
def get_loopback_device_id():
    """Finds the device ID for a loopback device based on the operating system."""
    system = platform.system()
    devices = sd.query_devices()
    
    if system == "Darwin": # macOS
        search_terms = ["BlackHole", "Wavebar"]
        
    elif system == "Windows":
        # Common loopback device names on Windows
        search_terms = ["Stereo Mix", "What U Hear", "Loopback"]
        
    else: # Linux/Other
        # Common Linux/PulseAudio names for loopback/monitor
        search_terms = ["Monitor", "Loopback"]

    for i, device in enumerate(devices):
        for term in search_terms:
            if term in device['name']:
                print(f"Found loopback device: {device['name']}")
                return i
                
    # Fallback: Try finding the default input device
    try:
        default_device_name = sd.query_devices(sd.default.device[0])['name']
        print(f"Warning: Loopback device not found. Using default input device: {default_device_name}")
        return sd.default.device[0]
    except Exception:
        raise ValueError(f"Loopback audio device not found for {system}. Please ensure a loopback device (like Stereo Mix/BlackHole) is installed and enabled.")

# --- CONFIGURATION ---
try:
    LOOPBACK_DEVICE_ID = get_loopback_device_id()
except ValueError as e:
    print(e)
    LOOPBACK_DEVICE_ID = None 
    if platform.system() == "Windows":
        print("\n**Action Required on Windows:** You likely need to enable 'Stereo Mix' or install a virtual cable.")
        
CHANNELS = 2
RATE = 96000
BLOCKSIZE = 1024
DURATION = 0.075
# ----------------------

# Initialize Pygame and Globals
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()
screen_width = 1512
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Audio Visualizer")

# Initialize global arrays for visualizer bars
trailer = []
wait1 = []
wait2 = []
mainb = []

for i in range(1, size+1):
        for j in range(20*i-20,20*i+20+1):
            trailer.append(830)
            wait1.append(120)
            wait2.append(0)
            mainb.append(870) # Initial bar height (zero amplitude)

# --- THREADING TASKS (Remain the same structure) ---

# 1. Background task for checking Spotify and fetching images
def song_update_task():
    global gotton
    global color
    
    # Run initial setup
    new_track_info = get_current_spotify_track()
    if new_track_info != gotton:
        gotton = new_track_info
        get_song_image()
        color = get_avg_img_col()
    
    # Main loop for periodic updates
    while True:
        try:
            new_track_info = get_current_spotify_track()
            
            if new_track_info != gotton:
                print(f"Song changed to: {new_track_info}")
                gotton = new_track_info
                
                get_song_image()
                color = get_avg_img_col()
            
        except Exception as e:
            print(f"Error in song update thread: {e}")

        # Wait 5 seconds before checking again
        time.sleep(5)

# 2. Audio callback function (only processes audio and updates shared data)
def callback(indata, frames, time, status):
    global mainb
    global size
    
    yf = fft(indata[:, 0])

    with data_lock:
        bar_index = 0
        for i in range(1, size + 1):
            for j in range(20 * i, 20 * i + 20 + 1):
                if bar_index < len(mainb):
                    mainb[bar_index] = (870 - int(np.abs(yf[j])))
                bar_index += 1

# 3. Main Pygame Loop (handles drawing, events, and decay logic)
def main_loop():
    global times
    global gotton, color, mainb, trailer, wait1
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # --- DRAWING ---
        try:
            image = pygame.image.load(os.getcwd()+"/temp.jpg").convert_alpha()
            screen.blit(image, [(0,0),(screen_width, screen_height)])
        except pygame.error:
            screen.fill((0, 0, 0))

        with data_lock:
            bar_index = 0
            for i in range(1, size + 1):
                for j in range(20 * i, 20 * i + 20 + 1):
                    if bar_index >= len(mainb):
                        break

                    bar_height_y = mainb[bar_index] 
                    trailer_height_y = trailer[bar_index]

                    bar_x = int((j-20)*((screen_width/size)/20))+2
                    bar_w = 2 
                    bar_h = 870 - bar_height_y

                    # Draw the main bar
                    pygame.draw.rect(screen, color, (bar_x, bar_height_y, bar_w, bar_h))
                    
                    # Trailer Decay Logic
                    if bar_height_y <= trailer_height_y:
                        trailer[bar_index] = bar_height_y
                        wait1[bar_index] = 0
                    else:
                        if wait1[bar_index] < 10:
                            wait1[bar_index] += 1
                            pygame.draw.rect(screen, (122, 255, 235), (bar_x, trailer_height_y - 1, bar_w, 2))
                        else:
                            if trailer_height_y < 830:
                                if wait1[bar_index] < 110: 
                                    trailer[bar_index] += 2
                                    wait1[bar_index] += 1
                                    pygame.draw.rect(screen, (122, 255, 235), (bar_x, trailer_height_y - 1, bar_w, 2))
                                else:
                                    trailer[bar_index] = 830
                            else:
                                trailer[bar_index] = 830
                    
                    bar_index += 1
        
        # Draw text
        text = font.render(gotton, True, color)
        screen.blit(text, (50, 50))

        # Update display and tick clock
        pygame.display.flip()
        clock.tick(60)
        times += 1
        
    pygame.quit()
    print("Exiting application.")
    os._exit(0) 

# --- EXECUTION ---

if __name__ == "__main__":
    
    # 1. Start the Song/Image Update Thread
    song_thread = threading.Thread(target=song_update_task, daemon=True)
    song_thread.start()
    
    # 2. Start the Audio Stream
    if LOOPBACK_DEVICE_ID is not None:
        try:
            print(f"Starting to capture audio from device ID: {LOOPBACK_DEVICE_ID}")
            audio_stream = sd.InputStream(
                device=LOOPBACK_DEVICE_ID,
                samplerate=RATE,
                channels=CHANNELS,
                blocksize=int(RATE*DURATION),
                callback=callback
            )
            audio_stream.start()
            print("\nCapturing... Close the Pygame window to stop.")
            
            # 3. Run the Pygame Loop in the Main Thread
            main_loop()

        except Exception as e:
            print(f"\nError: {e}")
        finally:
            if 'audio_stream' in locals() and audio_stream.active:
                audio_stream.stop()
            pygame.quit()
    else:
        print("Could not start audio stream due to missing loopback device. Exiting.")
        sys.exit(1)