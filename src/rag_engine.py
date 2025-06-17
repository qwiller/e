# -*- coding: utf-8 -*-
"""
RAG (检索增强生成) 引擎模块
"""

import logging
from typing import List, Dict, Any, Optional
from ai_models import SiliconFlowAPI
from vector_store import VectorStore
from document_processor import DocumentProcessor
from system_info_helper import KylinSystemInfo
from config import RAG_CONFIG

class RAGEngine:
    """
    RAG (检索增强生成) 引擎
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.document_processor = DocumentProcessor()
        self.ai_model = SiliconFlowAPI()
        self.logger = logging.getLogger(__name__)
        
        # 初始化系统信息助手
        try:
            self.system_helper = KylinSystemInfo()
        except Exception as e:
            self.logger.warning(f"系统信息助手初始化失败: {e}")
            self.system_helper = None
    
    def add_documents(self, file_paths: List[str]):
        """
        添加文档到知识库
        
        Args:
            file_paths: 文档文件路径列表
        """
        all_chunks = []
        
        for file_path in file_paths:
            try:
                self.logger.info(f"处理文档: {file_path}")
                chunks = self.document_processor.process_file(file_path)
                all_chunks.extend(chunks)
                
            except Exception as e:
                self.logger.error(f"处理文档 {file_path} 失败: {str(e)}")
        
        if all_chunks:
            self.vector_store.add_documents(all_chunks)
            self.logger.info(f"成功添加 {len(all_chunks)} 个文档块到知识库")
    
    def query(self, question: str, include_system_info: bool = False) -> Dict[str, Any]:
        """
        处理用户查询
        
        Args:
            question: 用户问题
            include_system_info: 是否包含系统信息
            
        Returns:
            查询结果
        """
        try:
            self.logger.info(f"处理查询: {question}")
            
            # 检索相关文档
            relevant_docs = self.vector_store.search(
                question,
                top_k=RAG_CONFIG.get('top_k', 5)
            )

            self.logger.info(f"检索到 {len(relevant_docs)} 个相关文档")
            for i, doc in enumerate(relevant_docs):
                self.logger.info(f"文档 {i+1}: 相似度 {doc.get('similarity', 0):.4f}, 内容: {doc.get('content', '')[:100]}...")

            # 构建上下文
            context = self._build_context(relevant_docs, include_system_info)
            self.logger.info(f"构建的上下文长度: {len(context)} 字符")
            if context:
                self.logger.debug(f"上下文内容: {context[:200]}...")
            
            # 生成回答
            answer = self.ai_model.generate_answer(question, context)
            
            result = {
                'question': question,
                'answer': answer or "抱歉，我无法回答这个问题。请检查API配置或稍后重试。",
                'relevant_docs': relevant_docs,
                'context_length': len(context),
                'system_info_included': include_system_info
            }
            
            self.logger.info(f"查询完成，找到 {len(relevant_docs)} 个相关文档")
            return result
            
        except Exception as e:
            self.logger.error(f"查询处理失败: {str(e)}")
            return {
                'question': question,
                'answer': f"处理查询时出现错误: {str(e)}",
                'relevant_docs': [],
                'context_length': 0,
                'system_info_included': False
            }
    
    def _build_context(self, relevant_docs: List[Dict[str, Any]], 
                      include_system_info: bool = False) -> str:
        """
        构建上下文信息
        
        Args:
            relevant_docs: 相关文档列表
            include_system_info: 是否包含系统信息
            
        Returns:
            上下文字符串
        """
        context_parts = []
        
        # 添加系统信息
        if include_system_info and self.system_helper:
            try:
                sys_info = self.system_helper.get_system_info()
                context_parts.append("=== 当前系统信息 ===")
                for key, value in sys_info.items():
                    context_parts.append(f"{key}: {value}")
                context_parts.append("")
            except Exception as e:
                self.logger.warning(f"获取系统信息失败: {str(e)}")
        elif include_system_info and not self.system_helper:
            self.logger.warning("系统信息助手未初始化，跳过系统信息获取")
        
        # 添加相关文档
        if relevant_docs:
            context_parts.append("=== 相关文档内容 ===")
            
            max_length = RAG_CONFIG.get('max_context_length', 2000)
            current_length = len("\n".join(context_parts))
            
            for i, doc in enumerate(relevant_docs):
                doc_text = f"文档{i+1} (相似度: {doc.get('similarity', 0):.3f}):\n{doc['content']}\n"
                
                if current_length + len(doc_text) > max_length:
                    break
                
                context_parts.append(doc_text)
                current_length += len(doc_text)
        
        return "\n".join(context_parts)
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """
        获取知识库统计信息
        """
        return self.vector_store.get_stats()
    
    def clear_knowledge_base(self):
        """
        清空知识库
        """
        self.vector_store.clear()
        self.logger.info("知识库已清空")