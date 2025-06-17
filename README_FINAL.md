# 🚀 银河麒麟智能问答助手

基于银河麒麟操作系统的RAG（检索增强生成）智能文档问答助手，集成麒麟AI SDK，支持多模态交互。

## ✨ 主要功能

- 📁 **文档管理**：支持PDF、TXT、MD等格式文档上传和处理
- 🤖 **智能问答**：基于文档内容的精准问答
- 🎤 **语音输入**：支持语音提问功能
- 🔊 **语音播报**：支持语音回答播报
- 🖥️ **系统信息**：显示银河麒麟系统详细信息
- 📋 **知识库管理**：可视化文档列表和状态管理

## 🛠️ 系统要求

- **操作系统**：银河麒麟 V10 或更高版本
- **Python版本**：Python 3.8+
- **内存**：建议4GB以上
- **存储空间**：至少1GB可用空间

## 📦 快速安装

### 1. 克隆项目
```bash
git clone <项目地址>
cd kylin-ai-assistant
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 创建图标（可选）
```bash
python3 create_icons.py
```

### 4. 运行系统测试
```bash
python3 test_system.py
```

### 5. 启动应用
```bash
# 使用启动脚本（推荐）
./start.sh

# 或直接运行
python3 main.py
```

## 🎯 使用指南

### 添加文档
1. 点击"📁 添加文档"按钮
2. 选择支持的文档格式（PDF、TXT、MD等）
3. 等待文档处理完成
4. 在"📋 知识库文档"中查看已添加的文档

### 智能问答
1. 在问题输入框中输入您的问题
2. 可选择"🎤 语音"进行语音输入
3. 点击"💬 提问"或按回车键
4. 查看基于文档内容的智能回答
5. 可选择"🔊 语音播报"听取回答

### 系统信息
- 点击"🖥️ 系统信息"查看麒麟系统详细信息
- 包含硬件配置、系统版本、网络状态等

## 🔧 配置说明

主要配置文件：`config.py`

```python
# API配置
SILICONFLOW_API_KEY = "your-api-key"  # 硅基流动API密钥
SILICONFLOW_API_ENDPOINT = "https://api.siliconflow.cn/v1/chat/completions"

# 向量数据库配置
VECTOR_CONFIG = {
    "similarity_threshold": 0.01,  # 相似度阈值
    "max_results": 10,             # 最大检索结果数
    "chunk_size": 500,             # 文档分块大小
}

# GUI配置
GUI_CONFIG = {
    "window_title": "银河麒麟智能问答助手",
    "window_size": "1200x800",
    "icon_path": "./assets/app_icon.png"
}
```

## 📁 项目结构

```
kylin-ai-assistant/
├── src/                    # 源代码目录
│   ├── gui.py             # GUI界面模块
│   ├── rag_engine.py      # RAG引擎核心
│   ├── vector_store.py    # 向量存储模块
│   ├── document_processor.py  # 文档处理模块
│   ├── ai_models.py       # AI模型接口
│   ├── voice_handler.py   # 语音处理模块
│   └── system_info_helper.py  # 系统信息助手
├── data/                  # 数据目录
│   └── vector_db/         # 向量数据库存储
├── logs/                  # 日志目录
├── assets/                # 资源文件
├── config.py              # 配置文件
├── main.py                # 主程序入口
├── requirements.txt       # 依赖列表
├── start.sh              # 启动脚本
└── README_FINAL.md       # 说明文档
```

## 🐛 故障排除

### 常见问题

1. **导入模块失败**
   ```bash
   pip install -r requirements.txt
   ```

2. **API连接失败**
   - 检查网络连接
   - 验证API密钥配置
   - 查看日志文件：`logs/app.log`

3. **语音功能不可用**
   ```bash
   sudo apt install pulseaudio pulseaudio-utils
   pip install SpeechRecognition pyttsx3
   ```

4. **文档处理失败**
   - 确保文档格式支持
   - 检查文件权限
   - 查看错误日志

### 系统测试
```bash
python3 test_system.py
```

### 查看日志
```bash
tail -f logs/app.log
```

## 🤝 技术支持

- **问题反馈**：请提交Issue描述问题
- **功能建议**：欢迎提出改进建议
- **技术交流**：可通过邮件联系开发团队

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🙏 致谢

- 银河麒麟操作系统团队
- 硅基流动AI平台
- 开源社区贡献者

---

**银河麒麟智能问答助手** - 让AI助力您的工作效率！🚀
