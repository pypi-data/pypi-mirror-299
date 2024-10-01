from setuptools import setup, find_packages

setup(
    name='PyDrawCLI',  # 包名
    version='4.0.0',  # 版本号
    description='A CLI tool for drawing shapes',  # 简短描述
    author='Momo',  # 作者
    author_email='2778623708@example.com',  # 作者邮箱
    url='https://github.com/mm-mhy/PyDrawCLI',  # 项目主页
    packages=find_packages(),  # 自动发现所有包和子包
    include_package_data=True,  # 包含数据文件
    install_requires=[  # 依赖列表
        'numpy',
        'textx'
    ],
    python_requires='>=3.6',  # Python 版本要求
)