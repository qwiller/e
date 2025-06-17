# 🖥️ Windows开发环境安装指南

> **注意：此指南仅用于Windows开发测试，生产环境请使用银河麒麟系统**

## 📋 Windows环境要求

- Windows 10/11
- Python 3.8 或更高版本
- 网络连接

## 🚀 快速安装步骤

### 第一步：安装Python
1. 访问 https://www.python.org/downloads/
2. 下载Python 3.8+版本
3. 安装时勾选"Add Python to PATH"

### 第二步：下载项目
```cmd
# 使用git
git clone https://github.com/qwiller/d.git
cd d

# 或下载zip包解压
```

### 第三步：运行安装脚本
```cmd
# 双击运行
quick_deploy.bat

# 或在命令行运行
quick_deploy.bat
```

### 第四步：配置API密钥
1. 编辑 `config.py` 文件
2. 将 `SILICONFLOW_API_KEY` 设置为您的API密钥
3. 保存文件

### 第五步：启动应用
```cmd
python main.py
```

## ⚠️ Windows环境限制

- 麒麟SDK功能不可用
- 系统信息获取受限
- 某些语音功能可能不稳定

## 🔧 常见问题

**Python未找到？**
- 确保Python已添加到PATH环境变量
- 重新安装Python并勾选"Add Python to PATH"

**依赖安装失败？**
- 使用管理员权限运行命令提示符
- 手动安装：`pip install requests numpy scikit-learn`

**界面无法显示？**
- 确保安装了tkinter：`pip install tk`

---

**💡 建议：完整功能体验请使用银河麒麟操作系统**
