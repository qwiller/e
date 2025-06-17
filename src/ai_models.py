# -*- coding: utf-8 -*-
"""
AI模型接口模块 - 硅基流动API集成
"""

import requests
import json
import logging
from typing import List, Dict, Any, Optional
from config import SILICONFLOW_API_KEY, SILICONFLOW_API_ENDPOINT, RAG_CONFIG
import time

class SiliconFlowAPI:
    """
    硅基流动API接口类
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or SILICONFLOW_API_KEY
        self.endpoint = SILICONFLOW_API_ENDPOINT
        self.logger = logging.getLogger(__name__)
        
        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            self.logger.warning("硅基流动API密钥未配置")

    def chat_completion(self, messages: List[Dict[str, str]], 
                       model: str = "Qwen/Qwen2.5-72B-Instruct",
                       temperature: float = 0.7,
                       max_tokens: int = 2000,
                       stream: bool = False,
                       max_retries: int = 3,
                       retry_delay: int = 2) -> Dict[str, Any]:
        """
        调用硅基流动聊天完成API
        
        Args:
            messages: 对话消息列表
            model: 模型名称，默认使用Qwen2.5
            temperature: 温度参数
            max_tokens: 最大token数
            stream: 是否流式输出
            
        Returns:
            API响应结果
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "KylinOS-Assistant/2.6.0",
            "Accept": "application/json"
        }
        
        payload = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': min(max_tokens, 4096),  # 限制最大token数
            'top_p': 0.9,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0,
            'stop': None,
            'n': 1
        }
        
        for attempt in range(max_retries):
            try:
                self.logger.info(f"正在调用API，请求参数: {json.dumps(payload, indent=2, ensure_ascii=False)}")
                response = requests.post(
                    self.endpoint,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code != 200:
                    self.logger.error(f"API返回错误状态码: {response.status_code}")
                    self.logger.error(f"API响应内容: {response.text}")
                    if attempt < max_retries - 1:
                        self.logger.info(f"重试 {attempt + 1}/{max_retries}...")
                        time.sleep(retry_delay)
                        continue
                    return {"error": f"API返回错误状态码: {response.status_code}"}
                
                result = response.json()
                self.logger.info("API调用成功")
                self.logger.info(f"API响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return result
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"硅基流动API调用失败: {e}")
                if attempt < max_retries - 1:
                    self.logger.info(f"重试 {attempt + 1}/{max_retries}...")
                    time.sleep(retry_delay)
                    continue
                return {"error": str(e)}
            except json.JSONDecodeError as e:
                self.logger.error(f"解析API响应失败: {e}")
                if attempt < max_retries - 1:
                    self.logger.info(f"重试 {attempt + 1}/{max_retries}...")
                    time.sleep(retry_delay)
                    continue
                return {"error": "无法解析API响应"}
            except Exception as e:
                self.logger.error(f"API调用过程中出现未知错误: {e}")
                if attempt < max_retries - 1:
                    self.logger.info(f"重试 {attempt + 1}/{max_retries}...")
                    time.sleep(retry_delay)
                    continue
                return {"error": str(e)}

    def generate_answer(self, question: str, context: str = "", 
                       include_system_info: bool = False,
                       system_info: str = "") -> str:
        """
        生成问答回复
        
        Args:
            question: 用户问题
            context: 相关文档上下文
            include_system_info: 是否包含系统信息
            system_info: 系统信息
            
        Returns:
            AI生成的回答
        """
        # 构建系统提示词
        system_prompt = """
你是一个智能问答助手，能够基于提供的文档内容回答用户的问题。
请仔细阅读提供的文档内容，并基于这些信息给出准确、有用的回答。
如果文档中包含相关信息，请详细回答；如果文档中没有相关信息，请诚实地说明。
优先使用文档内容回答问题，确保回答的准确性和相关性。
        """.strip()
        
        # 构建用户消息
        user_message = f"问题：{question}"
        
        if context:
            user_message += f"\n\n相关文档：\n{context}"
        
        if include_system_info and system_info:
            user_message += f"\n\n当前系统信息：\n{system_info}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # 调用API
        response = self.chat_completion(
            messages=messages,
            temperature=RAG_CONFIG.get('temperature', 0.7),
            max_tokens=2000  # 使用固定的2000 token限制
        )
        
        if "error" in response:
            return f"抱歉，生成回答时出现错误：{response['error']}"
        
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError) as e:
            self.logger.error(f"解析API响应失败: {e}")
            return "抱歉，无法解析AI回答，请稍后重试。"

    def get_available_models(self) -> List[str]:
        """
        获取可用的模型列表
        
        Returns:
            可用模型列表
        """
        return [
            "Qwen/Qwen2.5-72B-Instruct",  # 推荐使用
            "Qwen/Qwen2.5-32B-Instruct",
            "Qwen/Qwen2.5-14B-Instruct"
        ]

    def test_connection(self) -> bool:
        """
        测试API连接
        
        Returns:
            连接是否成功
        """
        test_messages = [
            {"role": "user", "content": "你好"}
        ]
        
        response = self.chat_completion(
            messages=test_messages,
            max_tokens=10
        )
        
        return "error" not in response

