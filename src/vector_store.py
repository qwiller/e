# -*- coding: utf-8 -*-
"""
向量存储模块 - 基于scikit-learn实现
"""

import os
import pickle
import logging
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
from config import VECTOR_CONFIG, VECTOR_DB_PATH

class VectorStore:
    """
    向量存储类
    """
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or VECTOR_DB_PATH
        self.logger = logging.getLogger(__name__)
        
        # 初始化TF-IDF向量化器
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words=None,
            ngram_range=(1, 2),
            tokenizer=self._tokenize_chinese
        )
        
        self.documents = []
        self.vectors = None
        self.is_fitted = False
        
        # 创建存储目录
        db_dir = os.path.dirname(self.db_path)
        if db_dir:  # 确保目录路径不为空
            os.makedirs(db_dir, exist_ok=True)
        
        # 尝试加载已有数据
        self.load()
    
    def _tokenize_chinese(self, text: str) -> List[str]:
        """
        中文分词
        """
        return list(jieba.cut(text))
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        添加文档到向量存储
        
        Args:
            documents: 文档列表
        """
        try:
            self.documents.extend(documents)
            
            # 提取文档内容
            texts = [doc['content'] for doc in self.documents]
            
            # 重新训练向量化器
            self.vectors = self.vectorizer.fit_transform(texts)
            self.is_fitted = True
            
            self.logger.info(f"添加了 {len(documents)} 个文档，总计 {len(self.documents)} 个文档")
            
            # 保存到磁盘
            self.save()
            
        except Exception as e:
            self.logger.error(f"添加文档失败: {str(e)}")
            raise
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        搜索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            相关文档列表
        """
        if not self.is_fitted or len(self.documents) == 0:
            self.logger.warning("向量存储为空或未训练")
            return []
        
        try:
            top_k = top_k or VECTOR_CONFIG.get('max_results', 10)
            threshold = VECTOR_CONFIG.get('similarity_threshold', 0.1)

            self.logger.debug(f"搜索参数: top_k={top_k}, threshold={threshold}")
            self.logger.debug(f"文档数量: {len(self.documents)}, 向量形状: {self.vectors.shape if self.vectors is not None else None}")

            # 向量化查询
            query_vector = self.vectorizer.transform([query])
            self.logger.debug(f"查询向量形状: {query_vector.shape}")

            # 计算相似度
            similarities = cosine_similarity(query_vector, self.vectors).flatten()
            self.logger.debug(f"相似度分数: {similarities}")

            # 获取最相似的文档索引
            top_indices = np.argsort(similarities)[::-1][:top_k]
            self.logger.debug(f"Top {top_k} 索引: {top_indices}")

            results = []
            for idx in top_indices:
                similarity = similarities[idx]
                self.logger.debug(f"文档 {idx}: 相似度 {similarity:.4f}, 阈值 {threshold}")
                if similarity >= threshold:
                    doc = self.documents[idx].copy()
                    doc['similarity'] = float(similarity)
                    results.append(doc)
                    self.logger.debug(f"添加文档 {idx} 到结果: {doc.get('content', '')[:100]}...")
                else:
                    self.logger.debug(f"文档 {idx} 相似度 {similarity:.4f} 低于阈值 {threshold}")

            self.logger.info(f"查询 '{query}' 返回 {len(results)} 个结果")
            return results
            
        except Exception as e:
            self.logger.error(f"搜索失败: {str(e)}")
            return []
    
    def save(self):
        """
        保存向量存储到磁盘
        """
        try:
            data = {
                'documents': self.documents,
                'vectorizer': self.vectorizer,
                'vectors': self.vectors,
                'is_fitted': self.is_fitted
            }
            
            with open(self.db_path, 'wb') as f:
                pickle.dump(data, f)
            
            self.logger.info(f"向量存储已保存到 {self.db_path}")
            
        except Exception as e:
            self.logger.error(f"保存向量存储失败: {str(e)}")
    
    def load(self):
        """
        从磁盘加载向量存储
        """
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'rb') as f:
                    data = pickle.load(f)
                
                self.documents = data.get('documents', [])
                self.vectorizer = data.get('vectorizer', self.vectorizer)
                self.vectors = data.get('vectors')
                self.is_fitted = data.get('is_fitted', False)
                
                self.logger.info(f"从 {self.db_path} 加载了 {len(self.documents)} 个文档")
            
        except Exception as e:
            self.logger.warning(f"加载向量存储失败: {str(e)}")
    
    def clear(self):
        """
        清空向量存储
        """
        self.documents = []
        self.vectors = None
        self.is_fitted = False
        
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        
        self.logger.info("向量存储已清空")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取存储统计信息
        """
        return {
            'document_count': len(self.documents),
            'is_fitted': self.is_fitted,
            'db_path': self.db_path,
            'vector_shape': self.vectors.shape if self.vectors is not None else None
        }