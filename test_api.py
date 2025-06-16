# -*- coding: utf-8 -*-
"""
测试硅基流动API连接
"""

import logging
import time
from src.ai_models import SiliconFlowAPI

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建API实例
api = SiliconFlowAPI()

# 测试API连接
def test_connection():
    logger.info("正在测试API连接...")
    try:
        if api.test_connection():
            logger.info("API连接测试成功！")
            return True
        else:
            logger.error("API连接测试失败")
            return False
    except Exception as e:
        logger.error(f"API连接测试异常: {str(e)}")
        return False

def test_chat():
    """测试聊天功能"""
    logger.info("正在测试聊天功能...")
    
    # 测试用例1: 简单问候
    messages1 = [
        {"role": "user", "content": "你好，我是银河麒麟系统的用户"}
    ]
    
    # 测试用例2: 详细问题
    messages2 = [
        {"role": "user", "content": "请详细介绍一下银河麒麟操作系统的主要特点和优势"}
    ]
    
    # 测试用例3: 多轮对话
    messages3 = [
        {"role": "user", "content": "我最近在使用银河麒麟系统，遇到了一些问题"},
        {"role": "assistant", "content": "请告诉我具体遇到了什么问题，我会尽力帮你解决"},
        {"role": "user", "content": "软件安装时提示缺少某些依赖包，怎么解决？"}
    ]
    
    test_cases = [
        (messages1, "简单问候测试"),
        (messages2, "详细问题测试"),
        (messages3, "多轮对话测试")
    ]
    
    all_success = True
    
    for messages, test_name in test_cases:
        logger.info(f"\n=== 开始测试: {test_name} ===")
        
        try:
            # 增加超时时间
            response = api.chat_completion(
                messages,
                max_retries=3,
                retry_delay=3,
                temperature=0.7,
                max_tokens=4096
            )
            
            if "error" not in response:
                logger.info("完整API响应:")
                # 分段输出响应内容
                response_str = json.dumps(response, indent=2, ensure_ascii=False)
                for i in range(0, len(response_str), 1000):  # 每1000字符输出一次
                    logger.info(response_str[i:i+1000])
                
                logger.info(f"{test_name}成功！")
                logger.info(f"回答内容: {response['choices'][0]['message']['content']}")
            else:
                logger.error(f"{test_name}失败: {response['error']}")
                all_success = False
        except Exception as e:
            logger.error(f"{test_name}异常: {str(e)}")
            all_success = False
            
    return all_success

def test_answer():
    """测试问答功能"""
    logger.info("正在测试问答功能...")
    
    try:
        # 测试简单问答
        simple_answer = api.generate_answer(
            question="什么是银河麒麟操作系统？",
            context="银河麒麟操作系统是由中国电子集团开发的国产操作系统，基于Linux内核，支持国产CPU和硬件平台。"
        )
        logger.info("简单问答测试:")
        logger.info(simple_answer)
        
        # 测试包含系统信息的问答
        system_answer = api.generate_answer(
            question="我的电脑配置是什么？",
            context="CPU: 龙芯3A5000\n内存: 16GB\n显卡: 国产7A1000\n系统版本: 银河麒麟V10 SP3",
            include_system_info=True,
            system_info="操作系统: 银河麒麟V10 SP3\n架构: x86_64\n内核版本: 5.10.0-kylin"
        )
        logger.info("系统信息问答测试:")
        logger.info(system_answer)
        
        # 测试长文本问答
        long_context = """
        银河麒麟操作系统是一款基于Linux内核的国产操作系统，由中国电子集团开发。
        主要特点包括：
        1. 完全自主可控
        2. 支持国产CPU架构（包括龙芯、飞腾、兆芯等）
        3. 支持主流国产数据库（达梦、金仓、神通等）
        4. 支持主流国产中间件（东方通、中创、金蝶等）
        5. 支持主流国产办公软件（金山WPS、永中Office等）
        """
        long_answer = api.generate_answer(
            question="银河麒麟操作系统的主要特点是什么？",
            context=long_context
        )
        logger.info("长文本问答测试:")
        logger.info(long_answer)
        
    except Exception as e:
        logger.error(f"问答测试失败: {str(e)}")
        return False
    return True

if __name__ == "__main__":
    logger.info("开始API测试...")
    if test_connection():
        logger.info("开始测试聊天功能...")
        chat_result = test_chat()
        logger.info("开始测试问答功能...")
        answer_result = test_answer()
        logger.info("测试完成！")
        logger.info(f"测试结果: 连接测试成功，聊天测试: {chat_result}，问答测试: {answer_result}")
    else:
        logger.error("API连接测试失败，测试终止")
