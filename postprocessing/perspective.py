import cv2
import numpy as np
from typing import Tuple, Optional, List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import Config


class PerspectiveCorrector:
    def __init__(self, target_size: Tuple[int, int] = None):
        self.target_size = target_size if target_size else (Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT)
    
    def detect_corners(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        x1, y1, x2, y2 = bbox
        roi = image[y1:y2, x1:x2]
        
        if roi.size == 0:
            return None
        
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        corners = cv2.goodFeaturesToTrack(
            gray,
            maxCorners=4,
            qualityLevel=0.01,
            minDistance=30,
            blockSize=3
        )
        
        if corners is None or len(corners) < 4:
            return self._estimate_corners_from_bbox(bbox)
        
        corners = np.int32(corners).reshape(-1, 2)
        corners[:, 0] += x1
        corners[:, 1] += y1
        
        corners = self._sort_corners(corners)
        
        return corners
    
    def _estimate_corners_from_bbox(self, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        x1, y1, x2, y2 = bbox
        corners = np.array([
            [x1, y1],
            [x2, y1],
            [x2, y2],
            [x1, y2]
        ], dtype=np.float32)
        return corners
    
    def _sort_corners(self, corners: np.ndarray) -> np.ndarray:
        center = np.mean(corners, axis=0)
        
        angles = np.arctan2(corners[:, 1] - center[1], corners[:, 0] - center[0])
        sorted_indices = np.argsort(angles)
        
        return corners[sorted_indices]
    
    def calculate_homography(self, src_corners: np.ndarray, 
                           dst_size: Tuple[int, int] = None) -> Tuple[np.ndarray, np.ndarray]:
        if dst_size is None:
            dst_size = self.target_size
        
        dst_corners = np.array([
            [0, 0],
            [dst_size[0], 0],
            [dst_size[0], dst_size[1]],
            [0, dst_size[1]]
        ], dtype=np.float32)
        
        H, _ = cv2.findHomography(src_corners, dst_corners, cv2.RANSAC, 5.0)
        
        return H, dst_corners
    
    def apply_perspective_transform(self, image: np.ndarray, 
                                   src_corners: np.ndarray,
                                   dst_size: Tuple[int, int] = None) -> np.ndarray:
        if dst_size is None:
            dst_size = self.target_size
        
        H, _ = self.calculate_homography(src_corners, dst_size)
        
        warped = cv2.warpPerspective(image, H, dst_size, 
                                    flags=cv2.INTER_LINEAR,
                                    borderMode=cv2.BORDER_CONSTANT,
                                    borderValue=(255, 255, 255))
        
        return warped
    
    def correct_perspective(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        corners = self.detect_corners(image, bbox)
        
        if corners is None:
            return None
        
        corrected = self.apply_perspective_transform(image, corners)
        
        return corrected
    
    def refine_corners(self, image: np.ndarray, corners: np.ndarray, 
                      window_size: int = 15) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        
        corners = np.float32(corners)
        refined_corners = cv2.cornerSubPix(gray, corners, (window_size, window_size), (-1, -1), criteria)
        
        return refined_corners
    
    def get_perspective_lines(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        corners = self.detect_corners(image, bbox)
        
        if corners is None:
            return None
        
        image_copy = image.copy()
        
        for i in range(4):
            pt1 = tuple(corners[i].astype(int))
            pt2 = tuple(corners[(i + 1) % 4].astype(int))
            cv2.line(image_copy, pt1, pt2, (0, 255, 0), 2)
        
        return image_copy
    
    def calculate_skew_angle(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> float:
        corners = self.detect_corners(image, bbox)
        
        if corners is None:
            return 0.0
        
        top_edge = corners[1] - corners[0]
        angle = np.arctan2(top_edge[1], top_edge[0]) * 180 / np.pi
        
        return angle
    
    def auto_rotate(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        angle = self.calculate_skew_angle(image, bbox)
        
        if abs(angle) < 1.0:
            return image
        
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), 
                               flags=cv2.INTER_LINEAR,
                               borderMode=cv2.BORDER_CONSTANT,
                               borderValue=(255, 255, 255))
        
        return rotated
