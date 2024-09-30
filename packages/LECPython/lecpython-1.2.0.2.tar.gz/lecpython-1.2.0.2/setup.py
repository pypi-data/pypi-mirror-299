# setup.py
from setuptools import setup, find_packages

setup(
    name='LECPython',
    version='1.2.0.2',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # 包含依赖文件的路径
        'LECPythonLib': ['*.pdb','*.dll', '*.so', '*.json'],
    },
    install_requires=[
        'pythonnet==3.0.4',  # 固定安装pythonnet版本为3.0.1。可通过 `pip show pythonnet` 查看当前版本
    ],
    author='xeden3',
    author_email='james@sctmes.com',
    description='LECPython is a Python component developed in C# that enables seamless communication between Python and PLCs. It supports the majority of PLCs available in the market, including those supporting Modbus protocol, Mitsubishi, Siemens, Omron, Rockwell, Keyence PLC, Delta, Beckhoff, Panasonic, Inovance, Fuji, EverSensing, Schneider, and more. This component is standalone, requiring no additional third-party PLC controls for support.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/xeden3/LECPython',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)