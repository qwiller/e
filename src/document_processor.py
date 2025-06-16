# -*- coding: utf-8 -*-
"""
文档处理模块 - 支持多种文档格式
"""

import os
import re
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# 导入文档处理库
try:
    import PyPDF2
    import pdfplumber
except ImportError:
    PyPDF2 = None
    pdfplumber = None

try:
    import markdown
    from bs4 import BeautifulSoup
except ImportError:
    markdown = None
    BeautifulSoup = None

from config import VECTOR_CONFIG, SUPPORTED_DOC_TYPES

class DocumentProcessor:
    """
    文档处理器类
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.chunk_size = VECTOR_CONFIG.get('chunk_size', 500)
        self.chunk_overlap = VECTOR_CONFIG.get('chunk_overlap', 50)
    
    def process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        处理单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文档块列表
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            file_ext = file_path.suffix.lower()
            
            # 根据文件类型选择处理方法
            if file_ext == '.pdf':
                content = self._process_pdf(file_path)
            elif file_ext == '.md':
                content = self._process_markdown(file_path)
            elif file_ext in ['.txt', '.rst']:
                content = self._process_text(file_path)
            else:
                raise ValueError(f"不支持的文件类型: {file_ext}")
            
            # 分块处理
            chunks = self._split_into_chunks(content, str(file_path), file_ext)
            
            # 提取结构化信息
            for chunk in chunks:
                chunk['sdk_interfaces'] = self._extract_sdk_interfaces(chunk['content'])
                chunk['headings'] = self._extract_headings(chunk['content'])
                chunk['keywords'] = self._extract_keywords(chunk['content'])
            
            self.logger.info(f"成功处理文件 {file_path}，生成 {len(chunks)} 个文档块")
            return chunks
            
        except Exception as e:
            self.logger.error(f"处理文件 {file_path} 失败: {str(e)}")
            raise
    
    def _process_pdf(self, file_path: Path) -> str:
        """
        处理PDF文件
        """
        content = ""
        
        # 优先使用pdfplumber
        if pdfplumber:
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            content += page_text + "\n"
                return content
            except Exception as e:
                self.logger.warning(f"pdfplumber处理失败，尝试PyPDF2: {str(e)}")
        
        # 备用PyPDF2
        if PyPDF2:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
                return content
            except Exception as e:
                self.logger.error(f"PyPDF2处理失败: {str(e)}")
        
        raise RuntimeError("无法处理PDF文件，请安装pdfplumber或PyPDF2")
    
    def _process_markdown(self, file_path: Path) -> str:
        """
        处理Markdown文件
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                md_content = file.read()
            
            if markdown and BeautifulSoup:
                # 转换为HTML然后提取纯文本
                html = markdown.markdown(md_content)
                soup = BeautifulSoup(html, 'html.parser')
                return soup.get_text()
            else:
                # 简单的Markdown处理
                # 移除Markdown标记
                content = re.sub(r'#{1,6}\s+', '', md_content)  # 标题
                content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # 粗体
                content = re.sub(r'\*(.*?)\*', r'\1', content)  # 斜体
                content = re.sub(r'`(.*?)`', r'\1', content)  # 行内代码
                content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)  # 链接
                return content
                
        except Exception as e:
            self.logger.error(f"处理Markdown文件失败: {str(e)}")
            raise
    
    def _process_text(self, file_path: Path) -> str:
        """
        处理文本文件
        """
        try:
            # 尝试不同的编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        return file.read()
                except UnicodeDecodeError:
                    continue
            
            raise UnicodeDecodeError("无法解码文件，尝试了多种编码格式")
            
        except Exception as e:
            self.logger.error(f"处理文本文件失败: {str(e)}")
            raise
    
    def _split_into_chunks(self, content: str, file_path: str, file_type: str) -> List[Dict[str, Any]]:
        """
        将内容分割成块
        """
        chunks = []
        
        # 清理内容
        content = self._clean_content(content)
        
        if len(content) <= self.chunk_size:
            # 内容较短，不需要分割
            chunks.append({
                'content': content,
                'chunk_id': 0,
                'source_file': file_path,
                'file_type': file_type,
                'start_pos': 0,
                'end_pos': len(content)
            })
        else:
            # 按段落分割
            paragraphs = content.split('\n\n')
            current_chunk = ""
            chunk_id = 0
            start_pos = 0
            
            for paragraph in paragraphs:
                # 检查添加当前段落是否会超过块大小
                if len(current_chunk) + len(paragraph) + 2 <= self.chunk_size:
                    if current_chunk:
                        current_chunk += "\n\n" + paragraph
                    else:
                        current_chunk = paragraph
                else:
                    # 保存当前块
                    if current_chunk:
                        chunks.append({
                            'content': current_chunk,
                            'chunk_id': chunk_id,
                            'source_file': file_path,
                            'file_type': file_type,
                            'start_pos': start_pos,
                            'end_pos': start_pos + len(current_chunk)
                        })
                        start_pos += len(current_chunk)
                        chunk_id += 1
                    
                    # 开始新块
                    current_chunk = paragraph
            
            # 保存最后一个块
            if current_chunk:
                chunks.append({
                    'content': current_chunk,
                    'chunk_id': chunk_id,
                    'source_file': file_path,
                    'file_type': file_type,
                    'start_pos': start_pos,
                    'end_pos': start_pos + len(current_chunk)
                })
        
        return chunks
    
    def _clean_content(self, content: str) -> str:
        """
        清理文本内容
        """
        # 移除多余的空白字符
        content = re.sub(r'\s+', ' ', content)
        
        # 移除多余的换行
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        # 移除首尾空白
        content = content.strip()
        
        return content
    
    def _extract_sdk_interfaces(self, content: str) -> Dict[str, Any]:
        """
        提取SDK接口信息
        """
        interfaces = {
            'c_interfaces': [],
            'dbus_interfaces': [],
            'python_interfaces': [],
            'api_calls': [],
            'data_structures': []
        }
        
        try:
            # C接口模式
            c_patterns = [
                r'extern\s+[\w\s\*]+\s+(\w+)\s*\([^)]*\);',  # extern函数声明
                r'[\w\s\*]+\s+(kdk_\w+)\s*\([^)]*\)',  # kdk开头的函数
                r'typedef\s+struct\s+(\w+)',  # 结构体定义
                r'#define\s+(\w+)\s+',  # 宏定义
            ]
            
            for pattern in c_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                interfaces['c_interfaces'].extend(matches)
            
            # DBus接口模式
            dbus_patterns = [
                r'(\w+)\s*\([^)]*\)\s*↦\s*\([^)]*\)',  # DBus方法签名
                r'interface\s+([\w\.]+)',  # 接口名称
                r'method\s+(\w+)',  # 方法名称
            ]
            
            for pattern in dbus_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                interfaces['dbus_interfaces'].extend(matches)
            
            # Python接口模式
            python_patterns = [
                r'def\s+(\w+)\s*\([^)]*\)',  # 函数定义
                r'class\s+(\w+)',  # 类定义
                r'import\s+([\w\.]+)',  # 导入模块
            ]
            
            for pattern in python_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                interfaces['python_interfaces'].extend(matches)
            
            # API调用模式
            api_patterns = [
                r'(\w+)\s*\(',  # 函数调用
                r'\.(\w+)\s*\(',  # 方法调用
            ]
            
            for pattern in api_patterns:
                matches = re.findall(pattern, content)
                interfaces['api_calls'].extend(matches)
            
            # 数据结构模式
            struct_patterns = [
                r'struct\s+(\w+)',  # 结构体
                r'enum\s+(\w+)',  # 枚举
                r'typedef\s+\w+\s+(\w+)',  # 类型定义
            ]
            
            for pattern in struct_patterns:
                matches = re.findall(pattern, content)
                interfaces['data_structures'].extend(matches)
            
            # 去重
            for key in interfaces:
                interfaces[key] = list(set(interfaces[key]))
            
        except Exception as e:
            self.logger.error(f"提取SDK接口信息失败: {str(e)}")
        
        return interfaces

    def _extract_headings(self, text: str) -> List[str]:
        """
        提取文档标题
        """
        headings = []

        # 提取Markdown风格标题
        markdown_headings = re.findall(r'^#{1,6}\s+(.+)$', text, re.MULTILINE)
        headings.extend(markdown_headings)

        # 提取其他可能的标题格式
        # 全大写的行（可能是标题）
        uppercase_lines = re.findall(r'^[A-Z\s]{5,}$', text, re.MULTILINE)
        headings.extend([line.strip() for line in uppercase_lines if len(line.strip()) < 50])

        # 中文标题模式
        chinese_headings = re.findall(r'^第[一二三四五六七八九十\d]+[章节部分]\s*[：:]\s*(.+)$', text, re.MULTILINE)
        headings.extend(chinese_headings)

        return list(set(headings))  # 去重

    def _extract_keywords(self, text: str) -> List[str]:
        """
        提取关键词
        """
        keywords = []

        # 麒麟系统相关关键词
        kylin_keywords = [
            '麒麟', '银河麒麟', 'Kylin', 'KylinOS',
            '系统安装', '配置', '故障排除', '安全',
            '驱动', '软件包', '服务', '网络',
            '用户管理', '权限', '防火墙', '备份'
        ]

        for keyword in kylin_keywords:
            if keyword in text:
                keywords.append(keyword)

        # 技术术语
        tech_terms = re.findall(r'\b[A-Z]{2,}\b', text)  # 大写缩写
        keywords.extend([term for term in tech_terms if len(term) <= 10])

        # 命令和文件路径
        commands = re.findall(r'`([^`]+)`', text)  # 反引号包围的命令
        keywords.extend([cmd for cmd in commands if len(cmd) <= 30])

        return list(set(keywords))  # 去重
    
    def get_supported_formats(self) -> List[str]:
        """
        获取支持的文件格式
        """
        return list(SUPPORTED_DOC_TYPES.keys())
    
    def validate_file(self, file_path: str) -> bool:
        """
        验证文件是否支持
        """
        try:
            file_path = Path(file_path)
            return file_path.exists() and file_path.suffix.lower() in SUPPORTED_DOC_TYPES
        except Exception:
            return False
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取文件信息
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {'error': '文件不存在'}
            
            stat = file_path.stat()
            
            return {
                'name': file_path.name,
                'size': stat.st_size,
                'size_mb': round(stat.st_size / 1024 / 1024, 2),
                'modified': stat.st_mtime,
                'extension': file_path.suffix.lower(),
                'supported': self.validate_file(str(file_path))
            }
            
        except Exception as e:
            return {'error': str(e)}