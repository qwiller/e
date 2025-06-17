#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试文档状态的专用脚本
"""

import sys
import os
import logging

# 设置详细日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def debug_vector_store():
    """
    调试向量存储状态
    """
    print("🗄️  调试向量存储状态")
    print("=" * 40)
    
    try:
        from src.vector_store import VectorStore
        
        vs = VectorStore()
        stats = vs.get_stats()
        
        print(f"文档数量: {stats.get('document_count', 0)}")
        print(f"是否已训练: {stats.get('is_fitted', False)}")
        print(f"数据库路径: {stats.get('db_path', 'N/A')}")
        print(f"向量形状: {stats.get('vector_shape', 'N/A')}")
        
        # 显示文档详情
        if hasattr(vs, 'documents') and vs.documents:
            print(f"\n📋 文档详情:")
            for i, doc in enumerate(vs.documents):
                print(f"  文档 {i+1}:")
                print(f"    来源: {doc.get('source', '未知')}")
                print(f"    内容长度: {len(doc.get('content', ''))}")
                print(f"    内容预览: {doc.get('content', '')[:100]}...")
                print(f"    元数据: {doc.get('metadata', {})}")
                print()
        else:
            print("⚠️  向量存储中没有文档")
        
        return True
        
    except Exception as e:
        print(f"❌ 向量存储调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_rag_engine():
    """
    调试RAG引擎状态
    """
    print("🧠 调试RAG引擎状态")
    print("=" * 40)
    
    try:
        from src.rag_engine import RAGEngine
        
        rag = RAGEngine()
        stats = rag.get_knowledge_base_stats()
        
        print(f"知识库统计:")
        for key, value in stats.items():
            if key == 'documents':
                print(f"  {key}: {len(value)} 个文档")
                for i, doc in enumerate(value):
                    print(f"    文档 {i+1}: {doc.get('source', '未知')}")
            else:
                print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG引擎调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_document_search():
    """
    测试文档搜索功能
    """
    print("🔍 测试文档搜索功能")
    print("=" * 40)
    
    try:
        from src.rag_engine import RAGEngine
        
        rag = RAGEngine()
        
        # 测试查询
        test_queries = [
            "这篇文档讲了什么",
            "文档内容",
            "获奖",
            "天津",
            "学院"
        ]
        
        for query in test_queries:
            print(f"\n查询: '{query}'")
            result = rag.generate_answer(query, include_system_info=False)
            
            relevant_docs = result.get('relevant_docs', [])
            answer = result.get('answer', '')
            
            print(f"  相关文档数: {len(relevant_docs)}")
            for i, doc in enumerate(relevant_docs):
                similarity = doc.get('similarity', 0)
                print(f"    文档 {i+1}: 相似度 {similarity:.4f}")
            
            print(f"  回答长度: {len(answer)}")
            print(f"  回答预览: {answer[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 文档搜索测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_file_system():
    """
    检查文件系统状态
    """
    print("📁 检查文件系统状态")
    print("=" * 40)
    
    # 检查向量存储文件
    vector_db_path = "./data/vector_db/vectors.pkl"
    if os.path.exists(vector_db_path):
        size = os.path.getsize(vector_db_path)
        print(f"✅ 向量存储文件存在: {vector_db_path} ({size} 字节)")
    else:
        print(f"❌ 向量存储文件不存在: {vector_db_path}")
    
    # 检查数据目录
    data_dir = "./data"
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        print(f"✅ 数据目录存在: {data_dir}")
        print(f"   内容: {files}")
        
        # 检查子目录
        vector_dir = os.path.join(data_dir, "vector_db")
        if os.path.exists(vector_dir):
            vector_files = os.listdir(vector_dir)
            print(f"   向量目录内容: {vector_files}")
    else:
        print(f"❌ 数据目录不存在: {data_dir}")
    
    # 检查日志目录
    log_dir = "./logs"
    if os.path.exists(log_dir):
        log_files = os.listdir(log_dir)
        print(f"✅ 日志目录存在: {log_dir}")
        print(f"   日志文件: {log_files}")
    else:
        print(f"❌ 日志目录不存在: {log_dir}")

def main():
    """
    主调试函数
    """
    print("🔍 文档状态调试工具")
    print("=" * 50)
    
    # 检查文件系统
    check_file_system()
    print()
    
    # 调试向量存储
    vs_ok = debug_vector_store()
    print()
    
    # 调试RAG引擎
    rag_ok = debug_rag_engine()
    print()
    
    # 测试搜索功能
    if vs_ok and rag_ok:
        search_ok = test_document_search()
    else:
        print("⚠️  跳过搜索测试，因为基础组件有问题")
        search_ok = False
    
    print("\n📊 调试结果总结:")
    print("-" * 30)
    print(f"向量存储: {'✅ 正常' if vs_ok else '❌ 异常'}")
    print(f"RAG引擎: {'✅ 正常' if rag_ok else '❌ 异常'}")
    print(f"搜索功能: {'✅ 正常' if search_ok else '❌ 异常'}")
    
    if vs_ok and rag_ok and search_ok:
        print("\n🎉 所有组件正常！")
    else:
        print("\n⚠️  发现问题，建议:")
        if not vs_ok:
            print("  - 重新添加文档到知识库")
        if not rag_ok:
            print("  - 检查RAG引擎配置")
        if not search_ok:
            print("  - 运行 python3 fix_search_issue.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 调试中断")
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()
