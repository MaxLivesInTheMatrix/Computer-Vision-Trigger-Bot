from ultralytics import YOLO

def main():
    # Load a model The nano model is perfect for this because it is so fast!
    #model = YOLO("yolov8n.yaml")  # build a new model from scratch
    #model = YOLO("yolov6n.yaml")  # build a new model from scratch
    model = YOLO("yolo11n.pt")     

    model.train(data="config.yaml", epochs=3000)  # train the model
    metrics = model.val()  # evaluate model performance on the validation set
    path = model.export(format="onnx")  # export the model to ONNX format
    device="0" # My 1080ti

if __name__ == '__main__':
    main()


# Making sure I have CUDA enabled and ready to go
# import torch
# print(torch.cuda.is_available())  # Should return True
# print(torch.cuda.current_device())  # Should return the device ID (0 for first GPU)
# print(torch.cuda.get_device_name(0))  # Should return the name of the GPU (1080ti)
# import torchvision
# print(torchvision.__version__)
# print(torch.ops.torchvision.nms)  # This should point to the CUDA NMS if supported
