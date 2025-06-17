#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银河麒麟智能问答助手 - 主程序
"""

import sys
import os
import logging
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_logging():
    """
    设置日志系统
    """
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("日志系统初始化完成")
    return logger

def check_dependencies():
    """
    检查依赖项
    """
    logger = logging.getLogger(__name__)
    
    required_modules = [
        'tkinter',
        'numpy', 
        'sklearn',
        'jieba',
        'requests'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            logger.debug(f"✅ {module} 可用")
        except ImportError:
            missing_modules.append(module)
            logger.warning(f"❌ {module} 缺失")
    
    if missing_modules:
        logger.error(f"缺少依赖模块: {missing_modules}")
        print(f"❌ 缺少依赖模块: {missing_modules}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    logger.info("✅ 所有依赖项检查通过")
    return True

def check_directories():
    """
    检查并创建必要的目录
    """
    logger = logging.getLogger(__name__)
    
    directories = [
        "data",
        "data/vector_db", 
        "logs",
        "assets"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"创建目录: {directory}")
        else:
            logger.debug(f"目录已存在: {directory}")
    
    return True

def check_config():
    """
    检查配置文件
    """
    logger = logging.getLogger(__name__)
    
    try:
        from config import SILICONFLOW_API_KEY, validate_config
        
        # 验证配置
        issues = validate_config()
        
        if issues:
            logger.warning(f"配置问题: {issues}")
            # 但不阻止启动，因为我们已经设置了API密钥
        
        # 检查API密钥
        if not SILICONFLOW_API_KEY or SILICONFLOW_API_KEY == "YOUR_API_KEY_HERE":
            logger.error("API密钥未配置")
            return False
        
        logger.info("✅ 配置检查通过")
        return True
        
    except Exception as e:
        logger.error(f"配置检查失败: {e}")
        return False

def main():
    """
    主函数
    """
    print("🚀 银河麒麟智能问答助手")
    print("=" * 50)
    
    # 设置日志
    logger = setup_logging()
    
    try:
        # 检查依赖项
        if not check_dependencies():
            return 1
        
        # 检查目录
        check_directories()
        
        # 检查配置
        if not check_config():
            logger.error("配置检查失败，无法启动")
            return 1
        
        # 导入并启动GUI
        logger.info("启动GUI应用...")
        
        try:
            from gui import RAGApplication
            
            app = RAGApplication()
            logger.info("GUI应用创建成功")
            
            print("✅ 应用启动成功！")
            print("📋 功能说明:")
            print("  - 📁 添加文档：支持PDF、TXT、MD等格式")
            print("  - 🤖 智能问答：基于文档内容回答问题")
            print("  - 🎤 语音输入：支持语音提问")
            print("  - 🔊 语音播报：支持语音回答")
            print("  - 🖥️ 系统信息：显示麒麟系统信息")
            print()
            
            app.run()
            
        except ImportError as e:
            logger.error(f"导入GUI模块失败: {e}")
            print(f"❌ 导入GUI模块失败: {e}")
            return 1
            
    except KeyboardInterrupt:
        logger.info("用户中断应用")
        print("\n👋 应用已退出")
        return 0
        
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        print(f"❌ 应用启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    logger.info("应用正常退出")
    return 0

if __name__ == "__main__":
    sys.exit(main())
