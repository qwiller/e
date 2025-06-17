#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证文件完整性
"""

import os
from pathlib import Path

def verify_files():
    """
    验证所有必要文件是否存在
    """
    print("🔍 验证文件完整性")
    print("=" * 40)
    
    required_files = [
        "main.py",
        "config.py", 
        "requirements.txt",
        "start.sh",
        "test_system.py",
        "src/gui.py",
        "src/rag_engine.py",
        "src/vector_store.py",
        "src/document_processor.py",
        "src/ai_models.py",
        "src/voice_handler.py",
        "src/system_info_helper.py"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} 字节)")
            existing_files.append(file_path)
        else:
            print(f"❌ {file_path} - 缺失")
            missing_files.append(file_path)
    
    print(f"\n📊 统计:")
    print(f"存在文件: {len(existing_files)}")
    print(f"缺失文件: {len(missing_files)}")
    
    if missing_files:
        print(f"\n❌ 缺失的文件:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print(f"\n✅ 所有必要文件都存在！")
        return True

def check_directories():
    """
    检查目录结构
    """
    print("\n📁 检查目录结构")
    print("=" * 40)
    
    required_dirs = [
        "src",
        "data",
        "data/vector_db",
        "logs",
        "assets"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"⚠️  {dir_path}/ - 不存在，将自动创建")
            os.makedirs(dir_path, exist_ok=True)

def main():
    """
    主函数
    """
    print("🧪 银河麒麟智能问答助手 - 文件验证")
    print("=" * 50)
    
    # 验证文件
    files_ok = verify_files()
    
    # 检查目录
    check_directories()
    
    if files_ok:
        print("\n🎉 验证通过！系统可以启动。")
        print("\n🚀 启动命令:")
        print("  python3 main.py")
        print("  或")
        print("  ./start.sh")
    else:
        print("\n❌ 验证失败！请检查缺失的文件。")
    
    return files_ok

if __name__ == "__main__":
    main()
