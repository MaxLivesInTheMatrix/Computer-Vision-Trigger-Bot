# Computer Vision Overwatch 2 Trigger Bot
# Overview
This project is an Overwatch 2 Triggerbot built using Python and a YOLO object detection model. The triggerbot detects enemy targets on screen using real-time object detection and triggers a mouse click when the detected target crosses the center of the screen. The YOLO model processes the frames captured from the screen, and the triggerbot operates with high efficiency, leveraging the TensorRT-optimized model for low latency. Trained on over 2500+ images of gameplay for thousands of epochs
See it in action here! https://youtu.be/fzFwPjRoTaM

# Key Features
* Real-time screen capture using mss for high FPS (140+) and 70+ FPS object detection (When leveraging CUDA.)
* YOLO-based object detection with the ultralytics YOLO model, optimized with TensorRT for high performance.
* Efficient mouse click actions using Windows API for non-blocking, fast clicks.
* Multithreading to handle multiple tasks in parallel without blocking performance.
* Customizable cooldown between shots to mimic human-like behavior and avoid detection by anti-cheat systems.
# Dependencies
The project requires the following Python libraries:

* mss: For fast screen capture.
* pyautogui: For getting screen size and other utility functions.
* cv2 (OpenCV): For converting images to a format that can be processed by YOLO.
* numpy: For image processing and conversion to a NumPy array.
* ultralytics: For YOLO object detection.
* threading: To handle blocking calls efficiently.
* pynput: To control mouse and keyboard inputs.
* concurrent.futures: For managing threads.
* ctypes: For sending low-level Windows API commands to simulate fast mouse clicks.

# Screen Resolution
By default, the triggerbot captures a 600x400 region at the center of the screen. Adjust the desiredHeight and desiredWidth variables if you want a different screen capture size.
# How It Works
# Screen Capture
The mss library captures a region of the screen in real-time, centered at the middle of the screen. This frame is then processed by the YOLO model for object detection.
# YOLO Object Detection
The YOLO model takes each frame, processes it to detect objects, and returns bounding boxes and confidence scores. If an enemy target is detected with a confidence score greater than 20%, the bot checks if the target is at the center of the screen (crosshair area).
# Clicking Mechanism
Once a valid target is detected, the bot simulates a left mouse click using Windows API functions for faster response times. The click is triggered using multithreading to avoid performance bottlenecks.

# Cooldown and Anti-Cheat Evasion
The bot implements a cooldown mechanism between clicks to mimic human-like behavior. You can adjust this cooldown (default is 0.65 seconds). Optionally, you can add randomness to the cooldown to evade anti-cheat systems.

# FPS Monitoring: 
The FPS (frames per second) is calculated and printed every 10 frames. You can monitor the performance and adjust the screen capture resolution or cooldown if needed to improve FPS.

# Notes
This triggerbot is designed for educational purposes only. Using a triggerbot in online games is typically against the game's terms of service and can lead to penalties, including account bans.
The project uses TensorRT to speed up YOLO inference, achieving more than 70 FPS on most modern GPUs (e.g., NVIDIA 1080ti or higher).
License
MIT License
