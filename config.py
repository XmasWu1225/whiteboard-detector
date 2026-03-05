import torch

class Config:
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    YOLOV5_MODEL_PATH = 'yolov5s.pt'
    YOLOV5_CONFIDENCE_THRESHOLD = 0.5
    YOLOV5_IOU_THRESHOLD = 0.45
    YOLOV5_IMAGE_SIZE = 640
    
    SORT_MAX_AGE = 30
    SORT_MIN_HITS = 3
    SORT_IOU_THRESHOLD = 0.3
    
    CROP_MARGIN_RATIO = 0.1
    
    ENHANCE_BRIGHTNESS_FACTOR = 1.2
    ENHANCE_CONTRAST_FACTOR = 1.1
    ENHANCE_SHARPEN_KERNEL = 0.2
    
    CAMERA_WIDTH = 1920
    CAMERA_HEIGHT = 1080
    CAMERA_FPS = 30
    
    DISPLAY_WIDTH = 1280
    DISPLAY_HEIGHT = 720
    
    SAVE_OUTPUT = False
    OUTPUT_PATH = './output'
    
    DEBUG_MODE = False
