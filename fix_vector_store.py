#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复向量存储问题的脚本
"""

import os
import sys
import shutil

def fix_vector_store_path():
    """
    修复向量存储路径问题
    """
    print("🔧 修复向量存储路径问题")
    print("=" * 40)
    
    # 检查当前配置
    try:
        from config import VECTOR_DB_PATH
        print(f"当前向量数据库路径: {VECTOR_DB_PATH}")
    except ImportError:
        print("❌ 无法导入配置文件")
        return False
    
    # 检查路径是否为目录
    if os.path.exists(VECTOR_DB_PATH) and os.path.isdir(VECTOR_DB_PATH):
        print("⚠️  检测到向量数据库路径是目录，需要修复")
        
        # 备份目录
        backup_path = VECTOR_DB_PATH + "_backup"
        if os.path.exists(backup_path):
            shutil.rmtree(backup_path)
        
        shutil.move(VECTOR_DB_PATH, backup_path)
        print(f"✅ 已备份原目录到: {backup_path}")
    
    # 确保父目录存在
    parent_dir = os.path.dirname(VECTOR_DB_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
        print(f"✅ 创建父目录: {parent_dir}")
    
    print("✅ 向量存储路径修复完成")
    return True

def clean_vector_store():
    """
    清理向量存储
    """
    print("\n🧹 清理向量存储")
    print("=" * 40)
    
    try:
        from config import VECTOR_DB_PATH
        
        if os.path.exists(VECTOR_DB_PATH):
            if os.path.isfile(VECTOR_DB_PATH):
                os.remove(VECTOR_DB_PATH)
                print(f"✅ 删除向量存储文件: {VECTOR_DB_PATH}")
            elif os.path.isdir(VECTOR_DB_PATH):
                shutil.rmtree(VECTOR_DB_PATH)
                print(f"✅ 删除向量存储目录: {VECTOR_DB_PATH}")
        
        # 重新创建正确的目录结构
        parent_dir = os.path.dirname(VECTOR_DB_PATH)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
            print(f"✅ 重新创建目录: {parent_dir}")
        
    except Exception as e:
        print(f"❌ 清理失败: {e}")
        return False
    
    print("✅ 向量存储清理完成")
    return True

def test_vector_store_fix():
    """
    测试修复后的向量存储
    """
    print("\n🧪 测试修复后的向量存储")
    print("=" * 40)
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from src.vector_store import VectorStore
        
        # 创建向量存储实例
        vector_store = VectorStore()
        print("✅ 向量存储实例创建成功")
        
        # 添加测试文档
        test_docs = [
            {
                'content': '这是一个测试文档，用于验证向量存储功能。',
                'source': 'test.txt',
                'metadata': {'type': 'test'}
            }
        ]
        
        vector_store.add_documents(test_docs)
        print("✅ 测试文档添加成功")
        
        # 测试搜索
        results = vector_store.search("测试文档", top_k=1)
        if results:
            print(f"✅ 搜索测试成功，找到 {len(results)} 个结果")
        else:
            print("⚠️  搜索测试返回空结果")
        
        # 测试保存
        vector_store.save()
        print("✅ 保存测试成功")
        
        # 清理测试数据
        vector_store.clear()
        print("✅ 清理测试成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """
    主函数
    """
    print("🔧 向量存储修复工具")
    print("=" * 50)
    
    print("选择操作:")
    print("1. 修复向量存储路径")
    print("2. 清理向量存储")
    print("3. 测试向量存储")
    print("4. 全部执行")
    
    try:
        choice = input("请选择 (1/2/3/4): ").strip()
        
        if choice == "1":
            fix_vector_store_path()
        elif choice == "2":
            clean_vector_store()
        elif choice == "3":
            test_vector_store_fix()
        elif choice == "4":
            fix_vector_store_path()
            clean_vector_store()
            test_vector_store_fix()
        else:
            print("无效选择，执行全部操作")
            fix_vector_store_path()
            clean_vector_store()
            test_vector_store_fix()
        
        print("\n🎉 操作完成！")
        
    except KeyboardInterrupt:
        print("\n👋 操作中断")
    except Exception as e:
        print(f"❌ 操作失败: {e}")

if __name__ == "__main__":
    main()
