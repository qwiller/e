#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有已知问题的综合脚本
"""

import os
import sys
import subprocess

def create_icons():
    """
    创建应用图标
    """
    print("🎨 创建应用图标...")
    
    try:
        # 运行图标创建脚本
        subprocess.run([sys.executable, "create_icons.py"], check=True)
        print("✅ 图标创建完成")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  图标创建失败，使用默认图标")
        return False
    except FileNotFoundError:
        print("⚠️  图标创建脚本不存在")
        return False

def fix_voice_issues():
    """
    修复语音问题
    """
    print("🎤 修复语音问题...")
    
    try:
        # 检查音频设备
        result = subprocess.run(['aplay', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 音频播放设备检测正常")
        else:
            print("⚠️  音频播放设备检测失败")
        
        # 检查PulseAudio
        result = subprocess.run(['pulseaudio', '--check'], capture_output=True)
        if result.returncode == 0:
            print("✅ PulseAudio运行正常")
        else:
            print("⚠️  PulseAudio未运行，尝试启动...")
            subprocess.run(['pulseaudio', '--start'], capture_output=True)
        
        return True
    except FileNotFoundError:
        print("⚠️  音频工具未安装")
        return False

def fix_search_issues():
    """
    修复搜索问题
    """
    print("🔍 修复搜索问题...")
    
    try:
        # 清理向量存储
        vector_db_path = "./data/vector_db/vectors.pkl"
        if os.path.exists(vector_db_path):
            os.remove(vector_db_path)
            print("✅ 清理旧向量存储")
        
        # 确保目录存在
        os.makedirs("./data/vector_db", exist_ok=True)
        print("✅ 向量存储目录就绪")
        
        return True
    except Exception as e:
        print(f"❌ 修复搜索问题失败: {e}")
        return False

def test_voice_functionality():
    """
    测试语音功能
    """
    print("🧪 测试语音功能...")
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from src.voice_handler import VoiceHandler
        
        voice_handler = VoiceHandler()
        
        if voice_handler.is_available:
            print("✅ 语音处理器初始化成功")
            
            # 测试语音合成
            test_text = "这是语音测试"
            if voice_handler.speak_text(test_text, async_mode=False):
                print("✅ 语音合成测试成功")
            else:
                print("❌ 语音合成测试失败")
            
            return True
        else:
            print("❌ 语音功能不可用")
            return False
            
    except Exception as e:
        print(f"❌ 语音功能测试失败: {e}")
        return False

def test_rag_functionality():
    """
    测试RAG功能
    """
    print("🧪 测试RAG功能...")
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from src.rag_engine import RAGEngine
        
        rag_engine = RAGEngine()
        
        # 添加测试文档
        test_content = """天津商务职业学院在第十五届全国职业院校技能大赛中获得优异成绩。
        
获奖情况：
- 计算机应用技术专业：一等奖2项
- 电子商务专业：一等奖1项，二等奖2项
- 会计专业：二等奖2项，三等奖3项

总计获得一等奖3项，二等奖4项，三等奖3项。"""
        
        # 创建临时文件
        test_file = "temp_test.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        try:
            # 添加文档
            result = rag_engine.add_document(test_file)
            print(f"✅ 文档添加: {result}")
            
            # 测试查询
            query = "天津商务职业学院获奖情况"
            answer_result = rag_engine.generate_answer(query)
            
            relevant_docs = answer_result.get('relevant_docs', [])
            answer = answer_result.get('answer', '')
            
            print(f"✅ 查询测试: 找到 {len(relevant_docs)} 个相关文档")
            
            if relevant_docs and "天津商务职业学院" in answer:
                print("✅ RAG功能测试成功")
                return True
            else:
                print("❌ RAG功能测试失败：回答与文档不匹配")
                print(f"回答: {answer[:100]}...")
                return False
                
        finally:
            # 清理测试文件
            if os.path.exists(test_file):
                os.remove(test_file)
        
    except Exception as e:
        print(f"❌ RAG功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """
    主修复函数
    """
    print("🔧 银河麒麟智能问答助手 - 综合问题修复")
    print("=" * 60)
    
    results = {}
    
    # 1. 创建图标
    results['icons'] = create_icons()
    
    # 2. 修复语音问题
    results['voice_fix'] = fix_voice_issues()
    
    # 3. 修复搜索问题
    results['search_fix'] = fix_search_issues()
    
    # 4. 测试语音功能
    results['voice_test'] = test_voice_functionality()
    
    # 5. 测试RAG功能
    results['rag_test'] = test_rag_functionality()
    
    # 显示结果
    print("\n📊 修复结果总结:")
    print("-" * 40)
    
    for task, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        task_name = {
            'icons': '图标创建',
            'voice_fix': '语音修复',
            'search_fix': '搜索修复',
            'voice_test': '语音测试',
            'rag_test': 'RAG测试'
        }.get(task, task)
        
        print(f"{task_name}: {status}")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n🎯 总体状态: {success_count}/{total_count} 项成功")
    
    if success_count == total_count:
        print("\n🎉 所有问题修复完成！可以启动应用了。")
        print("\n🚀 启动命令: python3 main.py")
    else:
        print("\n⚠️  部分问题仍需手动处理，请查看上述结果。")
        
        # 提供具体建议
        if not results.get('voice_fix') or not results.get('voice_test'):
            print("\n🎤 语音问题建议:")
            print("   - 检查音频设备连接")
            print("   - 运行: sudo apt install pulseaudio pulseaudio-utils")
            print("   - 重新登录系统以应用音频权限")
        
        if not results.get('rag_test'):
            print("\n🔍 RAG问题建议:")
            print("   - 检查API密钥配置")
            print("   - 运行: python3 debug_search.py")
            print("   - 查看日志文件: tail -f logs/app.log")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 修复中断")
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()
