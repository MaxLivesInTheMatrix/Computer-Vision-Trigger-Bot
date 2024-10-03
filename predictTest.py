from ultralytics import YOLO

# Load the trained model
model = YOLO(r"C:\TriggerBot\runs\detect\train3yolo11\weights\best.engine")  # Use raw string

# Run inference on a video
results = model.predict(source=r"C:\Users\jdidk\Documents\Overwatch\videos\overwatch\test2_24-08-10_10-23-33.mp4", show=True, save=True)

# Optionally, you can process results, such as saving output video
#output_video_path = results.save()  # This saves the output video with detections
    