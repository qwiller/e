# 🌟 银河麒麟智能问答助手

> 基于RAG技术和麒麟SDK2.5的专业智能问答系统，专为银河麒麟操作系统打造

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Kylin](https://img.shields.io/badge/platform-银河麒麟-red.svg)](https://www.kylinos.cn)

## 📋 项目简介

银河麒麟智能问答助手是一个专门为银河麒麟操作系统设计的智能问答系统，集成了最新的RAG（检索增强生成）技术和麒麟SDK2.5，能够为用户提供专业、准确的系统相关问题解答。

### 🎯 核心功能

- **🧠 智能问答**: 基于RAG技术，结合本地文档知识库和硅基流动AI大模型
- **🎤 语音交互**: 支持中文语音输入和智能语音播报
- **📚 文档处理**: 支持PDF、Word、Markdown等多种格式文档的智能解析
- **🔧 系统集成**: 基于麒麟SDK2.5的154个标准化接口，实时获取系统信息
- **🖥️ 现代界面**: 专为麒麟系统优化的图形用户界面
- **🛡️ 安全可控**: 集成麒麟系统安全审计和访问控制机制
- **🔌 硬件兼容**: 支持飞腾、龙芯、海光等国产处理器平台

## 🚀 超简单安装（3步完成）

> **专为初学者设计，无需复杂配置！**

### 📥 第一步：下载项目
```bash
git clone https://github.com/qwiller/d.git
cd d
```

### ⚡ 第二步：一键安装
```bash
chmod +x easy_install.sh
./easy_install.sh
```
*完全自动化安装，包含所有依赖和麒麟SDK*

### 🚀 第三步：启动使用
```bash
chmod +x start.sh
./start.sh
```
*首次启动会引导您配置API密钥*

**🎉 就是这么简单！3步完成，立即使用！**

---

### 📖 详细安装指南

如果需要了解详细的安装步骤，请查看 [QUICK_START.md](QUICK_START.md) 或继续阅读下面的详细指南。

## 📦 详细安装指南（麒麟操作系统）

### 环境要求

- **操作系统**: 银河麒麟 V10 SP1/SP2/SP3 或更高版本
- **Python版本**: Python 3.8 或更高版本
- **处理器**: 支持 x86_64、ARM64（飞腾、鲲鹏）、MIPS64（龙芯）、x86（海光）
- **内存**: 建议 4GB 或更多
- **存储**: 至少 2GB 可用空间

### 第一步：系统环境准备

```bash
# 更新系统包列表
sudo apt update && sudo apt upgrade -y

# 安装基础开发工具
sudo apt install -y \
    build-essential \
    python3-dev \
    python3-pip \
    git \
    curl \
    wget \
    vim

# 检查Python版本（需要3.8+）
python3 --version
```

### 第二步：安装麒麟SDK2.5

```bash
# 添加麒麟官方软件源（如果尚未添加）
echo "deb http://archive.kylinos.cn/kylin/KYLIN-ALL 10.1 main restricted universe multiverse" | sudo tee /etc/apt/sources.list.d/kylin.list

# 更新软件源
sudo apt update

# 安装麒麟SDK核心包
sudo apt install -y \
    libkysdk-base-dev \
    libkysdk-system-dev \
    libkysdk-desktop-dev \
    libkysdk-security-dev \
    libkysdk-coreai-vision-dev

# 安装系统能力包
sudo apt install -y \
    libkysdk-system \
    libkysdk-system-dbus \
    libkysdk-system-python \
    libkysdk-systime-dev \
    libkysdk-applications-dev \
    libkysdk-diagnostics-dev \
    libkysdk-net-dev \
    libkysdk-hw-dev \
    libkysdk-res-dev \
    libkysdk-print-dev

# 安装D-Bus相关依赖
sudo apt install -y \
    libdbus-1-dev \
    libdbus-glib-1-dev \
    python3-dbus

# 验证SDK安装
ls /usr/lib/*/libkysysinfo.so 2>/dev/null && echo "✅ 麒麟SDK安装成功" || echo "❌ 麒麟SDK安装失败"
```

### 第三步：安装音频和语音依赖

```bash
# 安装音频系统依赖
sudo apt install -y \
    portaudio19-dev \
    python3-pyaudio \
    alsa-utils \
    libasound2-dev \
    pulseaudio \
    pulseaudio-utils

# 安装语音合成引擎
sudo apt install -y \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    festival \
    festvox-kallpc16k

# 配置音频权限
sudo usermod -a -G audio $USER

# 测试音频设备
aplay -l  # 列出音频设备
```

### 第四步：安装Python依赖

```bash
# 配置pip使用国内镜像源（提高下载速度）
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 120
retries = 3
EOF

# 升级pip到最新版本
python3 -m pip install --upgrade pip

# 克隆项目代码
git clone https://github.com/qwiller/d.git
cd d

# 安装项目依赖
pip3 install -r requirements.txt

# 如果遇到编译错误，可以尝试单独安装问题包
# pip3 install --only-binary=all SpeechRecognition pyttsx3
```

### 第五步：配置和测试

```bash
# 1. 配置API密钥（编辑config.py文件）
vim config.py
# 找到 SILICONFLOW_API_KEY 并设置您的API密钥

# 2. 创建必要的目录
mkdir -p logs data/vector_db docs

# 3. 测试语音功能
python3 test_voice.py

# 4. 测试系统集成
python3 -c "
from src.system_info_helper import KylinSystemInfo
info = KylinSystemInfo()
print('✅ 系统信息获取成功:', info.get_os_info())
"

# 5. 启动应用
python3 main.py
```

## 🎯 使用指南

### 基本操作

1. **启动应用**
   ```bash
   python3 main.py
   ```

2. **添加文档到知识库**
   - 点击"添加文档"按钮
   - 选择PDF、Word、Markdown等格式的文档
   - 系统自动处理并添加到知识库

3. **智能问答**
   - 在输入框中输入问题
   - 勾选"包含系统信息"获取实时系统状态
   - 点击"提问"或按回车键

4. **语音交互**
   - 点击🎤按钮进行语音输入
   - 勾选🔊语音播报启用回答朗读
   - 支持中文语音识别和合成

5. **系统信息查看**
   - 点击"系统信息"按钮查看详细系统状态
   - 包括硬件信息、软件版本、网络状态等

### 高级功能

- **知识库管理**: 支持批量添加文档，自动去重和更新
- **语音设置**: 可调节语音识别语言、合成速度和音量
- **系统监控**: 实时监控系统资源使用情况
- **安全审计**: 集成麒麟系统安全机制

## 🛠️ 开发者指南

### 项目结构

```
银河麒麟智能问答助手/
├── main.py                    # 🚀 主程序入口
├── config.py                  # ⚙️ 配置文件
├── requirements.txt           # 📦 Python依赖
├── install.sh                # 🔧 自动安装脚本
├── run.sh                    # ▶️ 启动脚本
├── setup_voice.sh            # 🎤 语音功能配置
├── test_voice.py             # 🧪 语音功能测试
├── src/                      # 📁 源代码目录
│   ├── ai_models.py          # 🤖 AI模型接口
│   ├── rag_engine.py         # 🧠 RAG引擎
│   ├── vector_store.py       # 🗄️ 向量存储
│   ├── document_processor.py # 📄 文档处理
│   ├── system_info_helper.py # 🖥️ 系统信息
│   ├── voice_handler.py      # 🎵 语音处理
│   ├── gui.py               # 🖼️ 图形界面
│   └── dbus_helper.py       # 🔗 D-Bus接口
├── docs/                    # 📚 文档目录
├── data/                    # 💾 数据目录
│   └── vector_db/           # 🔢 向量数据库
├── logs/                    # 📝 日志目录
└── assets/                  # 🎨 资源文件
    └── icon.png             # 🖼️ 应用图标
```

### 核心模块说明

#### 🧠 RAG引擎 (`src/rag_engine.py`)
- 实现检索增强生成的核心逻辑
- 整合文档检索和AI生成功能
- 支持上下文构建和系统信息集成

#### 📄 文档处理器 (`src/document_processor.py`)
- 支持PDF、Word、Markdown等多种格式
- 智能文本分块和结构化提取
- 麒麟系统专业术语和关键词识别

#### 🗄️ 向量存储 (`src/vector_store.py`)
- 基于TF-IDF的轻量级向量化
- 支持文档增量添加和持久化存储
- 高效的余弦相似度检索算法

#### 🎵 语音处理器 (`src/voice_handler.py`)
- 中文语音识别（Google API + 离线备用）
- 智能语音合成（pyttsx3引擎）
- 自动环境噪音调整和配置优化

#### 🖥️ 系统信息助手 (`src/system_info_helper.py`)
- 集成麒麟SDK2.5的154个标准化接口
- 实时获取系统硬件和软件信息
- 支持多架构处理器（飞腾、龙芯、海光等）

#### 🤖 AI模型接口 (`src/ai_models.py`)
- 集成硅基流动API和多种大语言模型
- 专业的银河麒麟系统提示词优化
- 智能重试机制和错误处理

#### 🖼️ 图形界面 (`src/gui.py`)
- 基于tkinter的现代化界面设计
- 支持拖拽文档上传和知识库管理
- 集成语音输入和播报功能

## ⚠️ 故障排除

### 常见问题及解决方案

#### 1. 🔑 API密钥问题
```bash
# 问题：API调用失败
# 解决：检查config.py中的API密钥配置
vim config.py
# 确保 SILICONFLOW_API_KEY 设置正确
```

#### 2. 🎤 语音功能不可用
```bash
# 问题：语音识别或合成失败
# 解决：重新安装语音依赖
sudo apt install -y portaudio19-dev python3-pyaudio espeak espeak-data
pip3 install --force-reinstall SpeechRecognition pyttsx3

# 测试语音功能
python3 test_voice.py
```

#### 3. 🔧 麒麟SDK库找不到
```bash
# 问题：系统信息获取失败
# 解决：检查SDK库文件
ls /usr/lib/*/libkysysinfo.so

# 如果不存在，重新安装SDK
sudo apt update
sudo apt install -y libkysdk-base-dev libkysdk-system-dev
```

#### 4. 📦 Python依赖安装失败
```bash
# 问题：pip安装依赖失败
# 解决：使用国内镜像源
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt

# 或者单独安装失败的包
pip3 install --only-binary=all numpy scikit-learn
```

#### 5. 🖥️ GUI界面无法启动
```bash
# 问题：图形界面启动失败
# 解决：检查X11转发和显示环境
echo $DISPLAY
export DISPLAY=:0.0

# 安装tkinter（如果缺失）
sudo apt install -y python3-tk
```

#### 6. 💾 向量数据库错误
```bash
# 问题：文档处理或检索失败
# 解决：清理并重建向量数据库
rm -rf data/vector_db/*
# 重新启动应用并添加文档
```

### 性能优化建议

#### 🚀 系统性能优化
- **内存优化**: 建议8GB以上内存，可调整向量数据库缓存大小
- **存储优化**: 使用SSD存储提升文档处理速度
- **网络优化**: 配置稳定的网络连接以确保API调用成功

#### ⚙️ 配置优化
```python
# 在config.py中调整以下参数
VECTOR_CONFIG = {
    "chunk_size": 300,        # 减小分块大小以节省内存
    "max_results": 5,         # 减少检索结果数量
    "similarity_threshold": 0.2  # 提高相似度阈值
}

RAG_CONFIG = {
    "max_context_length": 1500,  # 减少上下文长度
    "temperature": 0.5           # 降低随机性提高稳定性
}
```

## 🔧 配置说明

### API配置
在 `config.py` 文件中配置您的API密钥：

```python
# 硅基流动API配置
SILICONFLOW_API_KEY = "your_api_key_here"  # 🔑 替换为您的API密钥
DEFAULT_MODEL = "Qwen/Qwen2.5-72B-Instruct"

# API参数配置
API_PARAMETERS = {
    "temperature": 0.7,        # 随机性控制（0.0-1.0）
    "max_tokens": 4096,        # 最大输出长度
    "top_p": 0.9,             # 采样概率
    "frequency_penalty": 0.0,  # 频率惩罚
    "presence_penalty": 0.0    # 新颖性惩罚
}

# 向量数据库配置
VECTOR_CONFIG = {
    "chunk_size": 500,        # 文档分块大小
    "chunk_overlap": 50,      # 分块重叠大小
    "similarity_threshold": 0.1,  # 相似度阈值
    "max_results": 10         # 最大检索结果数
}

# 语音配置
VOICE_CONFIG = {
    "recognition_language": "zh-CN",  # 识别语言
    "speech_rate": 150,              # 语音速度
    "speech_volume": 0.8             # 音量
}
```

### 环境变量配置（推荐）
为了安全起见，建议使用环境变量管理API密钥：

```bash
# 在 ~/.bashrc 中添加
export SILICONFLOW_API_KEY="your_api_key_here"

# 重新加载配置
source ~/.bashrc
```

## 📊 技术特性

### 🎯 核心技术栈
- **RAG技术**: 检索增强生成，结合文档检索和AI生成
- **向量化**: 基于TF-IDF的轻量级文档向量化
- **AI模型**: 硅基流动API，支持Qwen2.5系列大模型
- **系统集成**: 麒麟SDK2.5，154个标准化系统接口
- **语音技术**: Google语音识别 + pyttsx3语音合成
- **界面框架**: tkinter现代化GUI设计

### 🔒 安全特性
- **本地处理**: 文档在本地处理，保护数据隐私
- **API安全**: 支持环境变量管理API密钥
- **系统集成**: 集成麒麟系统安全审计机制
- **权限控制**: 基于麒麟系统用户权限管理

### 🚀 性能特性
- **轻量级**: 基于TF-IDF，无需GPU加速
- **高效检索**: 余弦相似度快速文档检索
- **智能缓存**: 向量数据库持久化存储
- **并发处理**: 支持多线程文档处理

## 📝 更新日志

### v2.6.1 (2025-06-16) - 最新版本
- ✨ **新增语音功能**: 完整的中文语音识别和合成
- 🔧 **优化文档处理**: 增强的结构化信息提取
- 🐛 **修复重复代码**: 清理配置文件和AI模型重复内容
- 📈 **性能优化**: 改进向量检索算法和内存使用
- 🎨 **界面增强**: 添加语音输入按钮和播报选项
- 🧪 **测试完善**: 新增语音功能测试脚本

### v2.6.0 (2025-06-01)
- 🎉 **初始版本发布**
- 🧠 **RAG引擎**: 完整的检索增强生成功能
- 🔧 **系统集成**: 集成麒麟SDK2.5
- 🤖 **AI集成**: 支持硅基流动API
- 📄 **文档处理**: 多格式文档解析和处理
- 🖥️ **GUI界面**: 基于tkinter的图形界面

## 🤝 贡献指南

欢迎为项目做出贡献！请遵循以下步骤：

1. **Fork项目** 到您的GitHub账户
2. **创建功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建Pull Request**

### 开发环境设置
```bash
# 克隆您的fork
git clone https://github.com/yourusername/d.git
cd d

# 安装开发依赖
pip3 install -r requirements.txt
pip3 install pytest black flake8  # 开发工具

# 运行测试
python3 -m pytest tests/
```

## 📞 支持与反馈

- **问题报告**: [GitHub Issues](https://github.com/qwiller/d/issues)
- **功能请求**: [GitHub Discussions](https://github.com/qwiller/d/discussions)
- **技术支持**: 请在Issues中详细描述问题和环境信息

## 📄 许可证

本项目采用 **MIT许可证**。详情请参见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢以下项目和组织的支持：
- **银河麒麟操作系统** - 提供系统平台和SDK支持
- **硅基流动** - 提供AI大模型API服务
- **开源社区** - 提供优秀的开源库和工具

---

<div align="center">

**🌟 如果这个项目对您有帮助，请给我们一个Star！🌟**

Made with ❤️ for 银河麒麟操作系统

</div>
