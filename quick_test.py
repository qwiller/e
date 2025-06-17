#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速功能测试脚本
"""

import sys
import os

def test_imports():
    """
    测试模块导入
    """
    print("📦 测试模块导入...")
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from src.rag_engine import RAGEngine
        from src.voice_handler import VoiceHandler
        from src.ai_models import SiliconFlowAPI
        from src.vector_store import VectorStore
        from src.document_processor import DocumentProcessor
        
        print("✅ 所有核心模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_api_connection():
    """
    测试API连接
    """
    print("🌐 测试API连接...")
    
    try:
        from src.ai_models import SiliconFlowAPI
        
        api = SiliconFlowAPI()
        if api.test_connection():
            print("✅ API连接成功")
            return True
        else:
            print("❌ API连接失败")
            return False
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def test_voice_basic():
    """
    测试语音基础功能
    """
    print("🎤 测试语音基础功能...")
    
    try:
        from src.voice_handler import VoiceHandler
        
        voice = VoiceHandler()
        if voice.is_available:
            print("✅ 语音功能可用")
            
            # 获取语音信息
            info = voice.get_voice_info()
            print(f"   音量: {info.get('volume', 'N/A')}")
            print(f"   速度: {info.get('rate', 'N/A')}")
            
            return True
        else:
            print("❌ 语音功能不可用")
            return False
    except Exception as e:
        print(f"❌ 语音测试失败: {e}")
        return False

def test_vector_store():
    """
    测试向量存储
    """
    print("🗄️  测试向量存储...")
    
    try:
        from src.vector_store import VectorStore
        
        vs = VectorStore()
        
        # 添加测试文档
        test_docs = [{
            'content': '这是一个测试文档，用于验证向量存储功能。',
            'source': 'test.txt',
            'metadata': {}
        }]
        
        vs.add_documents(test_docs)
        
        # 测试搜索
        results = vs.search("测试文档", top_k=1)
        
        if results:
            print(f"✅ 向量存储测试成功，相似度: {results[0].get('similarity', 0):.4f}")
            return True
        else:
            print("❌ 向量存储搜索无结果")
            return False
            
    except Exception as e:
        print(f"❌ 向量存储测试失败: {e}")
        return False

def test_rag_simple():
    """
    测试RAG简单功能
    """
    print("🧠 测试RAG简单功能...")
    
    try:
        from src.rag_engine import RAGEngine
        
        rag = RAGEngine()
        
        # 获取知识库状态
        stats = rag.get_knowledge_base_stats()
        doc_count = stats.get('document_count', 0)
        
        print(f"✅ RAG引擎初始化成功，知识库文档数: {doc_count}")
        return True
        
    except Exception as e:
        print(f"❌ RAG测试失败: {e}")
        return False

def test_gui_components():
    """
    测试GUI组件
    """
    print("🖼️  测试GUI组件...")
    
    try:
        import tkinter as tk
        
        # 创建测试窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 测试基本组件
        label = tk.Label(root, text="测试")
        button = tk.Button(root, text="测试")
        
        print("✅ GUI组件测试成功")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ GUI测试失败: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("🧪 银河麒麟智能问答助手 - 快速功能测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("API连接", test_api_connection),
        ("语音功能", test_voice_basic),
        ("向量存储", test_vector_store),
        ("RAG引擎", test_rag_simple),
        ("GUI组件", test_gui_components)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results[test_name] = False
        print()
    
    # 显示结果
    print("📊 测试结果总结:")
    print("-" * 30)
    
    success_count = 0
    for test_name, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
        if success:
            success_count += 1
    
    total_tests = len(results)
    print(f"\n🎯 总体结果: {success_count}/{total_tests} 项测试通过")
    
    if success_count == total_tests:
        print("\n🎉 所有测试通过！系统可以正常运行。")
    elif success_count >= total_tests * 0.8:
        print("\n⚠️  大部分测试通过，系统基本可用。")
    else:
        print("\n❌ 多项测试失败，建议运行修复脚本。")
        print("修复命令: python3 fix_all_issues.py")
    
    return success_count == total_tests

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 测试中断")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
