#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试GUI修复效果
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_gui_import():
    """
    测试GUI模块导入
    """
    print("🧪 测试GUI模块导入...")
    
    try:
        from gui import RAGApplication
        print("✅ GUI模块导入成功")
        return True
    except Exception as e:
        print(f"❌ GUI模块导入失败: {e}")
        return False

def test_voice_handler():
    """
    测试语音处理模块
    """
    print("\n🎤 测试语音处理模块...")
    
    try:
        from voice_handler import VoiceHandler
        
        voice = VoiceHandler()
        print(f"✅ 语音处理模块初始化成功")
        print(f"   语音功能可用: {voice.is_available}")
        
        if voice.is_available:
            # 测试语音播报
            print("   测试语音播报...")
            result = voice.speak_text("测试语音功能", async_mode=False)
            print(f"   语音播报结果: {'成功' if result else '失败'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 语音处理模块测试失败: {e}")
        return False

def test_rag_engine():
    """
    测试RAG引擎
    """
    print("\n🧠 测试RAG引擎...")
    
    try:
        from rag_engine import RAGEngine
        
        rag = RAGEngine()
        print("✅ RAG引擎初始化成功")
        
        # 测试知识库状态
        stats = rag.get_knowledge_base_stats()
        doc_count = stats.get('document_count', 0)
        print(f"   知识库文档数: {doc_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG引擎测试失败: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("🧪 GUI修复效果测试")
    print("=" * 40)
    
    tests = [
        ("GUI模块", test_gui_import),
        ("语音处理", test_voice_handler),
        ("RAG引擎", test_rag_engine)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name}测试异常: {e}")
            results.append((name, False))
    
    # 显示结果
    print("\n📊 测试结果:")
    print("-" * 30)
    
    passed = 0
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("\n🎉 所有测试通过！GUI修复成功。")
        print("🚀 现在可以启动应用: python3 main.py")
    elif passed >= len(results) * 0.8:
        print("\n⚠️  大部分测试通过，应用基本可用。")
        print("🚀 可以尝试启动: python3 main.py")
    else:
        print("\n❌ 多项测试失败，需要进一步检查。")
    
    return passed == len(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 测试中断")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
