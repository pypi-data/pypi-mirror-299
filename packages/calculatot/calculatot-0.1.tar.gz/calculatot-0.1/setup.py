# setup.py

from setuptools import setup, find_packages

setup(
    name='calculatot',
    version='0.1',
    packages=find_packages(),
    author='Yanu',
    author_email='reazerfreak12@gmail.com',
    description='Kalkulator sederhana untuk penjumlahan, pengurangan, perkalian, dan pembagian.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yanu403/calculatot',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
