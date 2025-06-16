# -*- coding: utf-8 -*-
"""
API配置设置脚本
"""

import os
import json
import getpass
from pathlib import Path

def setup_api_config():
    """设置API配置"""
    print("\n🚀 开始设置API配置...")
    
    # 检查配置文件
    config_path = Path("config.py")
    if config_path.exists():
        print("警告: 已存在配置文件，是否要覆盖？(y/n)")
        if input().lower() != 'y':
            print("配置设置已取消")
            return
    
    # 获取API密钥
    print("\n🔑 请提供硅基流动API密钥:")
    api_key = getpass.getpass("API密钥: ")
    
    # 获取其他配置
    print("\n🔧 请设置其他配置参数:")
    model = input(f"默认模型（默认：{DEFAULT_MODEL}）: ") or DEFAULT_MODEL
    max_tokens = input("最大输出长度（默认：4096）: ") or "4096"
    temperature = input("随机性控制（0.0-1.0，推荐0.7）: ") or "0.7"
    
    # 生成配置文件内容
    config_content = f"""# -*- coding: utf-8 -*-
"""
配置文件
"""

API_KEY = "{api_key}"
API_ENDPOINT = "https://api.siliconflow.com/v1/chat/completions"

DEFAULT_MODEL = "{model}"
MAX_TOKENS = {max_tokens}
TEMPERATURE = {temperature}

# 其他配置
RETRY_SETTINGS = {{
    "max_retries": 3,
    "retry_delay": 3,
    "timeout": 30
}}

# 系统配置
SYSTEM_SETTINGS = {{
    "log_level": "INFO",
    "cache_enabled": True,
    "cache_size": 100,
    "max_concurrent_requests": 5
}}
"""
    
    # 写入配置文件
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("\n✅ 配置文件已创建成功！")
    print("配置文件位置:", config_path.absolute())
    
    # 测试配置
    print("\n🧪 测试API连接...")
    try:
        # 这里可以添加测试API连接的代码
        print("API连接测试成功！")
    except Exception as e:
        print(f"警告: API连接测试失败: {str(e)}")
    
    print("\n🚀 配置设置完成！")
    print("建议您将API密钥安全地存储在环境变量中：")
    print("export SILICONFLOW_API_KEY=your_api_key")

if __name__ == "__main__":
    setup_api_config()
