# 🚀 银河麒麟智能问答助手 - 超简单安装指南

> **专为初学者设计，3步完成安装！**

## 📋 安装前准备

确保您的系统满足以下要求：
- ✅ 银河麒麟操作系统 V10 SP1 或更高版本
- ✅ 有网络连接
- ✅ 有管理员权限（sudo）

## 🎯 三步安装法

### 第一步：下载项目
```bash
# 方法1：使用git（推荐）
git clone https://github.com/qwiller/d.git
cd d

# 方法2：如果没有git，下载zip包
wget https://github.com/qwiller/d/archive/main.zip
unzip main.zip
cd d-main
```

### 第二步：一键安装
```bash
# 给安装脚本执行权限
chmod +x easy_install.sh

# 运行安装脚本（完全自动化）
./easy_install.sh
```

**安装过程说明：**
- ⏱️ 安装时间：5-10分钟
- 🔄 完全自动化，无需手动操作
- 📦 自动安装所有依赖
- 🎤 自动配置语音功能
- 🔧 自动安装麒麟SDK

### 第三步：配置和启动
```bash
# 方法1：使用启动脚本（推荐）
chmod +x start.sh
./start.sh

# 方法2：直接启动
python3 main.py
```

**首次启动会提示配置API密钥：**
1. 访问 https://cloud.siliconflow.cn
2. 注册并获取免费API密钥
3. 按提示输入密钥即可

## 🎉 安装完成！

启动后您将看到图形界面，可以：
- 💬 输入问题进行智能问答
- 🎤 点击麦克风按钮使用语音输入
- 📚 上传文档建立知识库
- 🔊 开启语音播报功能
- 🖥️ 查看系统信息

## ❓ 遇到问题？

### 常见问题快速解决

**1. 安装失败？**
```bash
# 检查网络连接
ping baidu.com

# 重新运行安装
./easy_install.sh
```

**2. 语音功能不工作？**
```bash
# 测试语音功能
python3 test_voice.py

# 重新登录系统（应用音频权限）
```

**3. 界面无法显示？**
```bash
# 检查图形环境
echo $DISPLAY

# 安装图形界面支持
sudo apt install python3-tk
```

**4. API调用失败？**
- 检查网络连接
- 确认API密钥正确
- 查看 logs/app.log 日志文件

## 📞 获取帮助

- 📖 详细文档：查看 README.md
- 🐛 问题报告：GitHub Issues
- 💡 功能建议：GitHub Discussions

---

**🌟 就是这么简单！3步完成安装，立即体验智能问答！**
