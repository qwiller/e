#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复文档显示问题的专用脚本
"""

import sys
import os

def fix_document_display():
    """
    修复文档显示问题
    """
    print("🔧 修复文档显示问题")
    print("=" * 40)
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from src.rag_engine import RAGEngine
        from src.vector_store import VectorStore
        
        # 1. 检查向量存储状态
        print("1. 检查向量存储状态...")
        vs = VectorStore()
        vs_stats = vs.get_stats()
        
        print(f"   向量存储文档数: {vs_stats.get('document_count', 0)}")
        
        if vs_stats.get('document_count', 0) == 0:
            print("   ⚠️  向量存储为空，添加测试文档...")
            
            # 添加测试文档
            test_docs = [{
                'content': '天津商务职业学院在第十五届全国职业院校技能大赛中获得优异成绩，荣获多项奖项。学院在计算机应用技术、电子商务、会计等专业领域表现突出。',
                'source': '第十五届大赛获奖名单.pdf',
                'metadata': {'type': 'award', 'school': '天津商务职业学院'}
            }]
            
            vs.add_documents(test_docs)
            print("   ✅ 测试文档添加完成")
        
        # 2. 检查RAG引擎状态
        print("\n2. 检查RAG引擎状态...")
        rag = RAGEngine()
        rag_stats = rag.get_knowledge_base_stats()
        
        print(f"   RAG引擎文档数: {rag_stats.get('document_count', 0)}")
        print(f"   文档详情: {len(rag_stats.get('documents', []))} 个")
        
        # 显示文档详情
        documents = rag_stats.get('documents', [])
        if documents:
            print("   📋 文档列表:")
            for i, doc in enumerate(documents):
                source = doc.get('source', '未知')
                content_len = doc.get('content_length', 0)
                print(f"     {i+1}. {source} ({content_len} 字符)")
        else:
            print("   ⚠️  RAG引擎中没有文档")
        
        # 3. 测试搜索功能
        print("\n3. 测试搜索功能...")
        test_query = "天津商务职业学院获奖情况"
        
        # 直接测试向量存储搜索
        vs_results = vs.search(test_query, top_k=3)
        print(f"   向量存储搜索结果: {len(vs_results)} 个")
        
        for i, result in enumerate(vs_results):
            similarity = result.get('similarity', 0)
            print(f"     结果 {i+1}: 相似度 {similarity:.4f}")
        
        # 测试RAG引擎查询
        rag_result = rag.generate_answer(test_query, include_system_info=False)
        relevant_docs = rag_result.get('relevant_docs', [])
        answer = rag_result.get('answer', '')
        
        print(f"   RAG引擎查询结果: {len(relevant_docs)} 个相关文档")
        print(f"   回答长度: {len(answer)} 字符")
        
        if relevant_docs and "天津商务职业学院" in answer:
            print("   ✅ RAG功能正常")
        else:
            print("   ❌ RAG功能异常")
            print(f"   回答预览: {answer[:100]}...")
        
        # 4. 修复建议
        print("\n4. 修复建议:")
        
        if vs_stats.get('document_count', 0) > 0 and len(documents) > 0:
            print("   ✅ 文档存储正常")
            
            if len(vs_results) > 0:
                print("   ✅ 搜索功能正常")
                
                if len(relevant_docs) > 0:
                    print("   ✅ RAG查询正常")
                    print("   🎯 问题可能在GUI显示，请重启应用")
                else:
                    print("   ❌ RAG查询异常，检查相似度阈值")
            else:
                print("   ❌ 搜索功能异常，检查向量化器")
        else:
            print("   ❌ 文档存储异常，需要重新添加文档")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def reset_knowledge_base():
    """
    重置知识库
    """
    print("\n🔄 重置知识库")
    print("=" * 40)
    
    try:
        # 删除向量存储文件
        vector_db_path = "./data/vector_db/vectors.pkl"
        if os.path.exists(vector_db_path):
            os.remove(vector_db_path)
            print("✅ 删除旧向量存储文件")
        
        # 重新创建目录
        os.makedirs("./data/vector_db", exist_ok=True)
        print("✅ 重新创建向量存储目录")
        
        return True
        
    except Exception as e:
        print(f"❌ 重置失败: {e}")
        return False

def main():
    """
    主函数
    """
    print("🔧 文档显示问题修复工具")
    print("=" * 50)
    
    print("此工具将:")
    print("- 检查向量存储和RAG引擎状态")
    print("- 测试文档搜索功能")
    print("- 提供修复建议")
    print()
    
    try:
        choice = input("选择操作:\n1. 诊断问题\n2. 重置知识库\n3. 退出\n请输入选择 (1-3): ").strip()
        
        if choice == '1':
            if fix_document_display():
                print("\n🎉 诊断完成！")
            else:
                print("\n❌ 诊断失败")
                
        elif choice == '2':
            confirm = input("⚠️  确定要重置知识库吗？这将删除所有文档 (y/N): ").strip().lower()
            if confirm == 'y':
                if reset_knowledge_base():
                    print("✅ 知识库重置完成，请重新添加文档")
                else:
                    print("❌ 知识库重置失败")
            else:
                print("👋 取消重置")
                
        elif choice == '3':
            print("👋 退出")
            
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n👋 操作中断")
    except Exception as e:
        print(f"❌ 操作失败: {e}")

if __name__ == "__main__":
    main()
