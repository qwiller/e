# -*- coding: utf-8 -*-
"""
语音处理模块 - 支持语音输入和语音播报
"""

import logging
import threading
import time
from typing import Optional, Callable

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

from config import VOICE_CONFIG

class VoiceHandler:
    """
    语音处理器类
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_available = VOICE_AVAILABLE
        
        if not self.is_available:
            self.logger.warning("语音功能不可用，请安装 speech_recognition 和 pyttsx3")
            return
        
        # 初始化语音识别器
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # 初始化语音合成器
        self.tts_engine = None
        self.is_speaking = False
        
        try:
            self._init_speech_recognition()
            self._init_text_to_speech()
            self.logger.info("语音功能初始化成功")
        except Exception as e:
            self.logger.error(f"语音功能初始化失败: {e}")
            self.is_available = False
    
    def _init_speech_recognition(self):
        """
        初始化语音识别
        """
        try:
            self.microphone = sr.Microphone()
            
            # 调整环境噪音
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.logger.info("语音识别初始化完成")
        except Exception as e:
            self.logger.error(f"语音识别初始化失败: {e}")
            raise
    
    def _init_text_to_speech(self):
        """
        初始化语音合成
        """
        try:
            self.tts_engine = pyttsx3.init()
            
            # 设置语音参数
            rate = VOICE_CONFIG.get('speech_rate', 150)
            volume = VOICE_CONFIG.get('speech_volume', 0.8)
            
            self.tts_engine.setProperty('rate', rate)
            self.tts_engine.setProperty('volume', volume)
            
            # 尝试设置中文语音
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            self.logger.info("语音合成初始化完成")
        except Exception as e:
            self.logger.error(f"语音合成初始化失败: {e}")
            raise
    
    def listen_for_speech(self, timeout: Optional[float] = None, 
                         phrase_timeout: Optional[float] = None) -> Optional[str]:
        """
        监听语音输入
        
        Args:
            timeout: 总超时时间
            phrase_timeout: 短语超时时间
            
        Returns:
            识别的文本，失败返回None
        """
        if not self.is_available or not self.microphone:
            self.logger.warning("语音识别不可用")
            return None
        
        try:
            timeout = timeout or VOICE_CONFIG.get('timeout', 5)
            phrase_timeout = phrase_timeout or VOICE_CONFIG.get('phrase_timeout', 1)
            
            self.logger.info("开始监听语音输入...")
            
            with self.microphone as source:
                # 监听音频
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_timeout
                )
            
            self.logger.info("语音录制完成，开始识别...")
            
            # 使用Google语音识别（支持中文）
            try:
                text = self.recognizer.recognize_google(
                    audio, 
                    language=VOICE_CONFIG.get('recognition_language', 'zh-CN')
                )
                self.logger.info(f"语音识别成功: {text}")
                return text
            except sr.UnknownValueError:
                self.logger.warning("无法识别语音内容")
                return None
            except sr.RequestError as e:
                self.logger.error(f"语音识别服务错误: {e}")
                # 尝试使用离线识别
                try:
                    text = self.recognizer.recognize_sphinx(audio, language='zh-cn')
                    self.logger.info(f"离线语音识别成功: {text}")
                    return text
                except:
                    return None
                    
        except sr.WaitTimeoutError:
            self.logger.warning("语音输入超时")
            return None
        except Exception as e:
            self.logger.error(f"语音识别失败: {e}")
            return None
    
    def speak_text(self, text: str, async_mode: bool = True) -> bool:
        """
        语音播报文本
        
        Args:
            text: 要播报的文本
            async_mode: 是否异步播报
            
        Returns:
            是否成功开始播报
        """
        if not self.is_available or not self.tts_engine:
            self.logger.warning("语音合成不可用")
            return False
        
        if self.is_speaking:
            self.logger.warning("正在播报中，跳过新的播报请求")
            return False
        
        try:
            if async_mode:
                # 异步播报
                thread = threading.Thread(target=self._speak_sync, args=(text,))
                thread.daemon = True
                thread.start()
                return True
            else:
                # 同步播报
                return self._speak_sync(text)
                
        except Exception as e:
            self.logger.error(f"语音播报失败: {e}")
            return False
    
    def _speak_sync(self, text: str) -> bool:
        """
        同步语音播报
        """
        try:
            self.is_speaking = True

            # 清理文本，避免特殊字符导致问题
            clean_text = text.strip()
            if not clean_text:
                return False

            self.logger.info(f"开始播报: {clean_text[:50]}...")

            # 设置合适的语音参数，避免怪音
            try:
                # 设置语速（较慢，避免怪音）
                self.tts_engine.setProperty('rate', 120)

                # 设置音量（适中）
                self.tts_engine.setProperty('volume', 0.7)

                # 尝试设置中文语音
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # 寻找中文语音
                    chinese_voice = None
                    for voice in voices:
                        if 'zh' in voice.id.lower() or 'chinese' in voice.name.lower():
                            chinese_voice = voice.id
                            break

                    if chinese_voice:
                        self.tts_engine.setProperty('voice', chinese_voice)
                        self.logger.debug(f"使用中文语音: {chinese_voice}")

            except Exception as e:
                self.logger.warning(f"设置语音参数失败: {e}")

            # 播报语音
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()

            self.logger.info("语音播报完成")
            return True

        except Exception as e:
            self.logger.error(f"语音播报执行失败: {e}")
            import traceback
            self.logger.error(f"详细错误: {traceback.format_exc()}")
            return False
        finally:
            self.is_speaking = False
    
    def stop_speaking(self):
        """
        停止语音播报
        """
        if self.tts_engine and self.is_speaking:
            try:
                self.tts_engine.stop()
                self.is_speaking = False
                self.logger.info("语音播报已停止")
            except Exception as e:
                self.logger.error(f"停止语音播报失败: {e}")
    
    def test_voice_functionality(self) -> dict:
        """
        测试语音功能
        
        Returns:
            测试结果字典
        """
        results = {
            'available': self.is_available,
            'speech_recognition': False,
            'text_to_speech': False,
            'microphone': False
        }
        
        if not self.is_available:
            return results
        
        # 测试麦克风
        try:
            if self.microphone:
                with self.microphone as source:
                    pass
                results['microphone'] = True
        except Exception as e:
            self.logger.error(f"麦克风测试失败: {e}")
        
        # 测试语音合成
        try:
            if self.tts_engine:
                # 简短测试
                self.tts_engine.say("测试")
                self.tts_engine.runAndWait()
                results['text_to_speech'] = True
        except Exception as e:
            self.logger.error(f"语音合成测试失败: {e}")
        
        # 语音识别需要实际音频输入，这里只检查初始化
        results['speech_recognition'] = self.recognizer is not None
        
        return results
    
    def get_voice_info(self) -> dict:
        """
        获取语音功能信息
        """
        info = {
            'available': self.is_available,
            'is_speaking': self.is_speaking,
            'config': VOICE_CONFIG
        }
        
        if self.is_available and self.tts_engine:
            try:
                voices = self.tts_engine.getProperty('voices')
                info['available_voices'] = [
                    {'id': voice.id, 'name': voice.name} 
                    for voice in voices[:5]  # 只显示前5个
                ]
                info['current_voice'] = self.tts_engine.getProperty('voice')
                info['rate'] = self.tts_engine.getProperty('rate')
                info['volume'] = self.tts_engine.getProperty('volume')
            except Exception as e:
                self.logger.error(f"获取语音信息失败: {e}")
        
        return info
