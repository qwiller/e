#!/bin/bash
# 麒麟SDK自动安装脚本 - 基于开发指南

set -e

echo "======================================"
echo "麒麟SDK2.5自动安装程序"
echo "======================================"

# 检测系统类型
if [ -f "/etc/kylin-release" ] || grep -q "Kylin" /etc/os-release 2>/dev/null; then
    echo "✓ 检测到银河麒麟操作系统"
    KYLIN_NATIVE=true
else
    echo "⚠ 非麒麟系统，将尝试添加软件源"
    KYLIN_NATIVE=false
fi

# 检查权限
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用sudo运行此脚本"
    exit 1
fi

# 更新系统
echo "📦 更新系统包列表..."
apt update

# 安装Python和pip（麒麟系统环境准备）
echo "🐍 安装Python环境..."
apt-get install -y python3 python3-pip python3-dev python3-venv
apt-get install -y python3-setuptools python3-wheel

# 验证Python安装
echo "✅ 验证Python安装..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python安装成功: $PYTHON_VERSION"
else
    echo "❌ Python安装失败"
    exit 1
fi

if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo "✓ pip安装成功: $PIP_VERSION"
else
    echo "❌ pip安装失败"
    exit 1
fi

# 升级pip到最新版本
echo "📦 升级pip到最新版本..."
python3 -m pip install --upgrade pip

# 安装基础开发工具
echo "🔧 安装基础开发工具..."
apt-get install -y build-essential cmake pkg-config
apt-get install -y libstdc++-dev libgl1-mesa-dev
apt-get install -y gdb gcc g++

# 根据系统类型安装SDK
if [ "$KYLIN_NATIVE" = true ]; then
    echo "🏠 在麒麟系统上安装SDK..."
    apt-get install -y libkysdk-base-dev libkysdk-system-dev \
                       libkysdk-desktop-dev libkysdk-security-dev \
                       libkysdk-coreai-vision-dev
else
    echo "🌐 添加麒麟软件源..."
    # 添加软件源
    echo "deb http://archive.kylinos.cn/kylin/KYLIN-ALL developer-kits main restricted universe" > /etc/apt/sources.list.d/kylin-sdk.list
    
    # 更新并安装
    apt update
    apt-get install -y libkysdk-base-dev libkysdk-system-dev \
                       libkysdk-desktop-dev libkysdk-security-dev \
                       libkysdk-coreai-vision-dev
fi

# 安装语音相关依赖
echo "🎤 安装语音功能依赖..."
apt-get install -y portaudio19-dev espeak espeak-data
apt-get install -y pulseaudio pulseaudio-utils
apt-get install -y alsa-utils libasound2-dev

# 验证安装
echo "✅ 验证SDK安装..."
SDK_LIBS=(
    "/usr/lib/*/libkysysinfo.so"
    "/usr/lib/*/libkyhardware.so"
    "/usr/lib/*/libkydate.so"
    "/usr/lib/*/libkypackage.so"
)

for lib_pattern in "${SDK_LIBS[@]}"; do
    if ls $lib_pattern 1> /dev/null 2>&1; then
        echo "✓ 找到SDK库: $(ls $lib_pattern | head -1)"
    else
        echo "⚠ 未找到SDK库: $lib_pattern"
    fi
done

# 设置环境变量
echo "🔧 配置环境变量..."
echo 'export KYSDK_PATH=/usr/lib' >> /etc/environment
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib' >> /etc/environment

echo "🎉 麒麟SDK安装完成！"
echo "请重新登录以使环境变量生效"