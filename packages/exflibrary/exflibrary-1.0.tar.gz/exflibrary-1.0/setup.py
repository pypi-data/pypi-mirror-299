# my_package/setup.py
from setuptools import setup, find_packages

setup(
    name='exflibrary',
    version='1.0',
    packages=find_packages(),
    description='A package that downloads a Python script, saving it to a user-accessible directory.',
    author='Adam Johns',
    author_email='rusty128944@gmail.com',
    url='https://github.com/miracledevelop/exflibrary',
    install_requires=[
        'requests',
        'os',
        'subprocess',
        'uuid',
        'ctypes',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
