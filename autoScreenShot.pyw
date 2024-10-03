import pyautogui
from pynput import mouse, keyboard
import os
from datetime import datetime
import threading
import tkinter as tk
from tkinter import messagebox
import time

# Directory to save screenshots
save_dir = r"C:\TriggerBot\screenShots"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Flag to indicate if the script should stop
stop_flag = threading.Event()

# Variable to store the last screenshot time
last_screenshot_time = 0

def save_screenshot(image, path):
    """Save the screenshot in a separate thread to reduce blocking."""
    image.save(path)
    print(f"Screenshot saved as {path}")

def take_screenshot():
    global last_screenshot_time
    current_time = time.time()
    
    # Check if at least one second has passed since the last screenshot
    if current_time - last_screenshot_time >= 1:
        # Generate a filename based on the current time
        screenshot_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        screenshot_path = os.path.join(save_dir, screenshot_filename)
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        # Save the screenshot in a separate thread
        threading.Thread(target=save_screenshot, args=(screenshot, screenshot_path)).start()
        
        # Update the last screenshot time
        last_screenshot_time = current_time

def on_click(x, y, button, pressed):
    # Only take a screenshot on left-click
    if pressed and button == mouse.Button.left and not stop_flag.is_set():
        take_screenshot()

def on_press(key):
    # Stop the script when the Esc key is pressed
    if key == keyboard.Key.esc:
        stop_flag.set()
        return False  # Stop the listener

def start_mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def start_listeners():
    # Clear the stop flag to start the listeners
    stop_flag.clear()
    global mouse_thread, keyboard_thread
    mouse_thread = threading.Thread(target=start_mouse_listener)
    keyboard_thread = threading.Thread(target=start_keyboard_listener)
    mouse_thread.start()
    keyboard_thread.start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

def stop_listeners():
    # Set the stop flag to stop the listeners
    stop_flag.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    messagebox.showinfo("Info", "Screenshot capturing stopped.")

# Initialize the GUI
root = tk.Tk()
root.title("Screenshot Capturer")

start_button = tk.Button(root, text="Start", command=start_listeners)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_listeners, state=tk.DISABLED)
stop_button.pack(pady=10)

root.mainloop()

# Ensure the threads are properly joined when the GUI is closed
if 'mouse_thread' in globals() and mouse_thread.is_alive():
    mouse_thread.join()
if 'keyboard_thread' in globals() and keyboard_thread.is_alive():
    keyboard_thread.join()

print("Script stopped.")