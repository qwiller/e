# -*- coding: utf-8 -*-
"""
图形用户界面模块 - 基于tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import logging
from typing import List
from pathlib import Path

from rag_engine import RAGEngine
from system_info_helper import KylinSystemInfo
from config import GUI_CONFIG, SUPPORTED_DOC_TYPES
from ai_models import SiliconFlowAPI
from voice_handler import VoiceHandler

class KylinQAApp:
    """
    银河麒麟智能问答助手GUI应用
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 初始化RAG引擎
        self.rag_engine = RAGEngine()
        self.system_info = KylinSystemInfo()
        
        # 初始化API实例
        self.ai_api = SiliconFlowAPI()

        # 初始化语音处理器
        self.voice_handler = VoiceHandler()

        # 创建主窗口
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()

        self.logger.info("GUI应用初始化完成")
    
    def setup_window(self):
        """
        设置主窗口
        """
        self.root.title(GUI_CONFIG.get('window_title', '银河麒麟智能问答助手'))
        self.root.geometry(GUI_CONFIG.get('window_size', '900x700'))
        
        # 设置图标（如果存在）
        icon_path = GUI_CONFIG.get('icon_path')
        if icon_path and Path(icon_path).exists():
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass
        
        # 设置字体
        self.font = (
            GUI_CONFIG.get('font_family', 'Arial'),
            GUI_CONFIG.get('font_size', 12)
        )
    
    def create_widgets(self):
        """
        创建界面组件
        """
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="银河麒麟智能问答助手", 
                               font=(self.font[0], self.font[1] + 4, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文档管理区域
        doc_frame = ttk.LabelFrame(main_frame, text="文档管理", padding="5")
        doc_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        doc_frame.columnconfigure(1, weight=1)
        
        ttk.Button(doc_frame, text="添加文档", command=self.add_documents).grid(row=0, column=0, padx=(0, 5))
        
        self.doc_status_label = ttk.Label(doc_frame, text="知识库状态: 未加载")
        self.doc_status_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Button(doc_frame, text="清空知识库", command=self.clear_knowledge_base).grid(row=0, column=2, padx=(5, 0))
        
        # 查询区域
        query_frame = ttk.LabelFrame(main_frame, text="智能问答", padding="5")
        query_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        query_frame.columnconfigure(0, weight=1)
        query_frame.rowconfigure(1, weight=1)
        
        # 问题输入
        input_frame = ttk.Frame(query_frame)
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        input_frame.columnconfigure(0, weight=1)
        
        self.question_entry = ttk.Entry(input_frame, font=self.font)
        self.question_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.question_entry.bind('<Return>', lambda e: self.ask_question())

        # 语音输入按钮
        voice_btn = ttk.Button(input_frame, text="🎤", command=self.voice_input)
        voice_btn.grid(row=0, column=1, padx=(0, 5))

        ttk.Button(input_frame, text="提问", command=self.ask_question).grid(row=0, column=2)
        
        # 选项
        options_frame = ttk.Frame(query_frame)
        options_frame.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        self.include_sysinfo = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="包含系统信息",
                       variable=self.include_sysinfo).grid(row=0, column=0)

        self.enable_voice_output = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="🔊语音播报",
                       variable=self.enable_voice_output).grid(row=0, column=1, padx=(10, 0))
        
        # 回答显示区域
        self.answer_text = scrolledtext.ScrolledText(query_frame, 
                                                    font=self.font,
                                                    wrap=tk.WORD,
                                                    height=20)
        self.answer_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        
        # 状态栏
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Button(status_frame, text="系统信息", command=self.show_system_info).grid(row=0, column=1, padx=(5, 0))
        
        # 更新知识库状态
        self.update_knowledge_base_status()
    
    def add_documents(self):
        """
        添加文档到知识库
        """
        file_types = [(f"{desc} (*{ext})", f"*{ext}") for ext, desc in SUPPORTED_DOC_TYPES.items()]
        file_types.append(("所有支持的文件", " ".join([f"*{ext}" for ext in SUPPORTED_DOC_TYPES.keys()])))
        
        file_paths = filedialog.askopenfilenames(
            title="选择文档文件",
            filetypes=file_types
        )
        
        if file_paths:
            self.status_label.config(text="正在处理文档...")
            self.root.update()
            
            def process_docs():
                try:
                    self.rag_engine.add_documents(list(file_paths))
                    self.root.after(0, lambda: self.status_label.config(text="文档添加完成"))
                    self.root.after(0, self.update_knowledge_base_status)
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("错误", f"添加文档失败: {str(e)}"))
                    self.root.after(0, lambda: self.status_label.config(text="就绪"))
            
            threading.Thread(target=process_docs, daemon=True).start()
    
    def ask_question(self):
        """
        处理用户提问
        """
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("警告", "请输入问题")
            return
        
        self.status_label.config(text="正在思考...")
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, "正在处理您的问题，请稍候...\n")
        self.root.update()
        
        def process_question():
            try:
                result = self.rag_engine.query(question, self.include_sysinfo.get())
                
                # 在主线程中更新UI
                self.root.after(0, lambda: self.display_answer(result))
                self.root.after(0, lambda: self.status_label.config(text="就绪"))
                
            except Exception as e:
                error_msg = f"处理问题时出错: {str(e)}"
                self.root.after(0, lambda: self.answer_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.answer_text.insert(tk.END, error_msg))
                self.root.after(0, lambda: self.status_label.config(text="就绪"))
        
        threading.Thread(target=process_question, daemon=True).start()

    def voice_input(self):
        """
        语音输入功能
        """
        if not self.voice_handler.is_available:
            messagebox.showwarning("警告", "语音功能不可用，请检查语音依赖安装")
            return

        # 显示语音输入状态
        original_text = self.question_entry.get()
        self.question_entry.delete(0, tk.END)
        self.question_entry.insert(0, "🎤 正在监听...")
        self.root.update()

        def voice_recognition():
            try:
                # 监听语音输入
                text = self.voice_handler.listen_for_speech(timeout=10)

                # 在主线程中更新UI
                def update_ui():
                    self.question_entry.delete(0, tk.END)
                    if text:
                        self.question_entry.insert(0, text)
                        messagebox.showinfo("语音识别", f"识别结果：{text}")
                    else:
                        self.question_entry.insert(0, original_text)
                        messagebox.showwarning("语音识别", "未能识别到语音内容，请重试")

                self.root.after(0, update_ui)

            except Exception as e:
                def show_error():
                    self.question_entry.delete(0, tk.END)
                    self.question_entry.insert(0, original_text)
                    messagebox.showerror("错误", f"语音识别失败：{str(e)}")

                self.root.after(0, show_error)

        threading.Thread(target=voice_recognition, daemon=True).start()

    def display_answer(self, result):
        """
        显示回答结果
        """
        self.answer_text.delete(1.0, tk.END)
        
        # 显示问题
        self.answer_text.insert(tk.END, f"问题: {result['question']}\n\n", "question")
        
        # 显示回答
        self.answer_text.insert(tk.END, f"回答:\n{result['answer']}\n\n", "answer")
        
        # 显示相关文档信息
        if result['relevant_docs']:
            self.answer_text.insert(tk.END, f"参考文档 ({len(result['relevant_docs'])} 个):\n", "info")
            for i, doc in enumerate(result['relevant_docs'][:3], 1):
                similarity = doc.get('similarity', 0)
                source = doc.get('source_file', '未知')
                self.answer_text.insert(tk.END, f"{i}. {Path(source).name} (相似度: {similarity:.3f})\n", "info")
        
        # 配置文本标签样式
        self.answer_text.tag_config("question", font=(self.font[0], self.font[1], 'bold'))
        self.answer_text.tag_config("answer", font=self.font)
        self.answer_text.tag_config("info", font=(self.font[0], self.font[1] - 1), foreground="gray")

        # 语音播报
        if self.enable_voice_output.get() and self.voice_handler.is_available:
            self.voice_handler.speak_text(result['answer'], async_mode=True)
    
    def show_system_info(self):
        """
        显示系统信息
        """
        try:
            info = self.system_info.get_full_system_report()
            
            # 创建新窗口显示系统信息
            info_window = tk.Toplevel(self.root)
            info_window.title("系统信息")
            info_window.geometry("600x500")
            
            text_widget = scrolledtext.ScrolledText(info_window, font=self.font)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 格式化显示系统信息
            for category, data in info.items():
                text_widget.insert(tk.END, f"=== {category} ===\n")
                if isinstance(data, dict):
                    for key, value in data.items():
                        text_widget.insert(tk.END, f"{key}: {value}\n")
                else:
                    text_widget.insert(tk.END, f"{data}\n")
                text_widget.insert(tk.END, "\n")
            
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("错误", f"获取系统信息失败: {str(e)}")
    
    def clear_knowledge_base(self):
        """
        清空知识库
        """
        if messagebox.askyesno("确认", "确定要清空知识库吗？此操作不可撤销。"):
            try:
                self.rag_engine.clear_knowledge_base()
                self.update_knowledge_base_status()
                messagebox.showinfo("成功", "知识库已清空")
            except Exception as e:
                messagebox.showerror("错误", f"清空知识库失败: {str(e)}")
    
    def update_knowledge_base_status(self):
        """
        更新知识库状态
        """
        try:
            stats = self.rag_engine.get_knowledge_base_stats()
            doc_count = stats.get('document_count', 0)
            self.doc_status_label.config(text=f"知识库状态: {doc_count} 个文档")
        except Exception as e:
            self.doc_status_label.config(text="知识库状态: 获取失败")
    
    def run(self):
        """
        运行应用
        """
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.info("用户中断应用")
        except Exception as e:
            self.logger.error(f"应用运行出错: {str(e)}")
            messagebox.showerror("错误", f"应用运行出错: {str(e)}")