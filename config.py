# -*- coding: utf-8 -*-
"""
银河麒麟智能问答助手配置文件 - 基于硅基流动API和麒麟SDK2.5
"""

import os
import platform

# 应用版本信息
APP_VERSION = "2.6.1"
APP_NAME = "银河麒麟智能问答助手"
APP_DESCRIPTION = "基于硅基流动API和麒麟SDK2.5的智能问答系统"

# 硅基流动 API 配置
SILICONFLOW_API_KEY = "sk-owsayozifrzvaxuxvyvywmyzcceokwatdbolevdnfnbwlurp"  # 调试用API密钥
SILICONFLOW_API_ENDPOINT = "https://api.siliconflow.cn/v1/chat/completions"

# 默认模型配置
DEFAULT_MODEL = "Qwen/Qwen2.5-72B-Instruct"

# API参数配置
API_PARAMETERS = {
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

# 文档路径配置
DOCUMENT_PATH = "./docs"
VECTOR_DB_PATH = "./data/vector_db/vectors.pkl"

# 检测系统架构
ARCH = platform.machine().lower()
if ARCH in ['aarch64', 'arm64']:
    LIB_ARCH = "aarch64-linux-gnu"
elif ARCH in ['x86_64', 'amd64']:
    LIB_ARCH = "x86_64-linux-gnu"
else:
    LIB_ARCH = "linux-gnu"

# 麒麟SDK2.5完整配置 - 基于开发指南要求
KYLIN_SDK_CONFIG = {
    "version": "2.5",
    "required_packages": [
        "libkysdk-base-dev",
        "libkysdk-system-dev",
        "libkysdk-desktop-dev",
        "libkysdk-security-dev",
        "libkysdk-coreai-vision-dev"
    ],
    "system_lib_path": f"/usr/lib/{LIB_ARCH}/libkysysinfo.so",
    "hardware_lib_path": f"/usr/lib/{LIB_ARCH}/libkyhardware.so",
    "time_lib_path": f"/usr/lib/{LIB_ARCH}/libkydate.so",
    "package_lib_path": f"/usr/lib/{LIB_ARCH}/libkypackage.so",
    "ai_lib_path": f"/usr/lib/{LIB_ARCH}/libkycoreai.so",
    "security_lib_path": f"/usr/lib/{LIB_ARCH}/libkysecurity.so",
    "fallback_paths": [
        "/usr/lib/libkysysinfo.so",
        "/usr/local/lib/libkysysinfo.so",
        "./lib/libkysysinfo.so"
    ],
    "auto_install": True,  # 启用自动安装
    "install_source": "http://archive.kylinos.cn/kylin/KYLIN-ALL"
}

# 支持的文档类型（基于SDK2.5文档格式）
SUPPORTED_DOC_TYPES = {
    '.pdf': 'PDF文档',
    '.md': 'Markdown文档',
    '.txt': '文本文档',
    '.rst': 'reStructuredText文档',
    '.doc': 'Word文档',
    '.docx': 'Word文档',
    '.html': 'HTML文档',
    '.htm': 'HTML文档'
}

# 语音配置
VOICE_CONFIG = {
    "recognition_language": "zh-CN",
    "speech_rate": 150,
    "speech_volume": 0.8,
    "timeout": 5,
    "phrase_timeout": 1
}

# GUI配置
GUI_CONFIG = {
    "window_title": f"银河麒麟智能问答助手 v{APP_VERSION}",
    "window_size": "1200x800",
    "theme": "default",
    "font_family": "SimHei",
    "font_size": 12,
    "icon_path": "./assets/app_icon.png"
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "file": "./logs/app.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# 向量数据库配置 - 优化为轻量级方案
VECTOR_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "embedding_model": "tfidf",  # 使用TF-IDF替代OpenAI嵌入
    "similarity_threshold": 0.01,  # 进一步降低阈值以提高召回率
    "max_results": 10,
    "max_features": 5000,  # TF-IDF特征数量
    "ngram_range": [1, 2]  # N-gram范围
}

# RAG配置
RAG_CONFIG = {
    "top_k": 5,
    "similarity_threshold": 0.7,
    "max_context_length": 2000,
    "temperature": 0.7,
    "max_tokens": 1000
}

# 系统配置
SYSTEM_CONFIG = {
    "max_file_size": 50 * 1024 * 1024,  # 50MB
    "supported_languages": ["zh-CN", "en-US"]
}

# 安全配置
SECURITY_CONFIG = {
    "api_timeout": 30,
    "max_retries": 3
}

# 性能配置
PERFORMANCE_CONFIG = {
    "max_concurrent_processes": 4,
    "cache_size": 100,
    "batch_size": 32
}

# 开发配置
DEV_CONFIG = {
    "debug": False,
    "log_api_calls": False
}

# API配置映射 - 扩展多个API提供商
API_CONFIGS = {
    "siliconflow": {
        "api_key": SILICONFLOW_API_KEY,
        "endpoint": SILICONFLOW_API_ENDPOINT,
        "models": [
            "Qwen/Qwen2.5-72B-Instruct",
            "Qwen/Qwen2.5-32B-Instruct",
            "Qwen/Qwen2.5-14B-Instruct",
            "deepseek-ai/DeepSeek-V3"
        ]
    },
    # 可以添加其他API提供商作为备选
    "backup_apis": {
        "openai_compatible": "https://api.openai.com/v1/chat/completions",
        "local_api": "http://localhost:8000/v1/chat/completions"  # 如果有本地API服务
    }
}

# 麒麟系统优化配置
KYLIN_OPTIMIZATION = {
    "use_hardware_acceleration": False,  # 禁用硬件加速
    "prefer_api_calls": True,  # 优先使用API调用
    "cache_responses": True,  # 启用响应缓存
    "max_cache_size": 1000,  # 最大缓存条目
    "api_timeout": 30,  # API超时时间
    "retry_attempts": 3  # 重试次数
}

# 麒麟SDK库路径配置
KYLIN_SDK_LIBS = {
    # 系统信息模块
    'system': 'libkysysinfo.so',
    'hardware': 'libkyhardware.so',
    'date': 'libkydate.so',
    'package': 'libkypackage.so',

    # 网络模块
    'network': 'libkynetwork.so',

    # 硬件设备模块
    'cpu': 'libkycpu.so',
    'bios': 'libkybios.so',
    'board': 'libkyboard.so',
    'usb': 'libkyusb.so',
    'bluetooth': 'libkybluetooth.so',
    'display': 'libkydisplay.so',
    'edid': 'libkyedid.so',
    'fan': 'libkyfan.so',

    # AI和安全模块
    'ai': 'libkyai.so',
    'security': 'libkysecurity.so',

    # 电源和系统管理
    'power': 'libkypower.so',
    'disk': 'libkydisk.so'
}

# SDK开发包列表
KYLIN_SDK_PACKAGES = [
    # 基础开发包
    'libkysdk-base-dev',
    'libkysdk-system-dev',
    'libkysdk-desktop-dev',
    'libkysdk-security-dev',

    # 系统能力包
    'libkysdk-system',
    'libkysdk-system-dbus',
    'libkysdk-system-python',

    # 具体功能包
    'libkysdk-systime-dev',
    'libkysdk-applications-dev',
    'libkysdk-diagnostics-dev',
    'libkysdk-net-dev',
    'libkysdk-hw-dev',
    'libkysdk-res-dev',
    'libkysdk-print-dev',

    # D-Bus相关
    'libdbus-1-dev',
    'libdbus-glib-1-dev',
    'python3-dbus'
]

# D-Bus服务配置
DBUS_SERVICES = {
    'time_server': {
        'service': 'com.kylin.kysdk.TimeServer',
        'path': '/com/kylin/kysdk/Timer',
        'interface': 'com.kylin.kysdk.TimeInterface'
    },
    'date_server': {
        'service': 'com.kylin.kysdk.DateServer',
        'path': '/com/kylin/kysdk/Date',
        'interface': 'com.kylin.kysdk.DateInterface'
    }
}

# 工具函数
def get_config(key, default=None):
    """获取配置值"""
    return globals().get(key, default)

def validate_config():
    """验证配置"""
    issues = []

    if not SILICONFLOW_API_KEY or SILICONFLOW_API_KEY == "YOUR_API_KEY_HERE":
        issues.append("硅基流动API密钥未配置")

    if not os.path.exists(DOCUMENT_PATH):
        issues.append(f"文档路径不存在: {DOCUMENT_PATH}")

    return issues
























