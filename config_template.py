# -*- coding: utf-8 -*-
"""
配置文件模板
"""

# API配置
API_KEY = ""  # 请在此处填写您的硅基流动API密钥
API_ENDPOINT = "https://api.siliconflow.com/v1/chat/completions"

# 默认模型配置
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"  # 默认使用的模型
AVAILABLE_MODELS = [
    "deepseek-ai/DeepSeek-V3",
    "deepseek-ai/DeepSeek-Coder-Base-1.3B",
    "deepseek-ai/DeepSeek-Coder-Base-6.7B"
]

# API参数配置
DEFAULT_PARAMETERS = {
    "temperature": 0.7,        # 随机性控制（0.0-1.0）
    "max_tokens": 4096,        # 最大输出长度
    "top_p": 0.9,             # 采样概率
    "frequency_penalty": 0.0,  # 频率惩罚
    "presence_penalty": 0.0    # 新颖性惩罚
}

# 重试机制配置
RETRY_SETTINGS = {
    "max_retries": 3,         # 最大重试次数
    "retry_delay": 3,         # 重试间隔（秒）
    "timeout": 30             # 请求超时时间（秒）
}

# 系统配置
SYSTEM_SETTINGS = {
    "log_level": "INFO",       # 日志级别
    "cache_enabled": True,     # 是否启用缓存
    "cache_size": 100,         # 缓存大小
    "max_concurrent_requests": 5  # 最大并发请求
}

# 安全配置
SECURITY_SETTINGS = {
    "api_key_env_var": "SILICONFLOW_API_KEY",  # API密钥环境变量名
    "encrypt_config": True,                    # 是否加密配置文件
    "config_file": "config_encrypted.json"     # 加密配置文件名
}

# 测试配置
TEST_SETTINGS = {
    "test_cases": [
        {
            "name": "简单问候测试",
            "messages": [
                {"role": "user", "content": "你好，我是银河麒麟系统的用户"}
            ]
        },
        {
            "name": "详细问题测试",
            "messages": [
                {"role": "user", "content": "请详细介绍一下银河麒麟操作系统的主要特点和优势"}
            ]
        },
        {
            "name": "多轮对话测试",
            "messages": [
                {"role": "user", "content": "我最近在使用银河麒麟系统，遇到了一些问题"},
                {"role": "assistant", "content": "请告诉我具体遇到了什么问题，我会尽力帮你解决"},
                {"role": "user", "content": "软件安装时提示缺少某些依赖包，怎么解决？"}
            ]
        }
    ]
}
