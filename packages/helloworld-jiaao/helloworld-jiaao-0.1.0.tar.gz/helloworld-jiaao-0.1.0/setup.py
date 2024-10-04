# setup.py

from setuptools import setup, find_packages

setup(
    name="helloworld-jiaao",  # 包名
    version="0.1.0",  # 版本号
    description="A simple hello world package",  # 简短描述
    long_description=open('README.md').read(),  # 读取详细描述
    long_description_content_type="text/markdown",
    author="Your Name",  # 作者名
    author_email="your.email@example.com",  # 作者邮箱
    url="https://github.com/yourusername/helloworld",  # 项目主页URL
    packages=find_packages(),  # 自动查找项目中的包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 支持的Python版本
)

