from setuptools import setup, find_packages

setup(
    name="quant-util",
    version="0.1",
    packages=find_packages(include=['*', 'data.*', 'pages.*', 'utils.*', 'test.*']),
    install_requires=[
        'tushare',
        'akshare',
        'pandas',
        'numpy',
    ],
) 