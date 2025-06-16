#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银河麒麟智能问答助手
基于硅基流动API和麒麟SDK2.5
"""

import sys
import os
import logging
import argparse
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import LOG_CONFIG, GUI_CONFIG, validate_config
from gui import KylinQAApp
from system_info_helper import KylinSystemInfo

def setup_logging():
    """
    设置日志配置
    """
    log_dir = Path(LOG_CONFIG['file']).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=getattr(logging, LOG_CONFIG.get('level', 'INFO')),
        format=LOG_CONFIG.get('format', default_format),
        handlers=[
            logging.FileHandler(LOG_CONFIG.get('file', './logs/app.log'), encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_system_compatibility():
    """
    检查系统兼容性
    """
    logger = logging.getLogger(__name__)
    
    # 检查是否为麒麟系统
    system_info = KylinSystemInfo()
    if system_info.is_kylin_system():
        logger.info("检测到银河麒麟操作系统")
    else:
        logger.warning("未检测到银河麒麟系统，某些功能可能受限")
    
    # 验证配置
    config_issues = validate_config()
    if config_issues:
        logger.warning("配置问题：")
        for issue in config_issues:
            logger.warning(f"  - {issue}")

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='银河麒麟智能问答助手')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--no-gui', action='store_true', help='命令行模式（暂未实现）')
    parser.add_argument('--config', type=str, help='指定配置文件路径')
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("="*50)
    logger.info("银河麒麟智能问答助手 v2.5 启动")
    logger.info("="*50)
    
    try:
        # 检查系统兼容性
        check_system_compatibility()
        
        # 创建必要目录
        for directory in ['data', 'logs', 'docs']:
            Path(directory).mkdir(exist_ok=True)
        
        if args.no_gui:
            logger.info("命令行模式暂未实现，请使用图形界面模式")
            return 1
        
        # 启动GUI应用
        logger.info("启动图形界面...")
        app = KylinQAApp()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        return 0
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
    
    logger.info("程序正常退出")
    return 0

if __name__ == '__main__':
    sys.exit(main())