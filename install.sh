#!/bin/bash
# 银河麒麟智能问答助手安装脚本 - 完整优化版
# 版本: v4.0.0 - 适配中国大陆网络环境
# 支持离线安装和国内镜像源

set -e

echo "======================================"
echo "银河麒麟智能问答助手安装程序 v4.0.0"
echo "一键安装 - 国内网络环境优化版"
echo "======================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 错误处理函数
handle_error() {
    log_error "安装过程中出现错误，正在尝试恢复..."
    log_info "请检查网络连接和系统权限"
    exit 1
}

# 设置错误处理
trap handle_error ERR

# 检查权限
if [ "$EUID" -ne 0 ]; then
    log_error "请使用sudo运行此安装脚本"
    echo "使用方法: sudo bash install1.sh"
    exit 1
fi

# 检查系统类型
log_info "检查系统兼容性..."
if [ -f "/etc/kylin-release" ] || grep -q "Kylin" /etc/os-release 2>/dev/null; then
    log_success "检测到银河麒麟操作系统"
    KYLIN_NATIVE=true
else
    log_warning "此程序专为银河麒麟系统设计"
    read -p "是否继续安装? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    KYLIN_NATIVE=false
fi

# 配置国内软件源
log_info "配置国内软件源..."
cp /etc/apt/sources.list /etc/apt/sources.list.backup

# 添加清华大学镜像源
cat > /etc/apt/sources.list.d/tsinghua.list << EOF
# 清华大学镜像源
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse
EOF

# 更新系统包列表
log_info "更新系统包列表..."
apt-get update || {
    log_warning "包列表更新失败，尝试修复..."
    apt-get update --fix-missing
}

# 安装基础系统依赖
log_info "安装基础系统依赖..."
apt-get install -y \
    curl wget git \
    build-essential cmake pkg-config \
    libstdc++-9-dev libgl1-mesa-dev \
    gdb gcc g++ || {
    log_error "基础依赖安装失败"
    exit 1
}

# 安装Python环境和开发包
log_info "安装Python环境和开发包..."
apt-get install -y \
    python3 python3-pip python3-dev python3-venv \
    python3-setuptools python3-wheel \
    python3-distutils || {
    log_error "Python环境安装失败"
    exit 1
}

# 验证Python安装
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    log_success "Python安装成功: $PYTHON_VERSION"
else
    log_error "Python安装失败"
    exit 1
fi

if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    log_success "pip安装成功: $PIP_VERSION"
else
    log_error "pip安装失败"
    exit 1
fi

# 配置pip使用国内镜像源
log_info "配置pip国内镜像源..."
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 120
retries = 3
EOF

# 升级pip
log_info "升级pip到最新版本..."
python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple || {
    log_warning "pip升级失败，继续使用当前版本"
}

# 安装音频系统依赖（解决pyaudio编译问题）
log_info "安装音频系统依赖..."
apt-get install -y \
    portaudio19-dev python3-pyaudio \
    espeak espeak-data libespeak1 libespeak-dev \
    festival festvox-kallpc16k \
    alsa-utils libasound2-dev \
    pulseaudio pulseaudio-utils || {
    log_warning "部分音频依赖安装失败，语音功能可能受限"
}

# 安装麒麟SDK
log_info "安装麒麟SDK2.5..."
if [ "$KYLIN_NATIVE" = true ]; then
    log_info "在麒麟系统上安装SDK..."
    
    # 基础SDK包
    SDK_PACKAGES=(
        "libkysdk-base-dev"
        "libkysdk-system-dev"
        "libkysdk-desktop-dev"
        "libkysdk-security-dev"
        "libkysdk-system"
        "libkysdk-system-dbus"
        "libkysdk-system-python"
        "libkysdk-systime-dev"
        "libkysdk-applications-dev"
        "libkysdk-diagnostics-dev"
        "libkysdk-net-dev"
        "libkysdk-hw-dev"
        "libkysdk-res-dev"
        "libkysdk-print-dev"
    )
    
    # D-Bus相关包
    DBUS_PACKAGES=(
        "libdbus-1-dev"
        "libdbus-glib-1-dev"
        "python3-dbus"
        "python3-gi"
    )
    
    # 安装SDK包
    for package in "${SDK_PACKAGES[@]}"; do
        log_info "安装 $package..."
        apt-get install -y --timeout=60 "$package" || log_warning "$package 安装失败，继续安装其他包"
    done
    
    # 安装D-Bus包
    for package in "${DBUS_PACKAGES[@]}"; do
        log_info "安装 $package..."
        apt-get install -y --timeout=60 "$package" || log_warning "$package 安装失败，继续安装其他包"
    done
else
    log_info "添加麒麟软件源..."
    echo "deb http://archive.kylinos.cn/kylin/KYLIN-ALL developer-kits main restricted universe" > /etc/apt/sources.list.d/kylin-sdk.list
    apt-get update --timeout=30
    apt-get install -y --timeout=60 \
        libkysdk-base-dev libkysdk-system-dev \
        libkysdk-desktop-dev libkysdk-security-dev || {
        log_warning "SDK安装失败，部分功能可能不可用"
    }
fi

# 设置安装目录
INSTALL_DIR="/opt/kylin-qa-assistant"
log_info "设置安装目录: $INSTALL_DIR"

# 创建安装目录
mkdir -p "$INSTALL_DIR"

# 复制程序文件
log_info "复制程序文件..."
cp -r . "$INSTALL_DIR/" || {
    log_error "文件复制失败"
    exit 1
}

# 设置文件权限
log_info "设置文件权限..."
chown -R root:root "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/run.sh"
chmod +x "$INSTALL_DIR/main.py"
chmod +x "$INSTALL_DIR/"*.sh

# 创建数据目录
log_info "创建数据目录..."
mkdir -p "$INSTALL_DIR/data" "$INSTALL_DIR/logs" "$INSTALL_DIR/docs"
chmod 755 "$INSTALL_DIR/data" "$INSTALL_DIR/logs" "$INSTALL_DIR/docs"

# 安装Python依赖
log_info "安装Python依赖包..."
cd "$INSTALL_DIR"

# 设置pip配置以提高安装成功率
export PIP_DEFAULT_TIMEOUT=120
export PIP_RETRIES=3
export PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"

# 核心依赖列表（适配中国大陆网络环境）
CORE_DEPS=(
    "uvicorn==0.24.0"
    "requests==2.31.0"
    "numpy==1.24.3"
    "pandas==2.0.3"
    "scipy==1.10.1"
    "scikit-learn==1.3.0"
    "jieba==0.42.1"
    "psutil==5.9.6"
)

# 安装核心依赖
for dep in "${CORE_DEPS[@]}"; do
    log_info "安装 $dep..."
    pip3 install "$dep" -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout=120 || log_warning "$dep 安装失败，跳过"
done

# 可选依赖列表
OPTIONAL_DEPS=(
    "langchain==0.0.335"
    "openai==1.3.5"
    "PyPDF2==3.0.1"
    "python-docx==0.8.11"
    "SpeechRecognition==3.10.0"
    "pyttsx3==2.90"
    "Pillow==10.0.1"
    "httpx==0.25.2"
    "aiohttp==3.9.1"
    "markdown==3.5.1"
    "beautifulsoup4==4.12.2"
    "lxml==4.9.3"
    "zhconv==1.4.3"
)

# 安装可选依赖
for dep in "${OPTIONAL_DEPS[@]}"; do
    log_info "安装 $dep..."
    pip3 install "$dep" -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout=120 || log_warning "$dep 安装失败，相关功能可能不可用"
done

# 配置用户权限（允许普通用户运行）
log_info "配置用户权限..."
if id "kylin" &>/dev/null; then
    chown -R kylin:kylin "$INSTALL_DIR/data" "$INSTALL_DIR/logs"
fi

# 创建系统服务（可选）
log_info "创建系统服务..."
if [ -f "$INSTALL_DIR/kylin-qa.service" ]; then
    cp "$INSTALL_DIR/kylin-qa.service" /etc/systemd/system/
    systemctl daemon-reload
    log_success "系统服务已创建，可使用 systemctl start kylin-qa 启动"
fi

# 创建桌面快捷方式
log_info "创建桌面快捷方式..."
cat > /usr/share/applications/kylin-qa-assistant.desktop << EOF
[Desktop Entry]
Name=银河麒麟智能问答助手
Comment=基于麒麟SDK的智能问答系统
Exec=cd $INSTALL_DIR && python3 main.py
Icon=$INSTALL_DIR/assets/icon.png
Terminal=false
Type=Application
Categories=Office;Utility;
EOF

# 创建命令行快捷方式
log_info "创建命令行快捷方式..."
cat > /usr/local/bin/kylin-qa << EOF
#!/bin/bash
cd $INSTALL_DIR
python3 main.py "\$@"
EOF
chmod +x /usr/local/bin/kylin-qa

# 验证安装
log_info "验证安装结果..."
cd "$INSTALL_DIR"

# 检查Python模块
log_info "检查Python模块..."
python3 -c "
import sys
modules = ['requests', 'numpy', 'pandas', 'scipy', 'sklearn', 'jieba']
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError:
        print(f'✗ {module} - 安装失败')
" || log_warning "部分Python模块验证失败"

# 检查麒麟SDK
log_info "检查麒麟SDK..."
SDK_LIBS=(
    "/usr/lib/*/libkysysinfo.so"
    "/usr/lib/*/libkyhardware.so"
    "/usr/lib/*/libkydate.so"
)

for lib_pattern in "${SDK_LIBS[@]}"; do
    if ls $lib_pattern 1> /dev/null 2>&1; then
        log_success "找到SDK库: $(ls $lib_pattern | head -1)"
    else
        log_warning "未找到SDK库: $lib_pattern"
    fi
done

# 创建离线配置文件
log_info "创建离线配置文件..."
cat > "$INSTALL_DIR/config_offline.py" << EOF
# 离线配置文件 - 适用于无网络环境

# API配置 - 使用本地服务
API_CONFIG = {
    'base_url': 'http://localhost:8000',  # 本地API服务
    'api_key': 'local-key',
    'model': 'local-model',
    'timeout': 30
}

# 向量存储配置 - 使用本地TF-IDF
VECTOR_CONFIG = {
    'type': 'tfidf',  # 使用TF-IDF而非外部嵌入服务
    'model_path': './data/tfidf_model.pkl',
    'index_path': './data/vector_index.pkl'
}

# 禁用外网功能
DISABLE_ONLINE_FEATURES = True
OFFLINE_MODE = True
EOF

# 安装完成
echo
log_success "======================================"
log_success "🎉 安装完成！"
log_success "======================================"
echo
log_info "安装目录: $INSTALL_DIR"
log_info "启动方式:"
echo "  1. 命令行启动: kylin-qa"
echo "  2. 脚本启动: cd $INSTALL_DIR && ./run.sh"
echo "  3. 系统服务: systemctl start kylin-qa"
echo "  4. 桌面快捷方式: 在应用菜单中查找'银河麒麟智能问答助手'"
echo
log_info "配置文件: $INSTALL_DIR/config.py"
log_info "离线配置: $INSTALL_DIR/config_offline.py"
log_info "日志目录: $INSTALL_DIR/logs"
log_info "文档目录: $INSTALL_DIR/docs"
echo
log_warning "首次运行前请:"
echo "  1. 配置API密钥 (编辑 config.py)"
echo "  2. 或使用离线模式 (使用 config_offline.py)"
echo "  3. 添加知识文档到 docs/ 目录"
echo "  4. 检查系统权限和网络连接"
echo
log_success "感谢使用银河麒麟智能问答助手！"
echo
echo "网络环境说明:"
echo "- 本安装脚本已优化适配中国大陆网络环境"
echo "- 使用清华大学镜像源，避免访问外网资源"
echo "- 支持离线模式运行，无需外网API"
echo "- 如遇网络问题，请使用离线配置文件"
echo