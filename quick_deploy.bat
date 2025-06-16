@echo off
REM 银河麒麟智能问答助手 - Windows快速部署脚本
REM 注意：此脚本仅用于开发测试，生产环境请使用Linux版本

echo 🌟 银河麒麟智能问答助手 - Windows开发环境部署
echo ==================================================
echo.

REM 检查Python
echo [INFO] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python版本过低，需要3.8或更高版本
    pause
    exit /b 1
)

echo [SUCCESS] Python环境检查通过

REM 检查pip
echo [INFO] 检查pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到pip，请重新安装Python
    pause
    exit /b 1
)

REM 升级pip
echo [INFO] 升级pip...
python -m pip install --upgrade pip

REM 配置pip镜像源
echo [INFO] 配置pip国内镜像源...
if not exist "%APPDATA%\pip" mkdir "%APPDATA%\pip"
echo [global] > "%APPDATA%\pip\pip.ini"
echo index-url = https://pypi.tuna.tsinghua.edu.cn/simple >> "%APPDATA%\pip\pip.ini"
echo trusted-host = pypi.tuna.tsinghua.edu.cn >> "%APPDATA%\pip\pip.ini"
echo timeout = 120 >> "%APPDATA%\pip\pip.ini"

REM 安装Python依赖
echo [INFO] 安装Python依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] 部分依赖安装失败，尝试单独安装...
    pip install requests numpy scikit-learn jieba pdfplumber python-docx beautifulsoup4 lxml
)

REM 创建必要目录
echo [INFO] 创建必要目录...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "data\vector_db" mkdir data\vector_db
if not exist "docs" mkdir docs
if not exist "assets" mkdir assets

REM 检查配置文件
echo [INFO] 检查配置文件...
findstr "YOUR_API_KEY_HERE" config.py >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] 检测到默认API密钥，需要配置您的硅基流动API密钥
    echo.
    echo 请访问 https://cloud.siliconflow.cn 获取您的API密钥
    echo 然后编辑 config.py 文件，将 SILICONFLOW_API_KEY 设置为您的密钥
    echo.
)

REM 测试安装
echo [INFO] 测试Python模块导入...
python -c "
import sys
modules = ['requests', 'numpy', 'sklearn', 'jieba']
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError:
        print(f'✗ {module} - 导入失败')
"

echo.
echo [SUCCESS] 🎉 安装完成！
echo.
echo 📋 使用说明:
echo 1. 启动应用: python main.py
echo 2. 配置API密钥: 编辑 config.py 文件
echo 3. 查看文档: README.md
echo.
echo ⚠️  注意: Windows环境仅用于开发测试
echo    生产环境请在银河麒麟系统上部署
echo.
pause
