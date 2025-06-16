#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音功能测试脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.voice_handler import VoiceHandler

def test_voice_functionality():
    """
    测试语音功能
    """
    print("🎤 银河麒麟智能问答助手 - 语音功能测试")
    print("=" * 50)
    
    # 初始化语音处理器
    voice_handler = VoiceHandler()
    
    # 检查语音功能可用性
    print(f"语音功能可用性: {'✅ 可用' if voice_handler.is_available else '❌ 不可用'}")
    
    if not voice_handler.is_available:
        print("\n❌ 语音功能不可用，请检查以下依赖：")
        print("1. pip install SpeechRecognition pyttsx3")
        print("2. sudo apt install portaudio19-dev python3-pyaudio")
        print("3. sudo apt install espeak espeak-data")
        return False
    
    # 获取语音信息
    voice_info = voice_handler.get_voice_info()
    print(f"\n📊 语音配置信息:")
    print(f"  - 当前语音引擎: {voice_info.get('current_voice', '默认')}")
    print(f"  - 语音速度: {voice_info.get('rate', 150)}")
    print(f"  - 音量: {voice_info.get('volume', 0.8)}")
    
    # 测试语音功能
    test_results = voice_handler.test_voice_functionality()
    print(f"\n🧪 功能测试结果:")
    print(f"  - 麦克风: {'✅' if test_results['microphone'] else '❌'}")
    print(f"  - 语音合成: {'✅' if test_results['text_to_speech'] else '❌'}")
    print(f"  - 语音识别: {'✅' if test_results['speech_recognition'] else '❌'}")
    
    # 交互式测试
    print(f"\n🎯 交互式测试:")
    
    # 测试语音合成
    print("1. 测试语音合成...")
    test_text = "您好，我是银河麒麟智能问答助手，语音功能测试成功！"
    if voice_handler.speak_text(test_text, async_mode=False):
        print("   ✅ 语音合成测试成功")
    else:
        print("   ❌ 语音合成测试失败")
    
    # 测试语音识别
    print("\n2. 测试语音识别...")
    print("   请在5秒内说话（例如：你好）...")
    
    try:
        recognized_text = voice_handler.listen_for_speech(timeout=5)
        if recognized_text:
            print(f"   ✅ 识别成功: {recognized_text}")
            
            # 播报识别结果
            response_text = f"我听到您说的是：{recognized_text}"
            voice_handler.speak_text(response_text, async_mode=False)
        else:
            print("   ⚠️ 未识别到语音内容")
    except Exception as e:
        print(f"   ❌ 语音识别测试失败: {e}")
    
    print(f"\n🎉 语音功能测试完成！")
    return True

def interactive_voice_test():
    """
    交互式语音测试
    """
    voice_handler = VoiceHandler()
    
    if not voice_handler.is_available:
        print("❌ 语音功能不可用")
        return
    
    print("\n🎤 进入交互式语音测试模式")
    print("说话后系统会重复您说的内容，输入 'quit' 退出")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\n按回车开始语音输入，或输入 'quit' 退出: ").strip()
            
            if user_input.lower() == 'quit':
                break
            
            print("🎤 正在监听... (5秒超时)")
            text = voice_handler.listen_for_speech(timeout=5)
            
            if text:
                print(f"识别结果: {text}")
                response = f"您说的是：{text}"
                voice_handler.speak_text(response, async_mode=False)
            else:
                print("未识别到语音内容")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"错误: {e}")
    
    print("👋 退出语音测试")

if __name__ == "__main__":
    print("选择测试模式:")
    print("1. 基础功能测试")
    print("2. 交互式测试")
    
    try:
        choice = input("请选择 (1/2): ").strip()
        
        if choice == "1":
            test_voice_functionality()
        elif choice == "2":
            interactive_voice_test()
        else:
            print("无效选择，执行基础功能测试")
            test_voice_functionality()
            
    except KeyboardInterrupt:
        print("\n👋 测试中断")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
