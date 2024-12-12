from ultralytics import YOLO
if __name__ == '__main__':
    model = YOLO('yolo11n.pt')
    model.train(data='data.yaml', epochs=500, imgsz=640, batch=16, workers=2, device='0')