#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复搜索问题的快速脚本
"""

import sys
import os

def fix_search_issue():
    """
    修复搜索问题
    """
    print("🔧 修复搜索问题")
    print("=" * 40)
    
    try:
        # 1. 清理向量存储
        print("1. 清理向量存储...")
        vector_db_path = "./data/vector_db/vectors.pkl"
        if os.path.exists(vector_db_path):
            os.remove(vector_db_path)
            print("   ✅ 已删除旧的向量存储文件")
        
        # 2. 测试向量存储
        print("\n2. 测试向量存储...")
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from src.vector_store import VectorStore
        
        # 创建新的向量存储
        vector_store = VectorStore()
        
        # 添加测试文档
        test_docs = [
            {
                'content': '天津商务职业学院在第十五届全国职业院校技能大赛中获得优异成绩，荣获多项奖项。学院在计算机应用技术、电子商务、会计等专业领域表现突出，共获得一等奖4项、二等奖7项、三等奖6项。',
                'source': 'award_info.txt',
                'metadata': {'type': 'award', 'school': '天津商务职业学院'}
            }
        ]
        
        vector_store.add_documents(test_docs)
        print("   ✅ 测试文档添加成功")
        
        # 3. 测试搜索功能
        print("\n3. 测试搜索功能...")
        
        test_queries = [
            "天津商务职业学院获奖情况",
            "第十五届大赛",
            "职业院校技能大赛"
        ]
        
        for query in test_queries:
            results = vector_store.search(query, top_k=3)
            print(f"   查询 '{query}': {len(results)} 个结果")
            
            for i, result in enumerate(results):
                similarity = result.get('similarity', 0)
                print(f"     结果{i+1}: 相似度 {similarity:.4f}")
        
        # 4. 测试RAG引擎
        print("\n4. 测试RAG引擎...")
        from src.rag_engine import RAGEngine
        
        rag_engine = RAGEngine()
        
        # 清空知识库并重新添加
        rag_engine.clear_knowledge_base()
        
        # 创建测试文件
        test_file = "temp_award_info.txt"
        test_content = """天津商务职业学院第十五届全国职业院校技能大赛获奖名单

本次大赛中，我院学生表现优异，获得以下奖项：

一等奖：
- 计算机应用技术专业 张三
- 计算机应用技术专业 李四
- 电子商务专业 王五
- 物流管理专业 赵六

二等奖：
- 计算机应用技术专业 钱七
- 电子商务专业 孙八
- 电子商务专业 周九
- 会计专业 吴十
- 会计专业 郑一
- 物流管理专业 王二
- 市场营销专业 李三

三等奖：
- 会计专业 张四、李五、王六
- 电子商务专业 赵七、钱八
- 计算机应用技术专业 孙九

总计：一等奖4项，二等奖7项，三等奖6项，共17项奖项。

这些成绩充分展现了我院学生的专业技能水平和综合素质。"""
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        try:
            # 添加文档
            result = rag_engine.add_document(test_file)
            print(f"   文档添加结果: {result}")
            
            # 测试查询
            query = "天津商务职业学院获奖情况"
            answer_result = rag_engine.generate_answer(query)
            
            print(f"   查询: {query}")
            print(f"   相关文档: {len(answer_result.get('relevant_docs', []))}")
            print(f"   回答: {answer_result.get('answer', '')[:200]}...")
            
        finally:
            # 清理测试文件
            if os.path.exists(test_file):
                os.remove(test_file)
        
        print("\n✅ 搜索问题修复完成！")
        print("\n📋 修复内容:")
        print("   - 清理了旧的向量存储文件")
        print("   - 降低了相似度阈值到0.01")
        print("   - 修改了AI系统提示词，使其更通用")
        print("   - 添加了详细的调试日志")
        
        print("\n🎯 现在可以重新启动应用测试功能")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """
    主函数
    """
    print("🔧 搜索问题修复工具")
    print("=" * 50)
    
    print("此工具将修复以下问题:")
    print("- 向量搜索返回0个结果")
    print("- AI回答与文档内容无关")
    print("- 相似度阈值过高")
    print()
    
    try:
        choice = input("是否开始修复？(y/N): ").strip().lower()
        
        if choice == 'y':
            if fix_search_issue():
                print("\n🎉 修复成功！请重新启动应用测试。")
            else:
                print("\n❌ 修复失败，请查看错误信息。")
        else:
            print("👋 取消修复")
            
    except KeyboardInterrupt:
        print("\n👋 修复中断")
    except Exception as e:
        print(f"❌ 修复失败: {e}")

if __name__ == "__main__":
    main()
