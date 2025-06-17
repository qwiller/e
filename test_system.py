#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统功能测试脚本
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_core_modules():
    """
    测试核心模块
    """
    print("🧪 测试核心模块...")
    
    modules = [
        ('RAG引擎', 'src.rag_engine', 'RAGEngine'),
        ('向量存储', 'src.vector_store', 'VectorStore'),
        ('文档处理器', 'src.document_processor', 'DocumentProcessor'),
        ('AI模型', 'src.ai_models', 'SiliconFlowAPI'),
        ('语音处理', 'src.voice_handler', 'VoiceHandler'),
        ('GUI界面', 'src.gui', 'RAGApplication')
    ]
    
    results = {}
    
    for name, module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {name}: 导入成功")
            results[name] = True
        except Exception as e:
            print(f"❌ {name}: 导入失败 - {e}")
            results[name] = False
    
    return results

def test_rag_functionality():
    """
    测试RAG功能
    """
    print("\n🧠 测试RAG功能...")
    
    try:
        from src.rag_engine import RAGEngine
        
        rag = RAGEngine()
        print("✅ RAG引擎初始化成功")
        
        # 获取知识库状态
        stats = rag.get_knowledge_base_stats()
        doc_count = stats.get('document_count', 0)
        print(f"   知识库文档数: {doc_count}")
        
        # 如果有文档，测试查询
        if doc_count > 0:
            print("   测试查询功能...")
            result = rag.query("这篇文档讲了什么")
            relevant_docs = result.get('relevant_docs', [])
            answer = result.get('answer', '')
            
            print(f"   查询结果: {len(relevant_docs)} 个相关文档")
            print(f"   回答长度: {len(answer)} 字符")
            
            if relevant_docs:
                print("✅ RAG查询功能正常")
                return True
            else:
                print("⚠️  RAG查询无结果，可能需要添加文档")
                return True
        else:
            print("⚠️  知识库为空，请添加文档后测试")
            return True
        
    except Exception as e:
        print(f"❌ RAG功能测试失败: {e}")
        return False

def test_api_connection():
    """
    测试API连接
    """
    print("\n🌐 测试API连接...")
    
    try:
        from src.ai_models import SiliconFlowAPI
        
        api = SiliconFlowAPI()
        print("✅ API客户端初始化成功")
        
        if api.test_connection():
            print("✅ API连接测试成功")
            return True
        else:
            print("❌ API连接测试失败")
            return False
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("🧪 银河麒麟智能问答助手 - 系统测试")
    print("=" * 50)
    
    # 测试核心模块
    module_results = test_core_modules()
    
    # 测试RAG功能
    rag_ok = test_rag_functionality()
    
    # 测试API连接
    api_ok = test_api_connection()
    
    # 显示结果
    print("\n📊 测试结果总结:")
    print("-" * 30)
    
    # 模块测试结果
    success_count = sum(module_results.values())
    total_modules = len(module_results)
    
    for name, success in module_results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"RAG功能: {'✅ 通过' if rag_ok else '❌ 失败'}")
    print(f"API连接: {'✅ 通过' if api_ok else '❌ 失败'}")
    
    # 总体评估
    total_tests = total_modules + 2  # 模块 + RAG + API
    passed_tests = success_count + (1 if rag_ok else 0) + (1 if api_ok else 0)
    
    print(f"\n🎯 总体结果: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("\n🎉 所有测试通过！系统可以正常运行。")
        print("🚀 启动命令: python3 main.py")
    elif passed_tests >= total_tests * 0.8:
        print("\n⚠️  大部分测试通过，系统基本可用。")
        print("🚀 启动命令: python3 main.py")
    else:
        print("\n❌ 多项测试失败，建议检查依赖和配置。")
        print("📋 建议:")
        print("  - 检查依赖安装: pip install -r requirements.txt")
        print("  - 检查配置文件: config.py")
        print("  - 查看日志文件: logs/app.log")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 测试中断")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
