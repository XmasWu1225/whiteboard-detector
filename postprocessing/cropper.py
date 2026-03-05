import cv2
import numpy as np
from typing import Tuple, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import Config


class SmartCropper:
    def __init__(self, margin_ratio: float = None, target_size: Tuple[int, int] = None):
        self.margin_ratio = margin_ratio if margin_ratio else Config.CROP_MARGIN_RATIO
        self.target_size = target_size if target_size else (Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT)
    
    def calculate_crop_region(self, bbox: Tuple[int, int, int, int], 
                            image_shape: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x1, y1, x2, y2 = bbox
        img_h, img_w = image_shape[:2]
        
        width = x2 - x1
        height = y2 - y1
        
        margin_x = int(width * self.margin_ratio)
        margin_y = int(height * self.margin_ratio)
        
        crop_x1 = max(0, x1 - margin_x)
        crop_y1 = max(0, y1 - margin_y)
        crop_x2 = min(img_w, x2 + margin_x)
        crop_y2 = min(img_h, y2 + margin_y)
        
        crop_width = crop_x2 - crop_x1
        crop_height = crop_y2 - crop_y1
        
        aspect_ratio = self.target_size[0] / self.target_size[1]
        current_ratio = crop_width / crop_height
        
        if current_ratio > aspect_ratio:
            new_width = int(crop_height * aspect_ratio)
            center_x = (crop_x1 + crop_x2) // 2
            crop_x1 = max(0, center_x - new_width // 2)
            crop_x2 = min(img_w, crop_x1 + new_width)
        else:
            new_height = int(crop_width / aspect_ratio)
            center_y = (crop_y1 + crop_y2) // 2
            crop_y1 = max(0, center_y - new_height // 2)
            crop_y2 = min(img_h, crop_y1 + new_height)
        
        return (crop_x1, crop_y1, crop_x2, crop_y2)
    
    def crop_image(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        crop_region = self.calculate_crop_region(bbox, image.shape)
        x1, y1, x2, y2 = crop_region
        
        cropped = image[y1:y2, x1:x2]
        
        if cropped.size == 0:
            return image
        
        resized = cv2.resize(cropped, self.target_size, interpolation=cv2.INTER_LINEAR)
        
        return resized
    
    def apply_digital_zoom(self, image: np.ndarray, zoom_factor: float = 1.0) -> np.ndarray:
        if zoom_factor <= 1.0:
            return image
        
        h, w = image.shape[:2]
        new_h, new_w = int(h / zoom_factor), int(w / zoom_factor)
        
        center_x, center_y = w // 2, h // 2
        x1 = max(0, center_x - new_w // 2)
        y1 = max(0, center_y - new_h // 2)
        x2 = min(w, x1 + new_w)
        y2 = min(h, y1 + new_h)
        
        cropped = image[y1:y2, x1:x2]
        resized = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
        
        return resized
    
    def calculate_optimal_zoom(self, bbox: Tuple[int, int, int, int], 
                              image_shape: Tuple[int, int]) -> float:
        x1, y1, x2, y2 = bbox
        img_h, img_w = image_shape[:2]
        
        bbox_width = x2 - x1
        bbox_height = y2 - y1
        
        target_width = img_w * 0.8
        target_height = img_h * 0.8
        
        zoom_x = bbox_width / target_width
        zoom_y = bbox_height / target_height
        
        optimal_zoom = max(zoom_x, zoom_y)
        
        return min(optimal_zoom, 2.0)
    
    def smart_crop_with_zoom(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        crop_region = self.calculate_crop_region(bbox, image.shape)
        x1, y1, x2, y2 = crop_region
        
        cropped = image[y1:y2, x1:x2]
        
        if cropped.size == 0:
            return image
        
        zoom_factor = self.calculate_optimal_zoom(bbox, image.shape)
        
        if zoom_factor > 1.0:
            cropped = self.apply_digital_zoom(cropped, zoom_factor)
        
        resized = cv2.resize(cropped, self.target_size, interpolation=cv2.INTER_LINEAR)
        
        return resized
    
    def draw_crop_region(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        image_copy = image.copy()
        crop_region = self.calculate_crop_region(bbox, image.shape)
        x1, y1, x2, y2 = crop_region
        
        cv2.rectangle(image_copy, (x1, y1), (x2, y2), (0, 255, 255), 2)
        
        return image_copy
