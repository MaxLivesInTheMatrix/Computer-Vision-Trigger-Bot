# # import torch
# # import cv
# # import cv2
# # print(torch.cuda.is_available())
# # print(torch.cuda.get_device_name(0))
# # print(cv.__version__)
# # print(cv.cuda.getCudaEnabledDeviceCount())

# # import torch
# # import cv2

# # print("CUDA available with PyTorch:", torch.cuda.is_available())
# # print("CUDA device name with PyTorch:", torch.cuda.get_device_name(0))

# # print("OpenCV version:", cv2.__version__)
# # print("CUDA enabled devices with OpenCV:", cv2.cuda.getCudaEnabledDeviceCount())

# # import cv2

# # count = cv2.cuda.getCudaEnabledDeviceCount()
# # print(count)
# # import cv2

# # print("OpenCV version:", cv2.__version__)
# # print("CUDA enabled devices with OpenCV:", cv2.cuda.getCudaEnabledDeviceCount())
# # #print(cv2.getBuildInformation())


from ultralytics import YOLO
import tensorrt

# Load model
model = YOLO(r"C:\TriggerBot\runs\detect\train3yolo11\weights\best.pt")

# Export the model to TensorRT format
model.export(format='engine')

