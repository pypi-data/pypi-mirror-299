from setuptools import setup, find_packages

setup(
    name='fl-cipher',  # 库的名称，要与PyPI上未被占用的名称一致
    version='1.0.0',  # 版本号，遵循语义化版本规范(主版本号.次版本号.修订号)
    packages=find_packages(),
    author='FengLing',
    author_email='damon__dong@163.com',
    description='一个包含AES、DES、RSA加密模块的包',
    long_description=open('README.md', encoding='utf8').read(),  # 假设你有一个README.md文件来详细描述库的功能等
    long_description_content_type='text/markdown',
    license='MIT',  # 库的许可证类型
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'  # 支持的Python版本
)