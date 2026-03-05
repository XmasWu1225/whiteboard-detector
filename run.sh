#!/bin/bash

echo "=========================================="
echo "白板检测系统 - 快速启动脚本"
echo "=========================================="
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

echo "✓ Python3 已安装"
python3 --version
echo ""

# 进入项目目录
cd "$(dirname "$0")"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    echo "✓ 虚拟环境创建成功"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo ""
echo "检查并安装依赖包..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ 依赖包安装成功"
else
    echo "✗ 依赖包安装失败"
    exit 1
fi

# 运行测试
echo ""
echo "运行系统测试..."
python test.py

# 询问用户要运行的模式
echo ""
echo "=========================================="
echo "请选择运行模式:"
echo "1. 摄像头实时检测"
echo "2. 处理视频文件"
echo "3. 处理图片"
echo "4. 查看示例"
echo "5. 退出"
echo "=========================================="
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo "启动摄像头检测..."
        python main.py --camera 0
        ;;
    2)
        read -p "请输入视频文件路径: " video_path
        read -p "请输入输出文件路径 (可选): " output_path
        if [ -z "$output_path" ]; then
            python main.py --video "$video_path"
        else
            python main.py --video "$video_path" --output "$output_path"
        fi
        ;;
    3)
        read -p "请输入图片文件路径: " image_path
        read -p "请输入输出文件路径 (可选): " output_path
        if [ -z "$output_path" ]; then
            python main.py --image "$image_path"
        else
            python main.py --image "$image_path" --output "$output_path"
        fi
        ;;
    4)
        echo "查看示例..."
        python examples.py
        ;;
    5)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

deactivate
