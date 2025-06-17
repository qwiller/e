# 🔧 故障排除快速指南

## 🚨 安装问题

### 问题：安装脚本运行失败
```bash
# 解决方案1：检查权限
chmod +x easy_install.sh
ls -la easy_install.sh

# 解决方案2：手动运行
bash easy_install.sh

# 解决方案3：检查网络
ping baidu.com
```

### 问题：Python依赖安装失败
```bash
# 解决方案1：更新pip
python3 -m pip install --upgrade pip

# 解决方案2：使用国内镜像
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests numpy

# 解决方案3：分别安装
pip3 install requests
pip3 install numpy
pip3 install scikit-learn
```

### 问题：麒麟SDK安装失败
```bash
# 解决方案1：更新软件源
sudo apt update

# 解决方案2：检查系统版本
cat /etc/kylin-release

# 解决方案3：跳过SDK（功能受限但可运行）
# 编辑 config.py，设置 KYLIN_SDK_AVAILABLE = False
```

## 🎤 语音功能问题

### 问题：语音识别不工作
```bash
# 解决方案1：测试语音功能
python3 test_voice.py

# 解决方案2：检查音频设备
aplay -l
arecord -l

# 解决方案3：重新安装语音依赖
sudo apt install --reinstall python3-pyaudio portaudio19-dev
```

### 问题：语音合成无声音
```bash
# 解决方案1：检查音频服务
pulseaudio --check -v

# 解决方案2：重启音频服务
pulseaudio --kill
pulseaudio --start

# 解决方案3：测试系统音频
speaker-test -t wav -c 2
```

### 问题：麦克风权限问题
```bash
# 解决方案1：添加用户到音频组
sudo usermod -a -G audio $USER

# 解决方案2：重新登录系统
# 注销并重新登录

# 解决方案3：检查权限
groups $USER | grep audio
```

## 🖥️ 界面问题

### 问题：GUI界面无法启动
```bash
# 解决方案1：检查显示环境
echo $DISPLAY
export DISPLAY=:0.0

# 解决方案2：安装tkinter
sudo apt install python3-tk

# 解决方案3：检查X11服务
ps aux | grep X11
```

### 问题：界面显示异常
```bash
# 解决方案1：更新系统
sudo apt update && sudo apt upgrade

# 解决方案2：重新安装图形库
sudo apt install --reinstall python3-tk

# 解决方案3：使用命令行模式
# 暂时跳过GUI，直接使用核心功能
```

## 🌐 网络和API问题

### 问题：API调用失败
```bash
# 解决方案1：检查网络连接
curl -I https://api.siliconflow.cn

# 解决方案2：检查API密钥
grep SILICONFLOW_API_KEY config.py

# 解决方案3：查看详细错误
tail -f logs/app.log
```

### 问题：网络连接超时
```bash
# 解决方案1：配置代理（如果需要）
export http_proxy=http://proxy:port
export https_proxy=http://proxy:port

# 解决方案2：增加超时时间
# 编辑 config.py，增加 timeout 值

# 解决方案3：使用国内镜像
# 已在安装脚本中配置
```

## 📊 性能问题

### 问题：程序运行缓慢
```bash
# 解决方案1：检查系统资源
htop
free -h

# 解决方案2：优化配置
# 编辑 config.py，减小 chunk_size 和 max_results

# 解决方案3：清理缓存
rm -rf data/vector_db/*
```

### 问题：内存占用过高
```bash
# 解决方案1：调整配置参数
# 在 config.py 中设置：
# VECTOR_CONFIG["chunk_size"] = 300
# VECTOR_CONFIG["max_results"] = 5

# 解决方案2：重启应用
# 定期重启应用释放内存

# 解决方案3：监控内存使用
watch -n 1 'ps aux | grep python3'
```

## 🔍 调试技巧

### 查看日志
```bash
# 实时查看日志
tail -f logs/app.log

# 查看错误日志
grep ERROR logs/app.log

# 清理日志
> logs/app.log
```

### 测试各个模块
```bash
# 测试AI模型
python3 -c "from src.ai_models import SiliconFlowAPI; print(SiliconFlowAPI().test_connection())"

# 测试文档处理
python3 -c "from src.document_processor import DocumentProcessor; print('文档处理模块正常')"

# 测试向量存储
python3 -c "from src.vector_store import VectorStore; print('向量存储模块正常')"

# 测试系统信息
python3 -c "from src.system_info_helper import KylinSystemInfo; print('系统信息模块正常')"
```

### 重置环境
```bash
# 清理所有数据
rm -rf logs/* data/vector_db/*

# 重新创建目录
mkdir -p logs data/vector_db docs

# 重新安装依赖
pip3 install --force-reinstall -r requirements.txt
```

## 📞 获取帮助

如果以上方法都无法解决问题：

1. **查看完整日志**：`cat logs/app.log`
2. **检查系统信息**：`uname -a && python3 --version`
3. **提交Issue**：在GitHub上提交详细的错误信息
4. **社区求助**：在项目讨论区寻求帮助

---

**💡 提示：大多数问题都可以通过重新运行安装脚本解决**
