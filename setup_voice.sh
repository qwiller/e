#!/bin/bash
# 语音功能配置脚本

echo "🎤 配置语音功能..."

# 检查系统类型
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "检测到Linux系统，配置麒麟系统语音支持..."
    
    # 安装系统级语音依赖
    sudo apt update
    sudo apt install -y \
        portaudio19-dev \
        python3-pyaudio \
        espeak espeak-data \
        libespeak1 libespeak-dev \
        festival festvox-kallpc16k \
        alsa-utils pulseaudio
    
    # 配置音频权限
    sudo usermod -a -G audio $USER
    
    echo "✅ Linux语音依赖安装完成"
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "检测到Windows系统..."
    echo "请确保已安装Windows语音引擎"
    echo "建议安装Microsoft Speech Platform"
    
else
    echo "⚠️ 未识别的系统类型: $OSTYPE"
fi

# 测试语音功能
echo "🧪 测试语音功能..."
python3 -c "
try:
    import speech_recognition as sr
    import pyttsx3
    print('✅ 语音识别模块导入成功')
    
    # 测试TTS
    engine = pyttsx3.init()
    print('✅ 语音合成引擎初始化成功')
    
    # 测试麦克风
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('✅ 麦克风访问成功')
    
    print('🎉 语音功能配置完成！')
    
except Exception as e:
    print(f'❌ 语音功能测试失败: {e}')
    print('请检查依赖安装和设备权限')
"

echo "📝 语音功能使用说明:"
echo "1. 点击🎤按钮开始语音输入"
echo "2. 勾选🔊语音播报启用回答朗读"
echo "3. 确保麦克风权限已授予应用"
echo "4. 在安静环境中使用以获得最佳识别效果"