#!/bin/bash
# 银河麒麟智能问答助手 - 超简单一键安装脚本
# 专为初学者设计，完全自动化安装

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 显示带颜色的消息
print_step() {
    echo -e "${BLUE}[步骤 $1/8]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# 显示欢迎信息
clear
echo -e "${PURPLE}"
echo "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟"
echo "🌟                                                          🌟"
echo "🌟        银河麒麟智能问答助手 - 超简单一键安装              🌟"
echo "🌟                                                          🌟"
echo "🌟        🤖 集成RAG技术 + 🎤 语音交互 + 🔧 系统集成        🌟"
echo "🌟                                                          🌟"
echo "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟"
echo -e "${NC}"
echo
echo -e "${CYAN}📋 安装过程完全自动化，您只需要等待即可！${NC}"
echo -e "${CYAN}⏱️  预计安装时间：5-10分钟（取决于网络速度）${NC}"
echo

# 检查用户权限
if [[ $EUID -eq 0 ]]; then
   print_error "请不要使用root用户运行此脚本"
   print_info "正确的使用方式: ./easy_install.sh"
   exit 1
fi

# 等待用户确认
read -p "🚀 按回车键开始安装，或按Ctrl+C取消..." -r
echo

# 步骤1：系统检查
print_step 1 "检查系统环境"
echo "   🔍 检查操作系统..."
if [ -f "/etc/kylin-release" ] || grep -q "Kylin" /etc/os-release 2>/dev/null; then
    KYLIN_VERSION=$(cat /etc/kylin-release 2>/dev/null || grep "VERSION" /etc/os-release | cut -d'"' -f2)
    print_success "检测到银河麒麟系统: $KYLIN_VERSION"
else
    print_warning "未检测到银河麒麟系统，某些功能可能受限"
fi

echo "   🔍 检查系统架构..."
ARCH=$(uname -m)
print_info "系统架构: $ARCH"

echo "   🔍 检查Python环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python环境: $PYTHON_VERSION"
else
    print_error "未找到Python3，将自动安装"
fi

# 步骤2：更新系统
print_step 2 "更新系统包列表"
echo "   📦 正在更新软件包列表..."
sudo apt update -qq
print_success "系统包列表更新完成"

# 步骤3：安装基础依赖
print_step 3 "安装基础系统依赖"
echo "   📦 安装Python和开发工具..."
sudo apt install -y -qq \
    python3 \
    python3-pip \
    python3-dev \
    python3-tk \
    python3-venv \
    build-essential \
    git \
    curl \
    wget \
    vim \
    unzip > /dev/null 2>&1

print_success "基础依赖安装完成"

# 步骤4：安装麒麟SDK
print_step 4 "安装麒麟SDK和系统集成组件"
echo "   🔧 安装麒麟SDK开发包..."

# 尝试安装麒麟SDK，如果失败则跳过
{
    sudo apt install -y -qq \
        libkysdk-base-dev \
        libkysdk-system-dev \
        libkysdk-desktop-dev \
        libkysdk-security-dev \
        libkysdk-system \
        libkysdk-system-dbus \
        libkysdk-system-python \
        libdbus-1-dev \
        libdbus-glib-1-dev \
        python3-dbus > /dev/null 2>&1
    print_success "麒麟SDK安装完成"
} || {
    print_warning "麒麟SDK安装失败，系统信息功能可能受限"
}

# 步骤5：安装语音依赖
print_step 5 "安装语音功能依赖"
echo "   🎤 安装语音识别和合成组件..."
{
    sudo apt install -y -qq \
        portaudio19-dev \
        python3-pyaudio \
        alsa-utils \
        libasound2-dev \
        pulseaudio \
        pulseaudio-utils \
        espeak \
        espeak-data \
        libespeak1 \
        libespeak-dev > /dev/null 2>&1
    
    # 配置音频权限
    sudo usermod -a -G audio $USER > /dev/null 2>&1
    print_success "语音依赖安装完成"
} || {
    print_warning "语音依赖安装失败，语音功能可能不可用"
}

# 步骤6：配置Python环境
print_step 6 "配置Python环境和依赖"
echo "   🐍 配置pip镜像源..."
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 120
retries = 3
EOF

echo "   🐍 升级pip..."
python3 -m pip install --upgrade pip -q

echo "   🐍 安装Python依赖包..."
# 分批安装，提高成功率
pip3 install -q requests numpy scikit-learn jieba
pip3 install -q pdfplumber python-docx beautifulsoup4 lxml
pip3 install -q SpeechRecognition pyttsx3 || print_warning "语音包安装失败"

print_success "Python环境配置完成"

# 步骤7：创建目录和配置
print_step 7 "创建必要目录和配置文件"
echo "   📁 创建应用目录..."
mkdir -p logs data/vector_db docs assets

echo "   ⚙️ 检查配置文件..."
if [ -f "config.py" ]; then
    print_success "配置文件已存在"
elif [ -f "config_template.py" ]; then
    print_info "从模板创建配置文件..."
    cp config_template.py config.py
    print_success "配置文件创建完成"
else
    print_warning "配置文件和模板都不存在，请检查项目完整性"
fi

print_success "目录和配置创建完成"

# 步骤8：最终测试
print_step 8 "测试安装结果"
echo "   🧪 测试Python模块..."
python3 -c "
import sys
modules = ['requests', 'numpy', 'sklearn', 'jieba']
success_count = 0
for module in modules:
    try:
        __import__(module)
        success_count += 1
    except ImportError:
        pass
print(f'Python模块测试: {success_count}/{len(modules)} 成功')
" 2>/dev/null

echo "   🧪 测试语音功能..."
python3 -c "
try:
    import speech_recognition
    import pyttsx3
    print('语音功能: 可用')
except ImportError:
    print('语音功能: 不可用')
" 2>/dev/null

print_success "安装测试完成"

# 显示完成信息
echo
echo -e "${GREEN}🎉🎉🎉 安装完成！🎉🎉🎉${NC}"
echo
echo -e "${PURPLE}📋 下一步操作：${NC}"
echo -e "${CYAN}1. 配置API密钥：${NC}"
echo "   编辑 config.py 文件，设置您的硅基流动API密钥"
echo "   获取密钥：https://cloud.siliconflow.cn"
echo
echo -e "${CYAN}2. 启动应用：${NC}"
echo "   python3 main.py"
echo
echo -e "${CYAN}3. 测试语音功能：${NC}"
echo "   python3 test_voice.py"
echo
echo -e "${YELLOW}⚠️  重要提醒：${NC}"
echo "   - 如果语音功能不工作，请重新登录系统以应用音频权限"
echo "   - 首次运行可能需要下载语音模型，请保持网络连接"
echo
echo -e "${BLUE}❓ 如遇问题：${NC}"
echo "   - 查看 README.md 中的故障排除部分"
echo "   - 运行 python3 test_voice.py 测试语音功能"
echo
echo -e "${GREEN}🌟 感谢使用银河麒麟智能问答助手！${NC}"
