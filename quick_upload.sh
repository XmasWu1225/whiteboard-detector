#!/bin/bash

# 快速上传脚本 - 简化版

echo "=========================================="
echo "快速上传到 GitHub"
echo "=========================================="
echo ""

# 获取 GitHub 用户名
read -p "请输入你的 GitHub 用户名: " username

if [ -z "$username" ]; then
    echo "错误: 用户名不能为空"
    exit 1
fi

# 仓库名称
repo_name="whiteboard-detector"

echo ""
echo "准备上传到: https://github.com/$username/$repo_name"
echo ""

# 检查远程仓库是否已存在
if git remote get-url origin &> /dev/null; then
    echo "远程仓库已存在，更新 URL..."
    git remote set-url origin "https://github.com/$username/$repo_name.git"
else
    echo "添加远程仓库..."
    git remote add origin "https://github.com/$username/$repo_name.git"
fi

echo ""
echo "=========================================="
echo "重要提示"
echo "=========================================="
echo ""
echo "请先在 GitHub 上创建仓库:"
echo ""
echo "1. 访问: https://github.com/new"
echo "2. 仓库名称: $repo_name"
echo "3. 描述: Whiteboard Detection System based on YOLOv5"
echo "4. 选择 Public 或 Private"
echo "5. 不要初始化 README、.gitignore 或 license"
echo "6. 点击 'Create repository'"
echo ""
read -p "完成上述步骤后，按回车键继续..."

# 推送代码
echo ""
echo "推送代码到 GitHub..."
echo ""

git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ 上传成功！"
    echo "=========================================="
    echo "仓库地址: https://github.com/$username/$repo_name"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "✗ 上传失败"
    echo "=========================================="
    echo ""
    echo "可能的原因:"
    echo "1. 仓库未创建或仓库名称错误"
    echo "2. 用户名错误"
    echo "3. 网络连接问题"
    echo "4. 需要认证（使用 Personal Access Token）"
    echo ""
    echo "请检查后重试，或查看详细指南:"
    echo "  cat GITHUB_UPLOAD_GUIDE.md"
fi
