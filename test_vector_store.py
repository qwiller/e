#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量存储测试脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.vector_store import VectorStore
from config import VECTOR_DB_PATH

def test_vector_store():
    """
    测试向量存储功能
    """
    print("🧪 向量存储功能测试")
    print("=" * 50)
    
    # 创建向量存储实例
    print("1. 创建向量存储实例...")
    vector_store = VectorStore()
    
    # 显示当前状态
    stats = vector_store.get_stats()
    print(f"   数据库路径: {stats['db_path']}")
    print(f"   文档数量: {stats['document_count']}")
    print(f"   是否已训练: {stats['is_fitted']}")
    
    # 添加测试文档
    print("\n2. 添加测试文档...")
    test_docs = [
        {
            'content': '天津商务职业学院是一所优秀的高等职业院校，在各类比赛中获得了多项荣誉。',
            'source': 'test_doc_1.txt',
            'metadata': {'type': 'test'}
        },
        {
            'content': '该学院在第十五届全国职业院校技能大赛中表现突出，获得了多个奖项。',
            'source': 'test_doc_2.txt', 
            'metadata': {'type': 'test'}
        },
        {
            'content': '学院的学生在计算机应用、商务管理等专业领域都有优异表现。',
            'source': 'test_doc_3.txt',
            'metadata': {'type': 'test'}
        }
    ]
    
    try:
        vector_store.add_documents(test_docs)
        print("   ✅ 测试文档添加成功")
    except Exception as e:
        print(f"   ❌ 测试文档添加失败: {e}")
        return False
    
    # 显示更新后的状态
    stats = vector_store.get_stats()
    print(f"   更新后文档数量: {stats['document_count']}")
    print(f"   向量形状: {stats['vector_shape']}")
    
    # 测试搜索功能
    print("\n3. 测试搜索功能...")
    test_queries = [
        "天津商务职业学院获奖情况",
        "第十五届大赛",
        "计算机应用专业",
        "职业院校技能大赛"
    ]
    
    for query in test_queries:
        print(f"\n   查询: {query}")
        results = vector_store.search(query, top_k=3)
        print(f"   结果数量: {len(results)}")
        
        for i, result in enumerate(results):
            print(f"   [{i+1}] 相似度: {result.get('similarity', 0):.3f}")
            print(f"       内容: {result['content'][:50]}...")
    
    # 测试保存和加载
    print("\n4. 测试保存和加载...")
    try:
        vector_store.save()
        print("   ✅ 保存成功")
        
        # 创建新实例测试加载
        new_vector_store = VectorStore()
        new_stats = new_vector_store.get_stats()
        print(f"   加载后文档数量: {new_stats['document_count']}")
        
        if new_stats['document_count'] == stats['document_count']:
            print("   ✅ 加载成功")
        else:
            print("   ❌ 加载失败，文档数量不匹配")
            
    except Exception as e:
        print(f"   ❌ 保存/加载失败: {e}")
    
    # 清理测试数据
    print("\n5. 清理测试数据...")
    try:
        vector_store.clear()
        print("   ✅ 清理完成")
    except Exception as e:
        print(f"   ❌ 清理失败: {e}")
    
    print("\n🎉 向量存储测试完成！")
    return True

def test_similarity_threshold():
    """
    测试不同相似度阈值的效果
    """
    print("\n🔍 相似度阈值测试")
    print("=" * 50)
    
    vector_store = VectorStore()
    
    # 添加测试文档
    test_docs = [
        {
            'content': '天津商务职业学院在第十五届全国职业院校技能大赛中获得一等奖',
            'source': 'award_doc.txt',
            'metadata': {'type': 'award'}
        }
    ]
    
    vector_store.add_documents(test_docs)
    
    query = "天津商务职业学院获奖情况"
    
    # 测试不同阈值
    thresholds = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7]
    
    for threshold in thresholds:
        # 临时修改阈值
        from config import VECTOR_CONFIG
        original_threshold = VECTOR_CONFIG['similarity_threshold']
        VECTOR_CONFIG['similarity_threshold'] = threshold
        
        results = vector_store.search(query, top_k=5)
        
        print(f"阈值 {threshold}: {len(results)} 个结果")
        for result in results:
            print(f"  相似度: {result.get('similarity', 0):.3f}")
        
        # 恢复原始阈值
        VECTOR_CONFIG['similarity_threshold'] = original_threshold
    
    # 清理
    vector_store.clear()

if __name__ == "__main__":
    print("选择测试模式:")
    print("1. 基础功能测试")
    print("2. 相似度阈值测试")
    print("3. 全部测试")
    
    try:
        choice = input("请选择 (1/2/3): ").strip()
        
        if choice == "1":
            test_vector_store()
        elif choice == "2":
            test_similarity_threshold()
        elif choice == "3":
            test_vector_store()
            test_similarity_threshold()
        else:
            print("无效选择，执行基础功能测试")
            test_vector_store()
            
    except KeyboardInterrupt:
        print("\n👋 测试中断")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
