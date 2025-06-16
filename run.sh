#!/bin/bash

# 银河麒麟智能问答助手启动脚本

echo "银河麒麟智能问答助手 v2.5"
echo "========================================"

# 检查是否为麒麟系统
if [ -f "/etc/kylin-release" ] || grep -q "Kylin" /etc/os-release 2>/dev/null; then
    echo "检测到银河麒麟操作系统"
else
    echo "警告: 未检测到银河麒麟系统，某些功能可能无法正常工作"
fi

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python版本: $PYTHON_VERSION"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到pip3，请先安装pip"
    exit 1
fi

# 检查依赖
echo "检查依赖项..."
if ! python3 -c "import numpy" 2>/dev/null; then
    echo "安装依赖项..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi

# 创建必要的目录
mkdir -p data logs docs

# 检查麒麟SDK库
echo "检查麒麟SDK库..."
SDK_LIBS=(
    "/usr/lib/aarch64-linux-gnu/libkysysinfo.so"
    "/usr/lib/x86_64-linux-gnu/libkysysinfo.so"
    "/usr/lib/libkysysinfo.so"
)

SDK_FOUND=false
for lib in "${SDK_LIBS[@]}"; do
    if [ -f "$lib" ]; then
        echo "找到麒麟SDK库: $lib"
        SDK_FOUND=true
        break
    fi
done

if [ "$SDK_FOUND" = false ]; then
    echo "警告: 未找到麒麟SDK库，系统信息功能可能受限"
fi

# 设置环境变量
export PYTHONPATH="$PWD/src:$PYTHONPATH"

# 启动程序
echo "启动银河麒麟智能问答助手..."
python3 main.py

if [ $? -ne 0 ]; then
    echo "程序运行出错"
    read -p "按任意键退出..."
fi