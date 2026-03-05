# 项目结构

```
whiteboard_detector/
│
├── __init__.py                 # 包初始化文件
├── config.py                   # 配置文件
├── requirements.txt            # 依赖包列表
├── README.md                   # 项目说明文档
├── main.py                     # 主程序入口
├── examples.py                 # 使用示例
├── test.py                     # 功能测试脚本
│
├── models/                     # 检测模型模块
│   ├── __init__.py
│   └── detector.py             # YOLOv5 白板检测器
│
├── tracking/                   # 跟踪算法模块
│   ├── __init__.py
│   ├── sort.py                 # SORT 跟踪算法实现
│   └── tracker.py              # 白板跟踪器封装
│
├── preprocessing/              # 预处理模块
│   └── __init__.py
│
├── postprocessing/             # 后处理模块
│   ├── __init__.py
│   ├── cropper.py              # 智能裁剪与数字变焦
│   ├── perspective.py          # 透视校正
│   └── enhancer.py             # 图像增强
│
└── utils/                      # 工具函数模块
    └── __init__.py
```

## 核心模块说明

### 1. models/detector.py
- **功能**: 使用 YOLOv5 进行白板检测
- **主要类**: `WhiteboardDetector`
- **关键方法**:
  - `detect()`: 检测图像中的所有对象
  - `detect_whiteboard()`: 专门检测白板
  - `get_whiteboard_region()`: 获取白板区域

### 2. tracking/sort.py
- **功能**: SORT 多目标跟踪算法实现
- **主要类**: `KalmanBoxTracker`, `Sort`
- **关键方法**:
  - `update()`: 更新跟踪器状态
  - `predict()`: 预测目标位置
  - `associate_detections_to_trackers()`: 关联检测结果与跟踪器

### 3. tracking/tracker.py
- **功能**: 白板跟踪器封装
- **主要类**: `WhiteboardTracker`
- **关键方法**:
  - `update()`: 更新跟踪状态
  - `get_most_stable_tracker()`: 获取最稳定的跟踪目标

### 4. postprocessing/cropper.py
- **功能**: 智能构图与数字裁剪
- **主要类**: `SmartCropper`
- **关键方法**:
  - `calculate_crop_region()`: 计算最佳裁剪区域
  - `smart_crop_with_zoom()`: 智能裁剪并应用数字变焦
  - `apply_digital_zoom()`: 应用数字变焦

### 5. postprocessing/perspective.py
- **功能**: 透视校正
- **主要类**: `PerspectiveCorrector`
- **关键方法**:
  - `detect_corners()`: 检测白板角点
  - `correct_perspective()`: 校正透视畸变
  - `auto_rotate()`: 自动旋转校正

### 6. postprocessing/enhancer.py
- **功能**: 图像增强
- **主要类**: `ImageEnhancer`
- **关键方法**:
  - `adjust_brightness()`: 调整亮度
  - `adjust_contrast()`: 调整对比度
  - `sharpen()`: 锐化图像
  - `full_enhancement_pipeline()`: 完整增强流程

### 7. main.py
- **功能**: 主程序，整合所有模块
- **主要类**: `WhiteboardDetectionSystem`
- **关键方法**:
  - `run()`: 运行实时检测
  - `process_video_file()`: 处理视频文件
  - `process_image()`: 处理单张图片

## 数据流程

```
输入图像/视频
    ↓
[预处理] - 图像格式转换、尺寸调整
    ↓
[白板检测] - YOLOv5 检测白板位置
    ↓
[目标跟踪] - SORT 算法持续跟踪白板
    ↓
[智能构图] - 计算最佳取景范围
    ↓
[透视校正] - 消除拍摄角度畸变
    ↓
[图像增强] - 亮度、对比度、锐化优化
    ↓
输出结果
```

## 使用流程

1. **初始化系统**: 加载模型、初始化跟踪器
2. **获取图像**: 从摄像头、视频文件或图片文件
3. **检测白板**: 使用 YOLOv5 检测白板位置
4. **跟踪白板**: 使用 SORT 算法持续跟踪
5. **智能裁剪**: 计算最佳裁剪区域并应用数字变焦
6. **透视校正**: 校正拍摄角度造成的畸变
7. **图像增强**: 优化图像质量
8. **显示/保存**: 实时显示或保存结果
