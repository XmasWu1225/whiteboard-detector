#!/bin/bash

echo "=========================================="
echo "GitHub 仓库创建和上传脚本"
echo "=========================================="
echo ""

# 检查是否在项目目录中
if [ ! -f "main.py" ]; then
    echo "错误: 请在 whiteboard_detector 项目目录中运行此脚本"
    exit 1
fi

echo "请提供以下信息来创建 GitHub 仓库:"
echo ""

# 获取用户输入
read -p "GitHub 用户名: " github_username
read -p "仓库名称 (默认: whiteboard-detector): " repo_name
read -p "仓库描述 (默认: Whiteboard Detection System based on YOLOv5): " repo_description

# 设置默认值
repo_name=${repo_name:-whiteboard-detector}
repo_description=${repo_description:-"Whiteboard Detection System based on YOLOv5"}

echo ""
echo "=========================================="
echo "创建 GitHub 仓库"
echo "=========================================="
echo "用户名: $github_username"
echo "仓库名称: $repo_name"
echo "描述: $repo_description"
echo ""

# 检查是否已配置 Git
if ! git config user.name > /dev/null 2>&1; then
    echo "错误: Git 用户未配置"
    echo "请运行: git config --global user.name 'Your Name'"
    echo "       git config --global user.email 'your.email@example.com'"
    exit 1
fi

# 方法 1: 使用 GitHub CLI (如果已安装)
if command -v gh &> /dev/null; then
    echo "检测到 GitHub CLI，使用 gh 创建仓库..."
    
    gh repo create "$repo_name" --public --description "$repo_description" --source=. --remote=origin --push
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ 仓库创建成功并已推送代码！"
        echo "仓库地址: https://github.com/$github_username/$repo_name"
        exit 0
    else
        echo "使用 GitHub CLI 失败，尝试手动方法..."
    fi
fi

# 方法 2: 手动创建仓库
echo ""
echo "=========================================="
echo "手动创建 GitHub 仓库"
echo "=========================================="
echo ""
echo "请按照以下步骤操作:"
echo ""
echo "1. 访问: https://github.com/new"
echo "2. 仓库名称: $repo_name"
echo "3. 描述: $repo_description"
echo "4. 选择 Public 或 Private"
echo "5. 不要初始化 README、.gitignore 或 license"
echo "6. 点击 'Create repository'"
echo ""
read -p "按回车键继续，完成上述步骤后..."

# 添加远程仓库
echo ""
echo "添加远程仓库..."
git remote add origin "https://github.com/$github_username/$repo_name.git" 2>/dev/null || {
    echo "远程仓库已存在，更新 URL..."
    git remote set-url origin "https://github.com/$github_username/$repo_name.git"
}

# 推送代码
echo ""
echo "推送代码到 GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ 代码上传成功！"
    echo "=========================================="
    echo "仓库地址: https://github.com/$github_username/$repo_name"
    echo ""
    echo "下一步:"
    echo "1. 访问仓库地址查看代码"
    echo "2. 添加 README.md 中的徽章"
    echo "3. 设置仓库主题和描述"
    echo "4. 添加 Issues 和 Projects"
else
    echo ""
    echo "=========================================="
    echo "✗ 代码上传失败"
    echo "=========================================="
    echo ""
    echo "请检查:"
    echo "1. GitHub 仓库是否正确创建"
    echo "2. 仓库名称和用户名是否正确"
    echo "3. 是否有 GitHub 访问权限"
    echo "4. 网络连接是否正常"
    echo ""
    echo "手动推送命令:"
    echo "  git remote add origin https://github.com/$github_username/$repo_name.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
fi
