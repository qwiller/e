# -*- coding: utf-8 -*-
"""
系统信息获取辅助模块 - 基于麒麟SDK2.5
"""

import ctypes
import logging
import os
import subprocess
from typing import Dict, Any, Optional
from config import KYLIN_SDK_CONFIG

class KylinSystemInfo:
    """
    麒麟系统信息获取类
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._load_kylin_libs()
        # 加载扩展SDK库
        self._load_extended_libraries()
        self._setup_extended_prototypes()
    
    def _load_kylin_libs(self):
        """
        加载麒麟SDK库
        """
        try:
            # 根据SDK2.5文档加载相关库
            sdk_config = KYLIN_SDK_CONFIG
            
            # 检查库文件是否存在
            lib_paths = {
                'sysinfo': sdk_config.get('system_lib_path', '/usr/lib/aarch64-linux-gnu/libkysysinfo.so'),
                'hardware': sdk_config.get('hardware_lib_path', '/usr/lib/aarch64-linux-gnu/libkyhardware.so'),
                'time': sdk_config.get('time_lib_path', '/usr/lib/aarch64-linux-gnu/libkydate.so'),
                'package': sdk_config.get('package_lib_path', '/usr/lib/aarch64-linux-gnu/libkypackage.so')
            }
            
            self.libs = {}
            for lib_name, lib_path in lib_paths.items():
                if os.path.exists(lib_path):
                    try:
                        self.libs[lib_name] = ctypes.CDLL(lib_path)
                        self.logger.info(f"成功加载 {lib_name} 库: {lib_path}")
                    except Exception as e:
                        self.logger.warning(f"加载 {lib_name} 库失败: {str(e)}")
                        self.libs[lib_name] = None
                else:
                    self.logger.warning(f"{lib_name} 库文件不存在: {lib_path}")
                    self.libs[lib_name] = None
            
            # 设置函数原型
            self._setup_function_prototypes()
            
        except Exception as e:
            self.logger.error(f"加载麒麟SDK库失败: {str(e)}")
            self.libs = {}
    
    def _setup_function_prototypes(self):
        """
        设置C函数原型
        """
        try:
            if self.libs.get('sysinfo'):
                # 设置系统信息相关函数原型
                # 根据SDK2.5文档设置返回类型和参数类型
                lib = self.libs['sysinfo']
                
                # 字符串返回函数
                for func_name in ['kdk_system_get_architecture', 'kdk_system_get_systemName', 
                                'kdk_system_get_version', 'kdk_system_get_hostName']:
                    if hasattr(lib, func_name):
                        func = getattr(lib, func_name)
                        func.restype = ctypes.c_char_p
                        func.argtypes = []
                
                # 整数返回函数
                for func_name in ['kdk_system_get_word', 'kdk_system_get_buildTime']:
                    if hasattr(lib, func_name):
                        func = getattr(lib, func_name)
                        func.restype = ctypes.c_int
                        func.argtypes = []
                        
        except Exception as e:
            self.logger.error(f"设置函数原型失败: {str(e)}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        获取系统基础信息
        """
        info = {
            '操作系统': '银河麒麟',
            '获取时间': self._get_current_time()
        }
        
        # 使用SDK获取系统信息
        if self.libs.get('sysinfo'):
            info.update(self._get_sdk_system_info())
        
        # 使用系统命令获取补充信息
        info.update(self._get_system_command_info())
        
        return info
    
    def _get_sdk_system_info(self) -> Dict[str, Any]:
        """
        使用SDK获取系统信息
        """
        info = {}
        lib = self.libs['sysinfo']
        
        try:
            # 获取系统架构
            if hasattr(lib, 'kdk_system_get_architecture'):
                arch = lib.kdk_system_get_architecture()
                if arch:
                    info['系统架构'] = arch.decode('utf-8')
            
            # 获取系统名称
            if hasattr(lib, 'kdk_system_get_systemName'):
                name = lib.kdk_system_get_systemName()
                if name:
                    info['系统名称'] = name.decode('utf-8')
            
            # 获取系统版本
            if hasattr(lib, 'kdk_system_get_version'):
                version = lib.kdk_system_get_version()
                if version:
                    info['系统版本'] = version.decode('utf-8')
            
            # 获取主机名
            if hasattr(lib, 'kdk_system_get_hostName'):
                hostname = lib.kdk_system_get_hostName()
                if hostname:
                    info['主机名'] = hostname.decode('utf-8')
            
            # 获取系统位数
            if hasattr(lib, 'kdk_system_get_word'):
                word = lib.kdk_system_get_word()
                if word > 0:
                    info['系统位数'] = f"{word}位"
                    
        except Exception as e:
            self.logger.error(f"获取SDK系统信息失败: {str(e)}")
        
        return info
    
    def _get_system_command_info(self) -> Dict[str, Any]:
        """
        使用系统命令获取补充信息
        """
        info = {}
        
        try:
            # 获取内核版本
            result = subprocess.run(['uname', '-r'], capture_output=True, text=True)
            if result.returncode == 0:
                info['内核版本'] = result.stdout.strip()
            
            # 获取CPU信息
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpu_info = f.read()
                    # 提取CPU型号
                    for line in cpu_info.split('\n'):
                        if 'model name' in line:
                            info['CPU型号'] = line.split(':')[1].strip()
                            break
                        elif 'Hardware' in line:  # ARM架构
                            info['硬件平台'] = line.split(':')[1].strip()
            except:
                pass
            
            # 获取内存信息
            try:
                with open('/proc/meminfo', 'r') as f:
                    mem_info = f.read()
                    for line in mem_info.split('\n'):
                        if 'MemTotal' in line:
                            mem_kb = int(line.split()[1])
                            mem_gb = round(mem_kb / 1024 / 1024, 2)
                            info['总内存'] = f"{mem_gb} GB"
                            break
            except:
                pass
            
            # 获取磁盘使用情况
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 4:
                        info['根分区大小'] = parts[1]
                        info['根分区已用'] = parts[2]
                        info['根分区可用'] = parts[3]
                        info['根分区使用率'] = parts[4]
            
            # 获取系统运行时间
            try:
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.read().split()[0])
                    days = int(uptime_seconds // 86400)
                    hours = int((uptime_seconds % 86400) // 3600)
                    minutes = int((uptime_seconds % 3600) // 60)
                    info['系统运行时间'] = f"{days}天 {hours}小时 {minutes}分钟"
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"获取系统命令信息失败: {str(e)}")
        
        return info
    
    # 删除以下两行错误的代码：
    # # 加载更多SDK库
    # self._load_extended_libraries()
    # self._setup_extended_prototypes()
    
    def _load_extended_libraries(self):
        """加载扩展的SDK库"""
        extended_libs = {
            'cpu': 'libkycpu.so',
            'network': 'libkynetwork.so', 
            'bios': 'libkybios.so',
            'board': 'libkyboard.so',
            'usb': 'libkyusb.so',
            'bluetooth': 'libkybluetooth.so',
            'display': 'libkydisplay.so',
            'edid': 'libkyedid.so',
            'fan': 'libkyfan.so',
            'security': 'libkysecurity.so'
        }
        
        for name, lib_name in extended_libs.items():
            try:
                lib_path = self._find_library_path(lib_name)
                if lib_path:
                    setattr(self, f'{name}_lib', ctypes.CDLL(lib_path))
                    self.logger.info(f"成功加载{name}库: {lib_path}")
            except Exception as e:
                self.logger.warning(f"加载{name}库失败: {e}")
                setattr(self, f'{name}_lib', None)

    def _find_library_path(self, lib_name: str) -> Optional[str]:
        """
        查找库文件路径
        """
        # 根据不同架构查找库文件
        arch = os.uname().machine
        if arch.startswith('aarch64'):
            paths = [
                f'/usr/lib/aarch64-linux-gnu/{lib_name}',
                f'/usr/lib/{lib_name}',
                f'/usr/local/lib/{lib_name}'
            ]
        else:
            paths = [
                f'/usr/lib/x86_64-linux-gnu/{lib_name}',
                f'/usr/lib/{lib_name}',
                f'/usr/local/lib/{lib_name}'
            ]
        
        for path in paths:
            if os.path.exists(path):
                return path
        return None

    def _apply_function_prototypes(self, lib, proto_map):
        """通用函数：根据映射设置 C 函数原型
        proto_map 形如 {func_name: (restype, argtypes)}
        """
        for func_name, (restype, argtypes) in proto_map.items():
            if hasattr(lib, func_name):
                func = getattr(lib, func_name)
                func.restype = restype
                func.argtypes = argtypes

    def _setup_extended_prototypes(self):
        """设置扩展的函数原型"""
        # CPU信息函数
        if hasattr(self, 'cpu_lib') and self.cpu_lib:
            cpu_funcs = {
                'kdk_cpu_get_arch': (ctypes.c_char_p, []),
                'kdk_cpu_get_vendor': (ctypes.c_char_p, []),
                'kdk_cpu_get_model': (ctypes.c_char_p, []),
                'kdk_cpu_get_freq_MHz': (ctypes.c_char_p, []),
                'kdk_cpu_get_corenums': (ctypes.c_uint, []),
                'kdk_cpu_get_virt': (ctypes.c_char_p, []),
                'kdk_cpu_get_process': (ctypes.c_uint, [])
            }
            self._apply_function_prototypes(self.cpu_lib, cpu_funcs)
        
        # 网络信息函数
        if hasattr(self, 'network_lib') and self.network_lib:
            network_funcs = {
                'kdk_nc_get_cardlist': (ctypes.POINTER(ctypes.c_char_p), []),
                'kdk_nc_get_ip': (ctypes.c_char_p, [ctypes.c_char_p]),
                'kdk_nc_get_mac': (ctypes.c_char_p, [ctypes.c_char_p]),
                'kdk_nc_get_type': (ctypes.c_char_p, [ctypes.c_char_p])
            }
            self._apply_function_prototypes(self.network_lib, network_funcs)
        
        # BIOS信息函数
        if hasattr(self, 'bios_lib') and self.bios_lib:
            bios_funcs = {
                'kdk_bios_get_manufacturer': (ctypes.c_char_p, []),
                'kdk_bios_get_version': (ctypes.c_char_p, []),
                'kdk_bios_get_release_date': (ctypes.c_char_p, [])
            }
            self._apply_function_prototypes(self.bios_lib, bios_funcs)
        
        # 主板信息函数
        if hasattr(self, 'board_lib') and self.board_lib:
            board_funcs = {
                'kdk_board_get_manufacturer': (ctypes.c_char_p, []),
                'kdk_board_get_product': (ctypes.c_char_p, []),
                'kdk_board_get_version': (ctypes.c_char_p, [])
            }
            self._apply_function_prototypes(self.board_lib, board_funcs)
        
        # USB信息函数
        if hasattr(self, 'usb_lib') and self.usb_lib:
            usb_funcs = {
                'kdk_usb_get_device_list': (ctypes.POINTER(ctypes.c_char_p), []),
                'kdk_usb_get_device_info': (ctypes.c_char_p, [ctypes.c_char_p])
            }
            self._apply_function_prototypes(self.usb_lib, usb_funcs)
        
        # 蓝牙信息函数
        if hasattr(self, 'bluetooth_lib') and self.bluetooth_lib:
            bt_funcs = {
                'kdk_bt_get_adapter_list': (ctypes.POINTER(ctypes.c_char_p), []),
                'kdk_bt_get_adapter_info': (ctypes.c_char_p, [ctypes.c_char_p])
            }
            self._apply_function_prototypes(self.bluetooth_lib, bt_funcs)
        
        # 显示器信息函数
        if hasattr(self, 'display_lib') and self.display_lib:
            display_funcs = {
                'kdk_display_get_monitor_list': (ctypes.POINTER(ctypes.c_char_p), []),
                'kdk_display_get_monitor_info': (ctypes.c_char_p, [ctypes.c_char_p])
            }
            self._apply_function_prototypes(self.display_lib, display_funcs)
        
        # EDID信息函数
        if hasattr(self, 'edid_lib') and self.edid_lib:
            edid_funcs = {
                'kdk_edid_get_raw': (ctypes.c_char_p, []),
                'kdk_edid_get_monitor_info': (ctypes.c_char_p, [])
            }
            self._apply_function_prototypes(self.edid_lib, edid_funcs)
        
        # 风扇信息函数
        if hasattr(self, 'fan_lib') and self.fan_lib:
            fan_funcs = {
                'kdk_fan_get_count': (ctypes.c_uint, []),
                'kdk_fan_get_status': (ctypes.c_char_p, [ctypes.c_uint]),
                'kdk_fan_get_speed': (ctypes.c_uint, [ctypes.c_uint])
            }
            self._apply_function_prototypes(self.fan_lib, fan_funcs)
        
        # 安全信息函数
        if hasattr(self, 'security_lib') and self.security_lib:
            security_funcs = {
                'kdk_security_get_status': (ctypes.c_char_p, []),
                'kdk_security_get_policy': (ctypes.c_char_p, [])
            }
            self._apply_function_prototypes(self.security_lib, security_funcs)
    
    def get_bios_info(self):
        """获取BIOS信息"""
        bios_info = {}
        
        if hasattr(self, 'bios_lib') and self.bios_lib:
            try:
                if hasattr(self.bios_lib, 'kdk_bios_get_vendor'):
                    vendor = self.bios_lib.kdk_bios_get_vendor()
                    if vendor:
                        bios_info['vendor'] = vendor.decode('utf-8')
                        # 释放内存
                        if hasattr(self.bios_lib, 'kdk_bios_free'):
                            self.bios_lib.kdk_bios_free(vendor)
                
                if hasattr(self.bios_lib, 'kdk_bios_get_version'):
                    version = self.bios_lib.kdk_bios_get_version()
                    if version:
                        bios_info['version'] = version.decode('utf-8')
                        # 释放内存
                        if hasattr(self.bios_lib, 'kdk_bios_free'):
                            self.bios_lib.kdk_bios_free(version)
                
            except Exception as e:
                self.logger.error(f"获取BIOS信息失败: {e}")
        
        return bios_info
    
    def get_complete_system_info(self):
        """获取完整的系统信息"""
        complete_info = self.get_system_info()  # 获取基础信息
        
        # 添加扩展信息
        complete_info.update({
            'extended_cpu': self.get_extended_cpu_info(),
            'network': self.get_network_info(),
            'bios': self.get_bios_info()
        })
        
        return complete_info

    def get_hardware_info(self) -> Dict[str, Any]:
        """
        获取硬件信息 - 基于麒麟SDK硬件接口
        """
        info = {}
        
        if self.libs.get('hardware'):
            lib = self.libs['hardware']
            try:
                # 获取CPU信息
                if hasattr(lib, 'kdk_hw_get_cpuinfo'):
                    cpu_info = lib.kdk_hw_get_cpuinfo()
                    if cpu_info:
                        info['CPU详细信息'] = self._parse_cpu_info(cpu_info)
                    
                # 获取内存信息
                if hasattr(lib, 'kdk_hw_get_meminfo'):
                    mem_info = lib.kdk_hw_get_meminfo()
                    if mem_info:
                        info['内存详细信息'] = self._parse_memory_info(mem_info)
                    
                # 获取磁盘信息
                if hasattr(lib, 'kdk_hw_get_diskinfo'):
                    disk_info = lib.kdk_hw_get_diskinfo()
                    if disk_info:
                        info['磁盘详细信息'] = self._parse_disk_info(disk_info)
                        
            except Exception as e:
                self.logger.error(f"获取硬件信息失败: {str(e)}")
        
        return info
    
    def get_security_status(self) -> Dict[str, Any]:
        """
        获取系统安全状态 - 基于麒麟SDK安全接口
        """
        info = {}
        
        if self.libs.get('security'):
            lib = self.libs['security']
            try:
                # 获取安全等级
                if hasattr(lib, 'kdk_sec_get_level'):
                    sec_level = lib.kdk_sec_get_level()
                    if sec_level >= 0:
                        levels = ['无', '低', '中', '高', '极高']
                        info['安全等级'] = levels[min(sec_level, len(levels)-1)]
                    
                # 获取防火墙状态
                if hasattr(lib, 'kdk_sec_get_firewall_status'):
                    fw_status = lib.kdk_sec_get_firewall_status()
                    info['防火墙状态'] = '启用' if fw_status else '禁用'
                    
            except Exception as e:
                self.logger.error(f"获取安全信息失败: {str(e)}")
        
        return info
    
    def _get_sdk_hardware_info(self) -> Dict[str, Any]:
        """
        使用SDK获取硬件信息
        """
        info = {}
        # 这里可以根据SDK2.5文档添加具体的硬件信息获取函数调用
        return info
    
    def _get_command_hardware_info(self) -> Dict[str, Any]:
        """
        使用命令获取硬件信息
        """
        info = {}
        
        try:
            # 获取USB设备
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            if result.returncode == 0:
                usb_devices = len(result.stdout.strip().split('\n'))
                info['USB设备数量'] = usb_devices
            
            # 获取PCI设备
            result = subprocess.run(['lspci'], capture_output=True, text=True)
            if result.returncode == 0:
                pci_devices = len(result.stdout.strip().split('\n'))
                info['PCI设备数量'] = pci_devices
                
        except Exception as e:
            self.logger.error(f"获取硬件信息失败: {str(e)}")
        
        return info
    
    def _get_current_time(self) -> str:
        """
        获取当前时间
        """
        import datetime
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_network_info(self) -> Dict[str, Any]:
        """
        获取网络信息
        """
        info = {}
        
        try:
            # 获取网络接口信息
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                interfaces = []
                current_interface = None
                
                for line in result.stdout.split('\n'):
                    if ': ' in line and not line.startswith(' '):
                        if current_interface:
                            interfaces.append(current_interface)
                        current_interface = {'name': line.split(':')[1].strip().split('@')[0]}
                    elif 'inet ' in line and current_interface:
                        ip = line.strip().split()[1].split('/')[0]
                        current_interface['ip'] = ip
            
                if current_interface:
                    interfaces.append(current_interface)
            
                info['网络接口'] = interfaces
            
        except Exception as e:
            self.logger.error(f"获取网络信息失败: {str(e)}")
        
        return info

    def get_process_info(self) -> Dict[str, Any]:
        """
        获取进程信息
        """
        info = {}
        
        try:
            # 获取进程数量
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if result.returncode == 0:
                process_count = len(result.stdout.strip().split('\n')) - 1  # 减去标题行
                info['进程总数'] = process_count
            
            # 获取负载信息
            try:
                with open('/proc/loadavg', 'r') as f:
                    load_avg = f.read().strip().split()[:3]
                    info['系统负载'] = f"{load_avg[0]} {load_avg[1]} {load_avg[2]}"
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"获取进程信息失败: {str(e)}")
        
        return info
    
    def is_kylin_system(self) -> bool:
        """
        检查是否为麒麟系统
        """
        try:
            # 检查系统发行版信息
            release_files = ['/etc/kylin-release', '/etc/os-release']
            
            for file_path in release_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        content = f.read().lower()
                        if 'kylin' in content:
                            return True
            
            # 检查SDK库是否存在
            return any(lib is not None for lib in self.libs.values())
            
        except Exception as e:
            self.logger.error(f"检查系统类型失败: {str(e)}")
            return False
    
    def get_full_system_report(self) -> Dict[str, Any]:
        """
        获取完整的系统报告
        """
        report = {
            '基本信息': self.get_system_info(),
            '硬件信息': self.get_hardware_info(),
            '网络信息': self.get_network_info(),
            '进程信息': self.get_process_info(),
            '是否麒麟系统': self.is_kylin_system()
        }
        
        return report