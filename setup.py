"""
项目安装配置文件
"""

from setuptools import setup, find_packages

setup(
    name="quant-util",
    version="0.1.0",
    description="量化交易工具库",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Quant Util Team",
    author_email="example@example.com",
    url="https://github.com/example/quant-util",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.4",
        "terminaltables3>=0.1.0",
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "python-dateutil>=2.8.2",
        "pytz>=2021.1",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
)
