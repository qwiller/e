#!/bin/bash
# 银河麒麟智能问答助手 - 快速部署脚本
# 适用于银河麒麟操作系统 V10 SP1/SP2/SP3

set -e  # 遇到错误立即退出

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

# 检查是否为root用户
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "请不要使用root用户运行此脚本"
        log_info "正确的使用方式: ./quick_deploy.sh"
        exit 1
    fi
}

# 检查麒麟系统
check_kylin_system() {
    log_info "检查操作系统..."
    
    if [ -f "/etc/kylin-release" ] || grep -q "Kylin" /etc/os-release 2>/dev/null; then
        KYLIN_VERSION=$(cat /etc/kylin-release 2>/dev/null || grep "VERSION" /etc/os-release | cut -d'"' -f2)
        log_success "检测到银河麒麟操作系统: $KYLIN_VERSION"
    else
        log_warning "未检测到银河麒麟系统，某些功能可能无法正常工作"
        read -p "是否继续安装？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# 检查系统架构
check_architecture() {
    ARCH=$(uname -m)
    log_info "检测到系统架构: $ARCH"
    
    case $ARCH in
        x86_64)
            log_success "支持的架构: x86_64"
            ;;
        aarch64|arm64)
            log_success "支持的架构: ARM64 (飞腾/鲲鹏)"
            ;;
        mips64)
            log_success "支持的架构: MIPS64 (龙芯)"
            ;;
        *)
            log_warning "未测试的架构: $ARCH，可能存在兼容性问题"
            ;;
    esac
}

# 检查Python版本
check_python() {
    log_info "检查Python环境..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "未找到Python3，请先安装Python 3.8+"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    log_info "Python版本: $PYTHON_VERSION"
    
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        log_success "Python版本满足要求 (>= 3.8)"
    else
        log_error "Python版本过低，需要3.8或更高版本"
        exit 1
    fi
}

# 安装系统依赖
install_system_dependencies() {
    log_info "安装系统依赖..."
    
    # 更新包列表
    sudo apt update
    
    # 安装基础开发工具
    sudo apt install -y \
        build-essential \
        python3-dev \
        python3-pip \
        git \
        curl \
        wget \
        vim \
        python3-tk
    
    log_success "基础依赖安装完成"
}

# 安装麒麟SDK
install_kylin_sdk() {
    log_info "安装麒麟SDK2.5..."
    
    # 检查是否已有麒麟软件源
    if ! grep -q "archive.kylinos.cn" /etc/apt/sources.list.d/* 2>/dev/null; then
        log_info "添加麒麟官方软件源..."
        echo "deb http://archive.kylinos.cn/kylin/KYLIN-ALL 10.1 main restricted universe multiverse" | sudo tee /etc/apt/sources.list.d/kylin.list
        sudo apt update
    fi
    
    # 安装SDK包
    sudo apt install -y \
        libkysdk-base-dev \
        libkysdk-system-dev \
        libkysdk-desktop-dev \
        libkysdk-security-dev \
        libkysdk-coreai-vision-dev \
        libkysdk-system \
        libkysdk-system-dbus \
        libkysdk-system-python \
        libdbus-1-dev \
        libdbus-glib-1-dev \
        python3-dbus
    
    # 验证安装
    if ls /usr/lib/*/libkysysinfo.so 1> /dev/null 2>&1; then
        log_success "麒麟SDK安装成功"
    else
        log_warning "麒麟SDK库文件未找到，系统信息功能可能受限"
    fi
}

# 安装语音依赖
install_voice_dependencies() {
    log_info "安装语音功能依赖..."
    
    sudo apt install -y \
        portaudio19-dev \
        python3-pyaudio \
        alsa-utils \
        libasound2-dev \
        pulseaudio \
        pulseaudio-utils \
        espeak \
        espeak-data \
        libespeak1 \
        libespeak-dev \
        festival \
        festvox-kallpc16k
    
    # 配置音频权限
    sudo usermod -a -G audio $USER
    
    log_success "语音依赖安装完成"
}

# 配置pip镜像源
configure_pip() {
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
    python3 -m pip install --upgrade pip
    
    log_success "pip配置完成"
}

# 安装Python依赖
install_python_dependencies() {
    log_info "安装Python依赖包..."
    
    # 安装项目依赖
    pip3 install -r requirements.txt
    
    log_success "Python依赖安装完成"
}

# 创建必要目录
create_directories() {
    log_info "创建必要的目录..."
    
    mkdir -p logs data/vector_db docs assets
    
    log_success "目录创建完成"
}

# 配置API密钥
configure_api_key() {
    log_info "配置API密钥..."
    
    if grep -q "YOUR_API_KEY_HERE" config.py; then
        log_warning "检测到默认API密钥，需要配置您的硅基流动API密钥"
        echo
        echo "请访问 https://cloud.siliconflow.cn 获取您的API密钥"
        echo "然后编辑 config.py 文件，将 SILICONFLOW_API_KEY 设置为您的密钥"
        echo
        read -p "是否现在配置API密钥？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "请输入您的API密钥: " api_key
            if [ ! -z "$api_key" ]; then
                sed -i "s/sk-owsayozifrzvaxuxvyvywmyzcceokwatdbolevdnfnbwlurp/$api_key/g" config.py
                log_success "API密钥配置完成"
            fi
        fi
    else
        log_success "API密钥已配置"
    fi
}

# 测试安装
test_installation() {
    log_info "测试安装..."
    
    # 测试Python模块导入
    python3 -c "
import sys
modules = ['requests', 'numpy', 'sklearn', 'jieba']
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError:
        print(f'✗ {module} - 导入失败')
" || log_warning "部分Python模块测试失败"
    
    # 测试语音功能
    log_info "测试语音功能..."
    python3 test_voice.py || log_warning "语音功能测试失败"
    
    # 测试系统信息
    log_info "测试系统信息获取..."
    python3 -c "
try:
    from src.system_info_helper import KylinSystemInfo
    info = KylinSystemInfo()
    print('✓ 系统信息获取成功')
except Exception as e:
    print(f'✗ 系统信息获取失败: {e}')
" || log_warning "系统信息功能测试失败"
    
    log_success "安装测试完成"
}

# 显示使用说明
show_usage() {
    echo
    log_success "🎉 银河麒麟智能问答助手安装完成！"
    echo
    echo "📋 使用说明:"
    echo "1. 启动应用: python3 main.py"
    echo "2. 测试语音: python3 test_voice.py"
    echo "3. 查看日志: tail -f logs/app.log"
    echo
    echo "🔧 配置文件: config.py"
    echo "📚 文档目录: docs/"
    echo "💾 数据目录: data/"
    echo
    echo "❓ 如遇问题，请查看 README.md 中的故障排除部分"
    echo
}

# 主函数
main() {
    echo "🌟 银河麒麟智能问答助手 - 快速部署脚本"
    echo "=================================================="
    echo
    
    check_root
    check_kylin_system
    check_architecture
    check_python
    
    echo
    log_info "开始安装..."
    
    install_system_dependencies
    install_kylin_sdk
    install_voice_dependencies
    configure_pip
    install_python_dependencies
    create_directories
    configure_api_key
    test_installation
    
    show_usage
}

# 运行主函数
main "$@"
