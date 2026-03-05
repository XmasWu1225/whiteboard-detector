@echo off
chcp 65001 >nul
echo ==========================================
echo 白板检测系统 - 快速启动脚本 (Windows)
echo ==========================================
echo.

REM 检查 Python 环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

echo ✓ Python 已安装
python --version
echo.

REM 进入项目目录
cd /d "%~dp0"

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo ✓ 虚拟环境创建成功
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo.
echo 检查并安装依赖包...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ✗ 依赖包安装失败
    pause
    exit /b 1
)
echo ✓ 依赖包安装成功

REM 运行测试
echo.
echo 运行系统测试...
python test.py

REM 询问用户要运行的模式
echo.
echo ==========================================
echo 请选择运行模式:
echo 1. 摄像头实时检测
echo 2. 处理视频文件
echo 3. 处理图片
echo 4. 查看示例
echo 5. 退出
echo ==========================================
set /p choice="请输入选项 (1-5): "

if "%choice%"=="1" (
    echo 启动摄像头检测...
    python main.py --camera 0
) else if "%choice%"=="2" (
    set /p video_path="请输入视频文件路径: "
    set /p output_path="请输入输出文件路径 (可选，直接回车跳过): "
    if "%output_path%"=="" (
        python main.py --video "%video_path%"
    ) else (
        python main.py --video "%video_path%" --output "%output_path%"
    )
) else if "%choice%"=="3" (
    set /p image_path="请输入图片文件路径: "
    set /p output_path="请输入输出文件路径 (可选，直接回车跳过): "
    if "%output_path%"=="" (
        python main.py --image "%image_path%"
    ) else (
        python main.py --image "%image_path%" --output "%output_path%"
    )
) else if "%choice%"=="4" (
    echo 查看示例...
    python examples.py
) else if "%choice%"=="5" (
    echo 退出
    exit /b 0
) else (
    echo 无效选项
    pause
    exit /b 1
)

deactivate
pause
