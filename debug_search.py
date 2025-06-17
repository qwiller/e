#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试向量搜索功能
"""

import sys
import os
import logging

# 设置详细日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def debug_vector_search():
    """
    调试向量搜索功能
    """
    print("🔍 调试向量搜索功能")
    print("=" * 50)
    
    try:
        from src.vector_store import VectorStore
        from config import VECTOR_CONFIG
        
        # 创建向量存储实例
        print("1. 创建向量存储实例...")
        vector_store = VectorStore()
        
        # 显示当前状态
        stats = vector_store.get_stats()
        print(f"   数据库路径: {stats['db_path']}")
        print(f"   文档数量: {stats['document_count']}")
        print(f"   是否已训练: {stats['is_fitted']}")
        print(f"   向量形状: {stats['vector_shape']}")
        
        # 如果没有文档，添加测试文档
        if stats['document_count'] == 0:
            print("\n2. 添加测试文档...")
            test_docs = [
                {
                    'content': '天津商务职业学院在第十五届全国职业院校技能大赛中获得优异成绩，荣获多项奖项。学院在计算机应用技术、电子商务、会计等专业领域表现突出。',
                    'source': 'test_award.txt',
                    'metadata': {'type': 'award', 'school': '天津商务职业学院'}
                },
                {
                    'content': '第十五届全国职业院校技能大赛获奖名单公布，天津商务职业学院学生在多个项目中获得一等奖、二等奖和三等奖。',
                    'source': 'award_list.txt',
                    'metadata': {'type': 'competition', 'event': '第十五届大赛'}
                }
            ]
            
            vector_store.add_documents(test_docs)
            stats = vector_store.get_stats()
            print(f"   添加后文档数量: {stats['document_count']}")
        
        # 显示所有文档内容
        print("\n3. 当前存储的文档:")
        for i, doc in enumerate(vector_store.documents):
            print(f"   文档 {i}: {doc.get('content', '')[:100]}...")
        
        # 测试不同的查询
        print("\n4. 测试查询功能:")
        test_queries = [
            "天津商务职业学院获奖情况",
            "第十五届大赛",
            "职业院校技能大赛",
            "获奖名单",
            "天津商务",
            "计算机应用"
        ]
        
        print(f"当前配置: 相似度阈值={VECTOR_CONFIG.get('similarity_threshold', 0.1)}")
        
        for query in test_queries:
            print(f"\n   查询: '{query}'")
            
            # 使用调试模式搜索
            results = vector_store.search(query, top_k=5)
            
            print(f"   结果数量: {len(results)}")
            for j, result in enumerate(results):
                similarity = result.get('similarity', 0)
                content = result.get('content', '')[:80]
                print(f"     [{j+1}] 相似度: {similarity:.4f} - {content}...")
        
        # 测试不同阈值
        print("\n5. 测试不同相似度阈值:")
        test_query = "天津商务职业学院获奖情况"
        
        original_threshold = VECTOR_CONFIG['similarity_threshold']
        
        for threshold in [0.0, 0.05, 0.1, 0.2, 0.3]:
            VECTOR_CONFIG['similarity_threshold'] = threshold
            results = vector_store.search(test_query, top_k=3)
            print(f"   阈值 {threshold}: {len(results)} 个结果")
            
            for result in results:
                print(f"     相似度: {result.get('similarity', 0):.4f}")
        
        # 恢复原始阈值
        VECTOR_CONFIG['similarity_threshold'] = original_threshold
        
        print("\n6. 检查向量化器:")
        if hasattr(vector_store.vectorizer, 'vocabulary_'):
            vocab_size = len(vector_store.vectorizer.vocabulary_)
            print(f"   词汇表大小: {vocab_size}")
            
            # 显示一些词汇
            vocab_items = list(vector_store.vectorizer.vocabulary_.items())[:10]
            print(f"   词汇示例: {vocab_items}")
        
        # 测试查询向量化
        print("\n7. 测试查询向量化:")
        test_query = "天津商务职业学院"
        query_vector = vector_store.vectorizer.transform([test_query])
        print(f"   查询: '{test_query}'")
        print(f"   向量形状: {query_vector.shape}")
        print(f"   非零元素: {query_vector.nnz}")
        
        return True
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_jieba_tokenization():
    """
    测试jieba分词功能
    """
    print("\n🔤 测试jieba分词功能")
    print("=" * 50)
    
    try:
        import jieba
        
        test_texts = [
            "天津商务职业学院获奖情况",
            "第十五届全国职业院校技能大赛",
            "计算机应用技术专业"
        ]
        
        for text in test_texts:
            tokens = list(jieba.cut(text))
            print(f"原文: {text}")
            print(f"分词: {tokens}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ jieba测试失败: {e}")
        return False

def main():
    """
    主函数
    """
    print("🔍 向量搜索调试工具")
    print("=" * 50)
    
    try:
        # 测试jieba分词
        test_jieba_tokenization()
        
        # 调试向量搜索
        debug_vector_search()
        
        print("\n🎉 调试完成！")
        
    except KeyboardInterrupt:
        print("\n👋 调试中断")
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
