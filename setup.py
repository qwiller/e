# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="kylin-qa-assistant",
    version="2.6.0",
    author="Qwiller",
    author_email="",
    description="银河麒麟智能问答助手",
    long_description="基于硅基流动API和麒麟SDK2.5的智能问答系统",
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "requests>=2.31.0",
        "numpy>=1.24.3",
        "scikit-learn>=1.3.0",
        "pandas>=2.0.3",
        "PyYAML>=6.0.1",
        "python-dotenv>=1.0.0",
        "tqdm>=4.65.0",
        "python-dateutil>=2.8.2",
        "pillow>=10.0.0",
        "jinja2>=3.1.2",
        "lxml>=4.9.3",
        "beautifulsoup4>=4.12.2",
        "PyPDF2>=3.0.1",
        "docx>=0.2.8",
        "openpyxl>=3.1.2",
        "pygments>=2.16.1",
        "pygments-github-lexers>=0.1.0",
        "pygments-style-solarized>=0.1.0",
        "pygments-style-tomorrow>=0.1.0"
    ],
    package_data={
        '': ['*.yaml', '*.json', '*.txt', '*.md'],
    },
    entry_points={
        'console_scripts': [
            'kylin-qa=src.main:main',
        ],
    },
)
