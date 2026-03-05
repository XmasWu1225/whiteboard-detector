#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    print("测试模块导入...")
    
    try:
        import torch
        print("✓ PyTorch 已安装")
    except ImportError:
        print("✗ PyTorch 未安装，请运行: pip install torch torchvision")
        return False
    
    try:
        import cv2
        print("✓ OpenCV 已安装")
    except ImportError:
        print("✗ OpenCV 未安装，请运行: pip install opencv-python")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy 已安装")
    except ImportError:
        print("✗ NumPy 未安装，请运行: pip install numpy")
        return False
    
    try:
        from filterpy.kalman import KalmanFilter
        print("✓ FilterPy 已安装")
    except ImportError:
        print("✗ FilterPy 未安装，请运行: pip install filterpy")
        return False
    
    return True


def test_config():
    print("\n测试配置文件...")
    
    try:
        from config import Config
        print(f"✓ 配置文件加载成功")
        print(f"  - 设备: {Config.DEVICE}")
        print(f"  - 置信度阈值: {Config.YOLOV5_CONFIDENCE_THRESHOLD}")
        print(f"  - 摄像头分辨率: {Config.CAMERA_WIDTH}x{Config.CAMERA_HEIGHT}")
        return True
    except Exception as e:
        print(f"✗ 配置文件加载失败: {e}")
        return False


def test_detector():
    print("\n测试检测器...")
    
    try:
        from models.detector import WhiteboardDetector
        print("✓ 检测器模块导入成功")
        
        detector = WhiteboardDetector()
        print("✓ 检测器初始化成功")
        
        return True
    except Exception as e:
        print(f"✗ 检测器测试失败: {e}")
        return False


def test_tracker():
    print("\n测试跟踪器...")
    
    try:
        from tracking.tracker import WhiteboardTracker
        print("✓ 跟踪器模块导入成功")
        
        tracker = WhiteboardTracker()
        print("✓ 跟踪器初始化成功")
        
        return True
    except Exception as e:
        print(f"✗ 跟踪器测试失败: {e}")
        return False


def test_postprocessing():
    print("\n测试后处理模块...")
    
    try:
        from postprocessing.cropper import SmartCropper
        from postprocessing.perspective import PerspectiveCorrector
        from postprocessing.enhancer import ImageEnhancer
        
        print("✓ 智能裁剪模块导入成功")
        print("✓ 透视校正模块导入成功")
        print("✓ 图像增强模块导入成功")
        
        cropper = SmartCropper()
        perspective = PerspectiveCorrector()
        enhancer = ImageEnhancer()
        
        print("✓ 后处理模块初始化成功")
        
        return True
    except Exception as e:
        print(f"✗ 后处理模块测试失败: {e}")
        return False


def test_image_processing():
    print("\n测试图像处理...")
    
    try:
        import cv2
        import numpy as np
        
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        test_image[:] = (255, 255, 255)
        
        from postprocessing.enhancer import ImageEnhancer
        enhancer = ImageEnhancer()
        
        enhanced = enhancer.enhance_whiteboard(test_image)
        print("✓ 图像增强功能正常")
        
        from postprocessing.cropper import SmartCropper
        cropper = SmartCropper()
        
        bbox = (100, 100, 500, 400)
        cropped = cropper.crop_image(test_image, bbox)
        print("✓ 图像裁剪功能正常")
        
        return True
    except Exception as e:
        print(f"✗ 图像处理测试失败: {e}")
        return False


def main():
    print("=" * 50)
    print("白板检测系统 - 功能测试")
    print("=" * 50)
    
    results = []
    
    results.append(("依赖包", test_imports()))
    results.append(("配置文件", test_config()))
    results.append(("检测器", test_detector()))
    results.append(("跟踪器", test_tracker()))
    results.append(("后处理", test_postprocessing()))
    results.append(("图像处理", test_image_processing()))
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:12s}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("所有测试通过！系统已准备就绪。")
        print("\n快速开始:")
        print("  python main.py --camera 0")
        print("  python main.py --image test.jpg")
        print("  python examples.py camera")
    else:
        print("部分测试失败，请检查错误信息并安装缺失的依赖。")
        print("\n安装依赖:")
        print("  pip install -r requirements.txt")
    print("=" * 50)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
