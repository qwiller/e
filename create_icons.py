#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建应用图标
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_app_icon():
    """
    创建应用图标
    """
    # 创建64x64的图标
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制圆形背景
    margin = 4
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=2)
    
    # 绘制"AI"文字
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
    
    text = "AI"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # 保存图标
    os.makedirs('assets', exist_ok=True)
    img.save('assets/app_icon.png')
    print("✅ 应用图标创建完成: assets/app_icon.png")
    
    return 'assets/app_icon.png'

def create_microphone_icon():
    """
    创建麦克风图标
    """
    size = 24
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制麦克风主体（椭圆）
    mic_width = 8
    mic_height = 12
    mic_x = (size - mic_width) // 2
    mic_y = 3
    
    draw.ellipse([mic_x, mic_y, mic_x + mic_width, mic_y + mic_height], 
                fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=1)
    
    # 绘制麦克风支架
    stand_x = size // 2
    stand_y = mic_y + mic_height
    draw.line([stand_x, stand_y, stand_x, stand_y + 4], fill=(52, 152, 219, 255), width=2)
    
    # 绘制底座
    base_width = 6
    base_x = stand_x - base_width // 2
    base_y = stand_y + 4
    draw.line([base_x, base_y, base_x + base_width, base_y], fill=(52, 152, 219, 255), width=2)
    
    # 绘制声波线条
    for i in range(3):
        offset = 2 + i * 2
        y_pos = mic_y + mic_height // 2
        draw.arc([mic_x + mic_width + offset, y_pos - offset, 
                 mic_x + mic_width + offset + 4, y_pos + offset], 
                start=270, end=90, fill=(52, 152, 219, 255), width=1)
    
    img.save('assets/microphone_icon.png')
    print("✅ 麦克风图标创建完成: assets/microphone_icon.png")
    
    return 'assets/microphone_icon.png'

def create_simple_icons():
    """
    创建简单的文本图标（如果PIL不可用）
    """
    os.makedirs('assets', exist_ok=True)
    
    # 创建简单的文本文件作为占位符
    with open('assets/app_icon.txt', 'w') as f:
        f.write("AI Assistant Icon")
    
    with open('assets/microphone_icon.txt', 'w') as f:
        f.write("🎤")
    
    print("✅ 简单图标创建完成")

def main():
    """
    主函数
    """
    print("🎨 创建应用图标")
    print("=" * 30)
    
    try:
        # 尝试使用PIL创建图标
        import PIL
        create_app_icon()
        create_microphone_icon()
    except ImportError:
        print("⚠️  PIL未安装，创建简单图标")
        create_simple_icons()
        print("提示：安装PIL可以创建更好的图标: pip install Pillow")

if __name__ == "__main__":
    main()
