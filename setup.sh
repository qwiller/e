#!/bin/bash
# 银河麒麟智能问答助手安装程序 v4.0.0
# 一键安装 - 国内网络环境优化版

set -e

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

echo "======================================"
echo "银河麒麟智能问答助手安装程序 v4.0.0"
echo "一键安装 - 国内网络环境优化版"
echo "======================================"
echo

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    log_error "请使用sudo运行此安装脚本"
    echo "使用方法: sudo bash setup.sh"
    exit 1
fi

# 设置脚本目录
SCRIPT_DIR=$(dirname $(readlink -f "$0"))

# 检查安装脚本是否存在
if [ ! -f "$SCRIPT_DIR/install.sh" ]; then
    log_error "安装脚本 install.sh 未找到"
    exit 1
fi

# 设置安装脚本为可执行
log_info "正在设置安装脚本为可执行..."
chmod +x "$SCRIPT_DIR/install.sh"

# 运行安装脚本
log_info "正在开始安装过程..."
"$SCRIPT_DIR/install.sh"

# 安装完成后
log_success "安装完成！"
echo "如果遇到任何问题，请查看日志文件"
echo "按任意键退出..."
read -n 1 -s
