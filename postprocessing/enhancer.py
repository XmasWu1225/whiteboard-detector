import cv2
import numpy as np
from typing import Tuple, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import Config


class ImageEnhancer:
    def __init__(self, brightness_factor: float = None, 
                 contrast_factor: float = None,
                 sharpen_kernel: float = None):
        self.brightness_factor = brightness_factor if brightness_factor else Config.ENHANCE_BRIGHTNESS_FACTOR
        self.contrast_factor = contrast_factor if contrast_factor else Config.ENHANCE_CONTRAST_FACTOR
        self.sharpen_kernel = sharpen_kernel if sharpen_kernel else Config.ENHANCE_SHARPEN_KERNEL
    
    def adjust_brightness(self, image: np.ndarray, factor: float = None) -> np.ndarray:
        if factor is None:
            factor = self.brightness_factor
        
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        v = np.clip(v * factor, 0, 255).astype(np.uint8)
        
        hsv = cv2.merge([h, s, v])
        enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return enhanced
    
    def adjust_contrast(self, image: np.ndarray, factor: float = None) -> np.ndarray:
        if factor is None:
            factor = self.contrast_factor
        
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        mean = np.mean(l)
        l = np.clip((l - mean) * factor + mean, 0, 255).astype(np.uint8)
        
        lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def sharpen(self, image: np.ndarray, kernel: float = None) -> np.ndarray:
        if kernel is None:
            kernel = self.sharpen_kernel
        
        sharpen_kernel = np.array([
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]
        ], dtype=np.float32)
        
        sharpen_kernel = sharpen_kernel * kernel
        sharpen_kernel[1, 1] = 1 + 8 * kernel
        
        sharpened = cv2.filter2D(image, -1, sharpen_kernel)
        
        return sharpened
    
    def enhance_whiteboard(self, image: np.ndarray) -> np.ndarray:
        enhanced = self.adjust_brightness(image)
        enhanced = self.adjust_contrast(enhanced)
        enhanced = self.sharpen(enhanced)
        
        return enhanced
    
    def auto_brightness_contrast(self, image: np.ndarray, clip_hist_percent: float = 1.0) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_size = len(hist)
        
        accumulator = np.cumsum(hist)
        
        max_val = accumulator[-1]
        clip_hist_percent *= (max_val / 100.0)
        clip_hist_percent /= 2.0
        
        min_gray = 0
        while accumulator[min_gray] < clip_hist_percent:
            min_gray += 1
        
        max_gray = hist_size - 1
        while accumulator[max_gray] >= (max_val - clip_hist_percent):
            max_gray -= 1
        
        alpha = 255 / (max_gray - min_gray)
        beta = -min_gray * alpha
        
        enhanced = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        
        return enhanced
    
    def unsharp_mask(self, image: np.ndarray, 
                    sigma: float = 1.0, 
                    strength: float = 1.5) -> np.ndarray:
        blurred = cv2.GaussianBlur(image, (0, 0), sigma)
        sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
        
        return sharpened
    
    def denoise(self, image: np.ndarray, h: float = 10.0) -> np.ndarray:
        denoised = cv2.fastNlMeansDenoisingColored(image, None, h, h, 7, 21)
        
        return denoised
    
    def enhance_text_clarity(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
        
        return enhanced
    
    def white_balance(self, image: np.ndarray) -> np.ndarray:
        result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        
        balanced = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
        
        return balanced
    
    def full_enhancement_pipeline(self, image: np.ndarray) -> np.ndarray:
        enhanced = self.white_balance(image)
        enhanced = self.auto_brightness_contrast(enhanced)
        enhanced = self.enhance_text_clarity(enhanced)
        enhanced = self.unsharp_mask(enhanced)
        
        return enhanced
    
    def histogram_equalization(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 2:
            return cv2.equalizeHist(image)
        
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        channels = cv2.split(ycrcb)
        cv2.equalizeHist(channels[0], channels[0])
        ycrcb = cv2.merge(channels)
        equalized = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        
        return equalized
    
    def adaptive_threshold(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        binary = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        
        return binary
