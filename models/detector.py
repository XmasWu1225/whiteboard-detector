import torch
import cv2
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import Config


class WhiteboardDetector:
    def __init__(self, model_path: str = None, device: str = None):
        self.device = device if device else Config.DEVICE
        self.model_path = model_path if model_path else Config.YOLOV5_MODEL_PATH
        self.confidence_threshold = Config.YOLOV5_CONFIDENCE_THRESHOLD
        self.iou_threshold = Config.YOLOV5_IOU_THRESHOLD
        self.image_size = Config.YOLOV5_IMAGE_SIZE
        
        self.model = None
        self._load_model()
    
    def _load_model(self):
        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', 
                                       path=self.model_path, 
                                       device=self.device)
            self.model.conf = self.confidence_threshold
            self.model.iou = self.iou_threshold
            self.model.eval()
            print(f"YOLOv5 model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading YOLOv5 model: {e}")
            raise
    
    def preprocess(self, image: np.ndarray) -> torch.Tensor:
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image_rgb
    
    def detect(self, image: np.ndarray) -> List[dict]:
        image_rgb = self.preprocess(image)
        
        with torch.no_grad():
            results = self.model(image_rgb, size=self.image_size)
        
        detections = []
        df = results.pandas().xyxy[0]
        
        for _, row in df.iterrows():
            detection = {
                'bbox': [int(row['xmin']), int(row['ymin']), 
                        int(row['xmax']), int(row['ymax'])],
                'confidence': float(row['confidence']),
                'class_id': int(row['class']),
                'class_name': row['name']
            }
            detections.append(detection)
        
        return detections
    
    def detect_whiteboard(self, image: np.ndarray) -> Optional[dict]:
        detections = self.detect(image)
        
        for det in detections:
            if 'whiteboard' in det['class_name'].lower():
                return det
        
        if detections:
            return max(detections, key=lambda x: x['confidence'])
        
        return None
    
    def get_whiteboard_region(self, image: np.ndarray) -> Optional[np.ndarray]:
        detection = self.detect_whiteboard(image)
        
        if detection:
            x1, y1, x2, y2 = detection['bbox']
            return image[y1:y2, x1:x2]
        
        return None
    
    def draw_detections(self, image: np.ndarray, detections: List[dict]) -> np.ndarray:
        image_copy = image.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            confidence = det['confidence']
            class_name = det['class_name']
            
            cv2.rectangle(image_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            label = f"{class_name}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            
            cv2.rectangle(image_copy, (x1, y1 - label_size[1] - 10),
                         (x1 + label_size[0], y1), (0, 255, 0), -1)
            cv2.putText(image_copy, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        return image_copy
