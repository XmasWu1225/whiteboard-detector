# 白板检测系统

基于 YOLOv5 的智能白板检测、跟踪与增强系统。

## 功能特性

- **白板检测**: 使用 YOLOv5 深度学习模型进行目标检测
- **目标跟踪**: 基于 SORT 算法的多目标跟踪
- **智能构图**: 自动计算最佳取景范围和数字变焦
- **透视校正**: 消除拍摄角度造成的画面畸变
- **图像增强**: 亮度、对比度、锐化等图像优化

## 系统架构

```
whiteboard_detector/
├── models/           # 检测模型
│   └── detector.py   # YOLOv5 白板检测器
├── tracking/         # 跟踪算法
│   ├── sort.py       # SORT 跟踪算法实现
│   └── tracker.py    # 白板跟踪器封装
├── preprocessing/    # 预处理模块
├── postprocessing/   # 后处理模块
│   ├── cropper.py    # 智能裁剪
│   ├── perspective.py # 透视校正
│   └── enhancer.py   # 图像增强
├── utils/            # 工具函数
├── config.py         # 配置文件
├── main.py           # 主程序
└── examples.py       # 使用示例
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 实时摄像头检测

```bash
python main.py --camera 0
```

### 2. 处理视频文件

```bash
python main.py --video input.mp4 --output output.mp4
```

### 3. 处理单张图片

```bash
python main.py --image input.jpg --output output.jpg
```

### 4. 使用自定义模型

```bash
python main.py --model path/to/model.pt --camera 0
```

## 配置说明

在 `config.py` 中可以调整以下参数:

- `YOLOV5_CONFIDENCE_THRESHOLD`: 检测置信度阈值 (默认: 0.5)
- `CROP_MARGIN_RATIO`: 裁剪边距比例 (默认: 0.1)
- `ENHANCE_BRIGHTNESS_FACTOR`: 亮度增强因子 (默认: 1.2)
- `ENHANCE_CONTRAST_FACTOR`: 对比度增强因子 (默认: 1.1)
- `CAMERA_WIDTH/HEIGHT`: 摄像头分辨率
- `DISPLAY_WIDTH/HEIGHT`: 显示分辨率

## 技术细节

### 白板检测
- 使用 YOLOv5 模型进行目标检测
- 支持自定义模型训练
- 实时检测性能优化

### 目标跟踪
- SORT (Simple Online and Realtime Tracking) 算法
- 卡尔曼滤波预测目标位置
- IOU 匹配进行目标关联

### 智能构图
- 自动计算最佳取景范围
- 数字变焦模拟光学变焦
- 保持白板内容完整

### 透视校正
- 检测白板四个角点
- 透视变换校正畸变
- 自动旋转校正

### 图像增强
- 自动亮度对比度调整
- 锐化滤波器增强边缘
- 白平衡色彩校正
- CLAHE 直方图均衡化

## 快捷键

- `q`: 退出程序
- `r`: 重置跟踪器

## 性能优化建议

1. 使用 GPU 加速 (CUDA)
2. 降低输入分辨率
3. 使用轻量级模型 (yolov5n, yolov5s)
4. 减少后处理步骤

## 注意事项

- 首次运行会自动下载 YOLOv5 模型
- 建议使用 GPU 以获得更好的性能
- 光照条件对检测效果影响较大
- 白板应尽量占据画面主要区域

## 许可证

MIT License
