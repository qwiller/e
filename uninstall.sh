#!/bin/bash

# 银河麒麟智能问答助手卸载脚本

echo "银河麒麟智能问答助手卸载程序"
echo "========================================"

# 检查权限
if [ "$EUID" -ne 0 ]; then
    echo "请使用sudo运行此卸载脚本"
    exit 1
fi

# 确认卸载
read -p "确定要卸载银河麒麟智能问答助手吗? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消卸载"
    exit 0
fi

# 停止服务
echo "停止系统服务..."
systemctl stop kylin-qa.service 2>/dev/null || true
systemctl disable kylin-qa.service 2>/dev/null || true

# 删除服务文件
rm -f /etc/systemd/system/kylin-qa.service
systemctl daemon-reload

# 删除安装目录
echo "删除程序文件..."
rm -rf /opt/kylin-qa-assistant

# 删除快捷方式
rm -f /home/kylin/Desktop/kylin-qa.desktop
rm -f /usr/local/bin/kylin-qa

echo "卸载完成！"