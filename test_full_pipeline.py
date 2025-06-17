#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整的RAG流程
"""

import sys
import os
import logging

# 设置详细日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_full_pipeline():
    """
    测试完整的RAG流程
    """
    print("🧪 测试完整的RAG流程")
    print("=" * 50)
    
    try:
        from src.rag_engine import RAGEngine
        
        # 创建RAG引擎
        print("1. 创建RAG引擎...")
        rag_engine = RAGEngine()
        
        # 检查知识库状态
        stats = rag_engine.get_knowledge_base_stats()
        print(f"   知识库状态: {stats['document_count']} 个文档")
        
        # 如果知识库为空，添加测试文档
        if stats['document_count'] == 0:
            print("\n2. 添加测试文档...")
            
            # 模拟文档内容
            test_content = """
天津商务职业学院在第十五届全国职业院校技能大赛中取得优异成绩。

获奖情况如下：
- 计算机应用技术专业：一等奖2项，二等奖3项
- 电子商务专业：一等奖1项，二等奖2项，三等奖1项  
- 会计专业：二等奖2项，三等奖3项
- 物流管理专业：一等奖1项，三等奖2项

本次大赛共有来自全国各地的500多所职业院校参加，天津商务职业学院的学生们凭借扎实的专业技能和良好的心理素质，在激烈的竞争中脱颖而出。

学院领导表示，这些成绩的取得离不开全体师生的共同努力，也体现了学院在职业教育方面的实力和水平。
            """.strip()
            
            # 创建临时文件
            temp_file = "temp_test_doc.txt"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            try:
                # 添加文档到知识库
                result = rag_engine.add_document(temp_file)
                print(f"   添加结果: {result}")
                
                # 检查更新后的状态
                stats = rag_engine.get_knowledge_base_stats()
                print(f"   更新后文档数量: {stats['document_count']}")
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        
        # 测试查询
        print("\n3. 测试查询功能...")
        test_queries = [
            "天津商务职业学院获奖情况",
            "第十五届大赛成绩",
            "计算机应用技术专业获奖",
            "电子商务专业表现如何",
            "学院在比赛中的表现"
        ]
        
        for query in test_queries:
            print(f"\n   查询: {query}")
            
            # 执行查询
            result = rag_engine.generate_answer(query, include_system_info=False)
            
            print(f"   相关文档数量: {len(result.get('relevant_docs', []))}")
            print(f"   上下文长度: {result.get('context_length', 0)}")
            
            # 显示回答
            answer = result.get('answer', '')
            if len(answer) > 200:
                print(f"   回答: {answer[:200]}...")
            else:
                print(f"   回答: {answer}")
            
            # 显示相关文档
            for i, doc in enumerate(result.get('relevant_docs', [])):
                similarity = doc.get('similarity', 0)
                content = doc.get('content', '')[:100]
                print(f"     文档{i+1} (相似度: {similarity:.4f}): {content}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vector_search_directly():
    """
    直接测试向量搜索
    """
    print("\n🔍 直接测试向量搜索")
    print("=" * 50)
    
    try:
        from src.vector_store import VectorStore
        
        # 创建向量存储
        vector_store = VectorStore()
        
        # 检查状态
        stats = vector_store.get_stats()
        print(f"文档数量: {stats['document_count']}")
        
        if stats['document_count'] == 0:
            print("添加测试文档...")
            test_docs = [
                {
                    'content': '天津商务职业学院在第十五届全国职业院校技能大赛中获得多项奖项，包括计算机应用技术一等奖。',
                    'source': 'test.txt',
                    'metadata': {}
                }
            ]
            vector_store.add_documents(test_docs)
        
        # 测试搜索
        query = "天津商务职业学院获奖情况"
        print(f"搜索查询: {query}")
        
        results = vector_store.search(query, top_k=5)
        print(f"搜索结果: {len(results)} 个")
        
        for i, result in enumerate(results):
            print(f"  结果{i+1}: 相似度 {result.get('similarity', 0):.4f}")
            print(f"    内容: {result.get('content', '')[:100]}...")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"❌ 向量搜索测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """
    主函数
    """
    print("🧪 RAG系统完整测试")
    print("=" * 50)
    
    try:
        # 测试向量搜索
        search_ok = test_vector_search_directly()
        
        if search_ok:
            print("✅ 向量搜索测试通过")
            
            # 测试完整流程
            pipeline_ok = test_full_pipeline()
            
            if pipeline_ok:
                print("\n🎉 所有测试通过！")
            else:
                print("\n❌ 完整流程测试失败")
        else:
            print("❌ 向量搜索测试失败，跳过完整流程测试")
        
    except KeyboardInterrupt:
        print("\n👋 测试中断")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    main()
