#!/bin/bash
# 银河麒麟智能问答助手 - 启动脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🌟 银河麒麟智能问答助手${NC}"
echo "================================"

# 检查配置文件
if [ ! -f "config.py" ]; then
    echo -e "${RED}❌ 配置文件 config.py 不存在${NC}"
    exit 1
fi

# 检查API密钥
if grep -q "YOUR_API_KEY_HERE" config.py || grep -q "sk-owsayozifrzvaxuxvyvywmyzcceokwatdbolevdnfnbwlurp" config.py; then
    echo -e "${YELLOW}⚠️  检测到默认API密钥，请先配置您的硅基流动API密钥${NC}"
    echo
    echo "📝 配置步骤："
    echo "1. 访问 https://cloud.siliconflow.cn 获取API密钥"
    echo "2. 编辑 config.py 文件"
    echo "3. 将 SILICONFLOW_API_KEY 设置为您的密钥"
    echo
    read -p "是否现在配置API密钥？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "请输入您的API密钥: " api_key
        if [ ! -z "$api_key" ]; then
            # 备份原配置文件
            cp config.py config.py.backup
            # 替换API密钥
            sed -i "s/sk-owsayozifrzvaxuxvyvywmyzcceokwatdbolevdnfnbwlurp/$api_key/g" config.py
            echo -e "${GREEN}✅ API密钥配置完成${NC}"
        else
            echo -e "${RED}❌ 未输入API密钥，程序退出${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠️  请手动配置API密钥后再启动${NC}"
        exit 1
    fi
fi

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到Python3，请先运行安装脚本${NC}"
    exit 1
fi

# 检查必要目录
mkdir -p logs data/vector_db docs

# 检查向量存储配置
echo -e "${BLUE}🔍 检查向量存储配置...${NC}"
if [ -d "./data/vector_db" ] && [ ! -f "./data/vector_db/vectors.pkl" ]; then
    echo -e "${GREEN}✅ 向量存储目录结构正确${NC}"
elif [ -f "./data/vector_db" ]; then
    echo -e "${YELLOW}⚠️  检测到向量存储路径问题，正在修复...${NC}"
    rm -f "./data/vector_db"
    mkdir -p "./data/vector_db"
    echo -e "${GREEN}✅ 向量存储路径已修复${NC}"
fi

# 检查系统状态
if [ ! -d "./data/vector_db" ]; then
    echo -e "${YELLOW}⚠️  首次运行，创建必要目录...${NC}"
    mkdir -p ./data/vector_db
    mkdir -p ./logs
    mkdir -p ./assets
fi

# 可选：运行系统测试
read -p "是否运行系统测试？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 test_system.py
    echo
fi

# 启动应用
echo -e "${GREEN}🚀 启动银河麒麟智能问答助手...${NC}"
echo

# 设置显示环境变量（如果需要）
export DISPLAY=${DISPLAY:-:0.0}

# 启动主程序
if [ -f "main.py" ]; then
    python3 main.py
else
    echo -e "${RED}❌ main.py 文件不存在${NC}"
    exit 1
fi
