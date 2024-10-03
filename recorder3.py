import mss                                                                      # mss for fastest screen capture (Over 140+ fps capable)
import pyautogui                                                                # pyautogui for gui (if using), getting screen size, and other functions
import cv2 as cv                                                                # cv for converting images to be able to use with yolo model
import numpy as np                                                              # Used for converting into a numpy array
import time                                                                     # Used for timing stuff
from ultralytics import YOLO                                                    # YOLO vision model
import threading                                                                # Threading massively helps with blocking calls
from pynput.mouse import Controller, Button                                     # Experimenting with mouse and keyboard movements
from pynput.keyboard import Controller as KeyboardController              
import random                                                                   # Random cooldown to help evade anticheat
from concurrent.futures import ThreadPoolExecutor                               # Used to make sure we don't have infinite threads being created
import ctypes                                                                   # Used for fast click with windows API
MOUSEEVENTF_LEFTDOWN = 0x0002                                                   # Mouse Left Down
MOUSEEVENTF_LEFTUP = 0x0004                                                     # Mouse Left Up

# Load the YOLO model to suppress output
#model = YOLO(r"C:\TriggerBot\runs\detect\train13\weights\best.onnx")
trt_model = YOLO(r"C:\TriggerBot\runs\detect\train3yolo11\weights\best.engine") # Using .engine format literally 2x+ the fps to over 70!

w, h = pyautogui.size()                                                         # Grabbing screen size and printing 
print("MSS Screen Capture Speed Test")                                          
print("Screen Resolution: " + str(w) + 'x' + str(h)) 
# desiredHeight = int(input("Enter desired height: "))                          # if the user wants to switch the input height and width, they can here
# desiredWidth = int(input("Enter desired width: "))                            # However I notices that 600 x 400 was the best balance between size and speed
desiredHeight = 600
desiredWidth  = 400
top = 540 - desiredHeight // 2                                                  # Centering the image capture on the middle of the screen
left = 960 - desiredWidth // 2
img = None
monitor = {"top": top, "left": left, "width": desiredWidth, "height": desiredHeight}

click_lock = threading.Lock()                                                   # Create a lock to prevent multiple threads from clicking simultaneously
executor = ThreadPoolExecutor(max_workers=1)                                    # Maximum of 1 extra thread at a time

last_click_time = 0                                                             # Variable to track the last click time
CLICK_COOLDOWN = .65                                                            # 0.65 second cooldown between clicks, I also used to use random here, and still might later on

# Initialize the keyboard controller, not using anymore, but still if I want to , I left it in 
# keyboard = KeyboardController()



def click_action():
    ''' click action is the function that checks if the time elapsed
    is greater than the click cooldown time, if it is, we call the 
    fast click function for a fast click that doesn't block anything.
    Initially I used pyautogui, but it "felt" slower to me, and I've
    had better results with the direct mouse event api'''
    global last_click_time
    current_time = time.time()
    with click_lock:                                                    # Click lock prevents too many threads from being created
        if current_time - last_click_time >= CLICK_COOLDOWN:
            fast_click(desiredWidth // 2, desiredHeight // 2)
            last_click_time = current_time

def fast_click(x, y):
    # ctypes.windll.user32.SetCursorPos(x, y)  # Set cursor position
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # Left mouse button down
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)    # Left mouse button up
    print("Shot's fired!")                                              # For debugging



def trigger_click():
    ''' This handles the click action in a seperate thread'''
    executor.submit(click_action)



def draw_boxes(results, img):
    ''' This function pulls out the data from the YOLO model'''
    for r in results:                                                                                           # For result in results
        boxes = r.boxes                                                                                         # We go through each bounding box formed
        for box in boxes:
            confidence = box.conf.item()                                                                        # Grab the confidence interval
            if confidence > 0.2:                                                                                # If the confidence interval is greater than 20%, (I'd rather have a false positive than miss a real positive)
                b = box.xyxy[0]                                                                                 # get box coordinates in (top, left, bottom, right) format
                x_min, y_min, x_max, y_max = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                
                if y_min < desiredHeight // 2 < y_max and x_min *1.075 < desiredWidth // 2 < x_max * .925:      # Trigger the click in a separate thread if the bounding box crosses the center of the screen
                    trigger_click()
                    #threading.Thread(target=click_action).start()
                    #CLICK_COOLDOWN = random.randrange(20, 35 ) / 10                                            # Here is where I would introduce randomness in the clicking frequency

    return img

# FPS calculation variables
frame_count = 0
start_time = time.time()
fps = 0

# Start the screen capture and processing loop
with mss.mss() as sct:
    while True:
        loop_start = time.time()

        # Capture the screen
        #capture_start = time.time()
        img = sct.grab((monitor["left"], monitor["top"], monitor["left"] + monitor["width"], monitor["top"] + monitor["height"])) # Grab the 600 x 400 image
        img = np.array(img)                                                                                                       # Convery to numpy array
        img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)                                                                                 # Convert to RGB from RGBA
        #capture_end = time.time()

        # Perform YOLO detection
        #detection_start = time.time()
        #results = model(img, verbose=False)
        results = trt_model(img, verbose=False)                                                                                   # Give the image to the model
        #detection_end = time.time()

        # Process the results and draw bounding boxes
        #draw_start = time.time()
        img = draw_boxes(results, img)                                                                                            # Pass the image into the draw boxes function
        #draw_end = time.time()


        # This is my FPS counter
        frame_count += 1
        if frame_count >= 10:
            end_time = time.time()
            fps = frame_count / (end_time - start_time)
            print(f"FPS: {fps:.2f}")
            frame_count = 0
            start_time = time.time()
            

cv.destroyAllWindows()