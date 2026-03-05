"""
使用示例
"""

from main import WhiteboardDetectionSystem
import cv2


def example_camera():
    print("示例 1: 使用摄像头实时检测白板")
    
    system = WhiteboardDetectionSystem(camera_id=0)
    system.run()


def example_video():
    print("示例 2: 处理视频文件")
    
    video_path = "path/to/your/video.mp4"
    output_path = "output/result.mp4"
    
    system = WhiteboardDetectionSystem()
    system.process_video_file(video_path, output_path)


def example_image():
    print("示例 3: 处理单张图片")
    
    image_path = "path/to/your/image.jpg"
    output_path = "output/result.jpg"
    
    system = WhiteboardDetectionSystem()
    system.process_image(image_path, output_path)


def example_custom_config():
    print("示例 4: 使用自定义配置")
    
    from config import Config
    
    Config.YOLOV5_CONFIDENCE_THRESHOLD = 0.6
    Config.CROP_MARGIN_RATIO = 0.15
    Config.ENHANCE_BRIGHTNESS_FACTOR = 1.3
    
    system = WhiteboardDetectionSystem(camera_id=0)
    system.run()


def example_step_by_step():
    print("示例 5: 分步处理")
    
    from models.detector import WhiteboardDetector
    from tracking.tracker import WhiteboardTracker
    from postprocessing.cropper import SmartCropper
    from postprocessing.perspective import PerspectiveCorrector
    from postprocessing.enhancer import ImageEnhancer
    
    detector = WhiteboardDetector()
    tracker = WhiteboardTracker()
    cropper = SmartCropper()
    perspective_corrector = PerspectiveCorrector()
    enhancer = ImageEnhancer()
    
    image = cv2.imread("path/to/image.jpg")
    
    detections = detector.detect(image)
    print(f"检测到 {len(detections)} 个对象")
    
    tracked_objects = tracker.update(detections)
    print(f"跟踪到 {len(tracked_objects)} 个对象")
    
    if tracked_objects:
        stable_tracker = tracker.get_most_stable_tracker()
        bbox = stable_tracker['bbox']
        
        cropped = cropper.smart_crop_with_zoom(image, bbox)
        corrected = perspective_corrector.correct_perspective(image, bbox)
        enhanced = enhancer.full_enhancement_pipeline(cropped)
        
        cv2.imshow("Original", image)
        cv2.imshow("Cropped", cropped)
        cv2.imshow("Corrected", corrected)
        cv2.imshow("Enhanced", enhanced)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        example_name = sys.argv[1]
        examples = {
            'camera': example_camera,
            'video': example_video,
            'image': example_image,
            'config': example_custom_config,
            'step': example_step_by_step
        }
        
        if example_name in examples:
            examples[example_name]()
        else:
            print(f"未知示例: {example_name}")
            print("可用示例: camera, video, image, config, step")
    else:
        print("请指定要运行的示例:")
        print("python examples.py camera  - 使用摄像头")
        print("python examples.py video   - 处理视频文件")
        print("python examples.py image   - 处理图片")
        print("python examples.py config  - 使用自定义配置")
        print("python examples.py step    - 分步处理")
