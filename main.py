import cv2
import numpy as np
import time
from typing import Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from config import Config
from models.detector import WhiteboardDetector
from tracking.tracker import WhiteboardTracker
from postprocessing.cropper import SmartCropper
from postprocessing.perspective import PerspectiveCorrector
from postprocessing.enhancer import ImageEnhancer


class WhiteboardDetectionSystem:
    def __init__(self, camera_id: int = 0, model_path: str = None):
        self.camera_id = camera_id
        self.model_path = model_path
        
        self.detector = WhiteboardDetector(model_path=self.model_path)
        self.tracker = WhiteboardTracker()
        self.cropper = SmartCropper()
        self.perspective_corrector = PerspectiveCorrector()
        self.enhancer = ImageEnhancer()
        
        self.cap = None
        self.is_running = False
        
        self.current_whiteboard = None
        self.tracking_id = None
        self.tracking_confidence = 0
        
        self.frame_count = 0
        self.fps = 0
        self.last_time = time.time()
    
    def initialize_camera(self) -> bool:
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_id}")
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, Config.CAMERA_FPS)
        
        return True
    
    def process_frame(self, frame: np.ndarray) -> tuple:
        self.frame_count += 1
        current_time = time.time()
        self.fps = 1.0 / (current_time - self.last_time)
        self.last_time = current_time
        
        detections = self.detector.detect(frame)
        
        tracked_objects = self.tracker.update(detections)
        
        whiteboard_info = None
        processed_frame = frame.copy()
        
        if tracked_objects:
            stable_tracker = self.tracker.get_most_stable_tracker()
            
            if stable_tracker:
                bbox = stable_tracker['bbox']
                track_id = stable_tracker['id']
                
                if self.tracking_id is None or track_id == self.tracking_id:
                    self.tracking_id = track_id
                    self.current_whiteboard = bbox
                    
                    cropped = self.cropper.smart_crop_with_zoom(frame, bbox)
                    
                    corrected = self.perspective_corrector.correct_perspective(frame, bbox)
                    if corrected is not None:
                        corrected = self.enhancer.full_enhancement_pipeline(corrected)
                    else:
                        corrected = self.enhancer.full_enhancement_pipeline(cropped)
                    
                    whiteboard_info = {
                        'bbox': bbox,
                        'track_id': track_id,
                        'cropped': cropped,
                        'corrected': corrected
                    }
                    
                    cv2.rectangle(processed_frame, (bbox[0], bbox[1]), 
                                 (bbox[2], bbox[3]), (0, 255, 0), 3)
                    
                    label = f"Whiteboard ID: {track_id}"
                    cv2.putText(processed_frame, label, (bbox[0], bbox[1] - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        cv2.putText(processed_frame, f"FPS: {self.fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return processed_frame, whiteboard_info
    
    def run(self):
        if not self.initialize_camera():
            return
        
        self.is_running = True
        print("Whiteboard Detection System started. Press 'q' to quit.")
        
        try:
            while self.is_running:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                processed_frame, whiteboard_info = self.process_frame(frame)
                
                if whiteboard_info:
                    display_frame = np.hstack([
                        cv2.resize(processed_frame, (640, 360)),
                        cv2.resize(whiteboard_info['cropped'], (640, 360)),
                        cv2.resize(whiteboard_info['corrected'], (640, 360))
                    ])
                    
                    cv2.putText(display_frame, "Original", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(display_frame, "Cropped", (650, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(display_frame, "Enhanced", (1290, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    cv2.imshow('Whiteboard Detection System', display_frame)
                else:
                    cv2.imshow('Whiteboard Detection System', processed_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.is_running = False
                elif key == ord('r'):
                    self.tracker.reset()
                    self.tracking_id = None
                    self.current_whiteboard = None
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.cleanup()
    
    def process_video_file(self, video_path: str, output_path: str = None):
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, 30.0, 
                                  (Config.DISPLAY_WIDTH * 3, Config.DISPLAY_HEIGHT))
        
        self.is_running = True
        print(f"Processing video file: {video_path}")
        
        try:
            while self.is_running:
                ret, frame = self.cap.read()
                
                if not ret:
                    break
                
                processed_frame, whiteboard_info = self.process_frame(frame)
                
                if whiteboard_info:
                    display_frame = np.hstack([
                        cv2.resize(processed_frame, (640, 360)),
                        cv2.resize(whiteboard_info['cropped'], (640, 360)),
                        cv2.resize(whiteboard_info['corrected'], (640, 360))
                    ])
                else:
                    display_frame = cv2.resize(processed_frame, (1920, 360))
                
                if output_path:
                    out.write(display_frame)
                
                cv2.imshow('Whiteboard Detection System', display_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.is_running = False
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            if output_path:
                out.release()
            self.cleanup()
    
    def process_image(self, image_path: str, output_path: str = None):
        frame = cv2.imread(image_path)
        
        if frame is None:
            print(f"Error: Could not read image {image_path}")
            return
        
        processed_frame, whiteboard_info = self.process_frame(frame)
        
        if whiteboard_info:
            result = np.hstack([
                cv2.resize(processed_frame, (640, 360)),
                cv2.resize(whiteboard_info['cropped'], (640, 360)),
                cv2.resize(whiteboard_info['corrected'], (640, 360))
            ])
        else:
            result = processed_frame
        
        if output_path:
            cv2.imwrite(output_path, result)
            print(f"Result saved to {output_path}")
        
        cv2.imshow('Whiteboard Detection System', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def cleanup(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Whiteboard Detection System stopped")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Whiteboard Detection System using YOLOv5')
    parser.add_argument('--camera', type=int, default=0, help='Camera ID (default: 0)')
    parser.add_argument('--video', type=str, help='Video file path')
    parser.add_argument('--image', type=str, help='Image file path')
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--model', type=str, help='Path to YOLOv5 model')
    
    args = parser.parse_args()
    
    system = WhiteboardDetectionSystem(camera_id=args.camera, model_path=args.model)
    
    if args.video:
        system.process_video_file(args.video, args.output)
    elif args.image:
        system.process_image(args.image, args.output)
    else:
        system.run()


if __name__ == '__main__':
    main()
