# 快速开始指南

## 环境要求

- Python 3.7+
- CUDA 10.2+ (可选，用于 GPU 加速)
- 摄像头设备 (用于实时检测)

## 快速安装

### 方法 1: 使用启动脚本 (推荐)

#### Linux/Mac
```bash
cd whiteboard_detector
./run.sh
```

#### Windows
```cmd
cd whiteboard_detector
run.bat
```

### 方法 2: 手动安装

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行测试
python test.py
```

## 基本使用

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

## 快捷键

- `q`: 退出程序
- `r`: 重置跟踪器

## 常见问题

### 1. 模型下载失败

首次运行时，YOLOv5 模型会自动下载。如果下载失败，可以手动下载：

```bash
# 下载 YOLOv5s 模型
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt
```

### 2. 摄像头无法打开

检查摄像头设备是否被其他程序占用，或尝试更改摄像头 ID：

```bash
python main.py --camera 1
```

### 3. 性能优化

如果检测速度较慢，可以尝试以下方法：

1. 使用 GPU 加速 (确保已安装 CUDA)
2. 降低输入分辨率 (修改 `config.py` 中的 `CAMERA_WIDTH/HEIGHT`)
3. 使用轻量级模型 (修改 `config.py` 中的 `YOLOV5_MODEL_PATH` 为 `yolov5n.pt`)

### 4. 检测效果不佳

如果白板检测效果不佳，可以尝试：

1. 调整置信度阈值 (修改 `config.py` 中的 `YOLOV5_CONFIDENCE_THRESHOLD`)
2. 改善光照条件
3. 确保白板在画面中占据较大区域
4. 训练自定义模型

## 自定义配置

编辑 `config.py` 文件可以调整各种参数：

```python
# 检测参数
YOLOV5_CONFIDENCE_THRESHOLD = 0.5  # 置信度阈值
YOLOV5_IOU_THRESHOLD = 0.45         # IOU 阈值

# 跟踪参数
SORT_MAX_AGE = 30                   # 最大跟踪帧数
SORT_MIN_HITS = 3                   # 最小命中次数

# 裁剪参数
CROP_MARGIN_RATIO = 0.1             # 裁剪边距比例

# 增强参数
ENHANCE_BRIGHTNESS_FACTOR = 1.2    # 亮度增强因子
ENHANCE_CONTRAST_FACTOR = 1.1       # 对比度增强因子
ENHANCE_SHARPEN_KERNEL = 0.2        # 锐化核大小
```

## 进阶使用

### 1. 分步处理

参考 `examples.py` 中的 `example_step_by_step()` 函数，可以分步调用各个模块：

```python
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

# 读取图像
image = cv2.imread("image.jpg")

# 检测
detections = detector.detect(image)

# 跟踪
tracked_objects = tracker.update(detections)

# 裁剪
bbox = tracked_objects[0]['bbox']
cropped = cropper.smart_crop_with_zoom(image, bbox)

# 校正
corrected = perspective_corrector.correct_perspective(image, bbox)

# 增强
enhanced = enhancer.full_enhancement_pipeline(cropped)
```

### 2. 训练自定义模型

如果需要检测特定类型的白板，可以训练自定义 YOLOv5 模型：

1. 准备训练数据集
2. 参考 YOLOv5 官方文档进行训练
3. 将训练好的模型路径设置到 `config.py` 中的 `YOLOV5_MODEL_PATH`

## 技术支持

- 查看项目文档: `README.md`
- 查看项目结构: `PROJECT_STRUCTURE.md`
- 运行测试: `python test.py`
- 查看示例: `python examples.py`

## 许可证

MIT License
