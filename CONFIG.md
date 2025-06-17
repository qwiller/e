# 🔧 配置文件说明

## 📋 配置文件概述

项目包含以下配置文件：

### 1. **`config.py`** - 主配置文件
- 包含所有系统配置参数
- API密钥和端点配置
- 向量数据库配置
- 语音功能配置
- 麒麟SDK配置

### 2. **`config_template.py`** - 配置模板文件
- 配置文件的模板版本
- 包含默认配置和注释说明
- 用于快速创建新的配置文件

## 🔑 API密钥配置

### 获取硅基流动API密钥
1. 访问 https://cloud.siliconflow.cn
2. 注册并登录账户
3. 在控制台中创建API密钥
4. 复制密钥到配置文件中

### 配置方法
```python
# 在 config.py 中设置
SILICONFLOW_API_KEY = "your_api_key_here"
```

## ⚙️ 主要配置项

### API配置
```python
SILICONFLOW_API_KEY = "your_api_key_here"
SILICONFLOW_API_ENDPOINT = "https://api.siliconflow.cn/v1/chat/completions"
DEFAULT_MODEL = "Qwen/Qwen2.5-72B-Instruct"
```

### 向量数据库配置
```python
VECTOR_CONFIG = {
    "chunk_size": 500,        # 文档分块大小
    "chunk_overlap": 50,      # 分块重叠大小
    "similarity_threshold": 0.1,  # 相似度阈值
    "max_results": 10         # 最大检索结果数
}
```

### 语音配置
```python
VOICE_CONFIG = {
    "recognition_language": "zh-CN",  # 识别语言
    "speech_rate": 150,              # 语音速度
    "speech_volume": 0.8             # 音量
}
```

### RAG配置
```python
RAG_CONFIG = {
    "top_k": 5,                    # 检索结果数量
    "similarity_threshold": 0.7,    # 相似度阈值
    "max_context_length": 2000,     # 最大上下文长度
    "temperature": 0.7,             # 生成温度
    "max_tokens": 1000              # 最大生成token数
}
```

## 🔒 安全建议

1. **不要提交API密钥到版本控制**
2. **使用环境变量管理敏感信息**
3. **定期更换API密钥**
4. **限制API密钥权限**

## 🛠️ 配置文件管理

### 创建本地配置
```bash
# 复制模板文件
cp config_template.py config.py

# 编辑配置
vim config.py
```

### 环境变量配置
```bash
# 在 ~/.bashrc 中添加
export SILICONFLOW_API_KEY="your_api_key_here"

# 重新加载
source ~/.bashrc
```

## ❓ 常见问题

**Q: 配置文件丢失怎么办？**
A: 使用 `config_template.py` 作为模板重新创建

**Q: API密钥无效怎么办？**
A: 检查密钥是否正确，是否有足够的配额

**Q: 如何备份配置？**
A: 复制 `config.py` 到安全位置，注意保护API密钥
