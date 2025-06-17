#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银河麒麟智能问答助手 - 系统诊断脚本
"""

import os
import sys
import importlib

def check_python_environment():
    """
    检查Python环境
    """
    print("🐍 Python环境检查")
    print("-" * 30)
    
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
    # 检查必要的Python模块
    required_modules = [
        'requests', 'numpy', 'sklearn', 'jieba', 
        'pdfplumber', 'docx', 'bs4', 'tkinter'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'tkinter':
                import tkinter
            else:
                importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - 未安装")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  缺少模块: {', '.join(missing_modules)}")
        print("运行以下命令安装:")
        print(f"pip3 install {' '.join(missing_modules)}")
    else:
        print("\n✅ 所有Python模块都已安装")
    
    return len(missing_modules) == 0

def check_project_structure():
    """
    检查项目结构
    """
    print("\n📁 项目结构检查")
    print("-" * 30)
    
    required_files = [
        'config.py', 'main.py', 'requirements.txt',
        'src/ai_models.py', 'src/rag_engine.py', 
        'src/vector_store.py', 'src/document_processor.py',
        'src/system_info_helper.py', 'src/gui.py'
    ]
    
    required_dirs = [
        'src', 'logs', 'data', 'data/vector_db', 'docs'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
            missing_files.append(file_path)
    
    missing_dirs = []
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - 目录不存在")
            missing_dirs.append(dir_path)
    
    if missing_files or missing_dirs:
        print(f"\n⚠️  缺少文件: {missing_files}")
        print(f"⚠️  缺少目录: {missing_dirs}")
        return False
    else:
        print("\n✅ 项目结构完整")
        return True

def check_configuration():
    """
    检查配置文件
    """
    print("\n⚙️  配置文件检查")
    print("-" * 30)
    
    try:
        from config import SILICONFLOW_API_KEY, VECTOR_DB_PATH
        
        # 检查API密钥
        if not SILICONFLOW_API_KEY or SILICONFLOW_API_KEY in ["YOUR_API_KEY_HERE", "sk-owsayozifrzvaxuxvyvywmyzcceokwatdbolevdnfnbwlurp"]:
            print("❌ API密钥未配置或使用默认值")
            print("   请编辑 config.py 设置您的硅基流动API密钥")
            api_configured = False
        else:
            print("✅ API密钥已配置")
            api_configured = True
        
        # 检查向量数据库路径
        print(f"向量数据库路径: {VECTOR_DB_PATH}")
        
        # 检查路径是否正确（应该是文件路径，不是目录）
        if VECTOR_DB_PATH.endswith('.pkl'):
            print("✅ 向量数据库路径格式正确")
            path_correct = True
        else:
            print("❌ 向量数据库路径格式错误（应该以.pkl结尾）")
            path_correct = False
        
        # 检查父目录是否存在
        parent_dir = os.path.dirname(VECTOR_DB_PATH)
        if os.path.exists(parent_dir):
            print(f"✅ 向量数据库父目录存在: {parent_dir}")
        else:
            print(f"❌ 向量数据库父目录不存在: {parent_dir}")
            os.makedirs(parent_dir, exist_ok=True)
            print(f"✅ 已创建目录: {parent_dir}")
        
        return api_configured and path_correct
        
    except ImportError as e:
        print(f"❌ 无法导入配置文件: {e}")
        return False

def check_vector_store():
    """
    检查向量存储功能
    """
    print("\n🗄️  向量存储检查")
    print("-" * 30)
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from src.vector_store import VectorStore
        
        # 创建向量存储实例
        vector_store = VectorStore()
        print("✅ 向量存储实例创建成功")
        
        # 获取统计信息
        stats = vector_store.get_stats()
        print(f"数据库路径: {stats['db_path']}")
        print(f"文档数量: {stats['document_count']}")
        print(f"是否已训练: {stats['is_fitted']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 向量存储检查失败: {e}")
        return False

def check_api_connection():
    """
    检查API连接
    """
    print("\n🌐 API连接检查")
    print("-" * 30)
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from src.ai_models import SiliconFlowAPI
        
        api = SiliconFlowAPI()
        if api.test_connection():
            print("✅ API连接测试成功")
            return True
        else:
            print("❌ API连接测试失败")
            return False
            
    except Exception as e:
        print(f"❌ API连接检查失败: {e}")
        return False

def generate_report():
    """
    生成诊断报告
    """
    print("\n📊 诊断报告")
    print("=" * 50)
    
    results = {
        'python_env': check_python_environment(),
        'project_structure': check_project_structure(),
        'configuration': check_configuration(),
        'vector_store': check_vector_store(),
        'api_connection': check_api_connection()
    }
    
    print(f"\n📋 总结:")
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    for check, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {check}: {status}")
    
    print(f"\n🎯 总体状态: {passed_checks}/{total_checks} 项检查通过")
    
    if passed_checks == total_checks:
        print("🎉 所有检查都通过，系统可以正常运行！")
    else:
        print("⚠️  存在问题，请根据上述检查结果进行修复")
        
        # 提供修复建议
        print("\n🔧 修复建议:")
        if not results['python_env']:
            print("  - 运行: pip3 install -r requirements.txt")
        if not results['configuration']:
            print("  - 编辑 config.py 配置API密钥")
        if not results['vector_store']:
            print("  - 运行: python3 fix_vector_store.py")
        if not results['api_connection']:
            print("  - 检查网络连接和API密钥")

def main():
    """
    主函数
    """
    print("🔍 银河麒麟智能问答助手 - 系统诊断")
    print("=" * 50)
    
    try:
        generate_report()
    except KeyboardInterrupt:
        print("\n👋 诊断中断")
    except Exception as e:
        print(f"❌ 诊断失败: {e}")

if __name__ == "__main__":
    main()
