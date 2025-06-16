#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D-Bus服务调用助手
用于与麒麟SDK的D-Bus服务进行通信
"""

import logging
try:
    import dbus
    import dbus.service
    from dbus.mainloop.glib import DBusGMainLoop
    DBUS_AVAILABLE = True
except ImportError:
    DBUS_AVAILABLE = False
    logging.warning("D-Bus模块不可用，相关功能将被禁用")

logger = logging.getLogger(__name__)

class KylinDBusHelper:
    """麒麟SDK D-Bus服务助手"""
    
    def __init__(self):
        self.bus = None
        self.services = {}
        
        if DBUS_AVAILABLE:
            try:
                DBusGMainLoop(set_as_default=True)
                self.bus = dbus.SystemBus()
                logger.info("D-Bus连接已建立")
            except Exception as e:
                logger.error(f"D-Bus连接失败: {e}")
                self.bus = None
    
    def connect_time_service(self):
        """连接时间服务"""
        if not self.bus:
            return None
            
        try:
            service_name = 'com.kylin.kysdk.TimeServer'
            object_path = '/com/kylin/kysdk/Timer'
            interface_name = 'com.kylin.kysdk.TimeInterface'
            
            proxy = self.bus.get_object(service_name, object_path)
            interface = dbus.Interface(proxy, interface_name)
            
            self.services['time'] = interface
            logger.info("时间服务连接成功")
            return interface
            
        except Exception as e:
            logger.error(f"连接时间服务失败: {e}")
            return None
    
    def connect_date_service(self):
        """连接日期服务"""
        if not self.bus:
            return None
            
        try:
            service_name = 'com.kylin.kysdk.DateServer'
            object_path = '/com/kylin/kysdk/Date'
            interface_name = 'com.kylin.kysdk.DateInterface'
            
            proxy = self.bus.get_object(service_name, object_path)
            interface = dbus.Interface(proxy, interface_name)
            
            self.services['date'] = interface
            logger.info("日期服务连接成功")
            return interface
            
        except Exception as e:
            logger.error(f"连接日期服务失败: {e}")
            return None
    
    def setup_signal_handlers(self, time_change_callback=None, time_signal_callback=None):
        """设置信号处理器"""
        if not self.bus:
            return
            
        try:
            # 时间修改信号
            if time_change_callback:
                self.bus.add_signal_receiver(
                    time_change_callback,
                    signal_name='TimeChangeSignal',
                    dbus_interface='com.kylin.kysdk.TimeInterface',
                    bus_name='com.kylin.kysdk.TimeServer'
                )
                logger.info("时间修改信号处理器已设置")
            
            # 整分报时信号
            if time_signal_callback:
                self.bus.add_signal_receiver(
                    time_signal_callback,
                    signal_name='TimeSignal',
                    dbus_interface='com.kylin.kysdk.TimeInterface',
                    bus_name='com.kylin.kysdk.TimeServer'
                )
                logger.info("整分报时信号处理器已设置")
                
        except Exception as e:
            logger.error(f"设置信号处理器失败: {e}")
    
    def is_available(self):
        """检查D-Bus是否可用"""
        return DBUS_AVAILABLE and self.bus is not None

# 信号处理回调函数示例
def on_time_change(time_str):
    """时间修改信号回调"""
    logger.info(f"系统时间已修改: {time_str}")

def on_time_signal(time_str):
    """整分报时信号回调"""
    logger.info(f"整分报时: {time_str}")

# 使用示例
if __name__ == "__main__":
    dbus_helper = KylinDBusHelper()
    
    if dbus_helper.is_available():
        # 连接服务
        dbus_helper.connect_time_service()
        dbus_helper.connect_date_service()
        
        # 设置信号处理器
        dbus_helper.setup_signal_handlers(
            time_change_callback=on_time_change,
            time_signal_callback=on_time_signal
        )
        
        print("D-Bus服务已就绪")
    else:
        print("D-Bus服务不可用")