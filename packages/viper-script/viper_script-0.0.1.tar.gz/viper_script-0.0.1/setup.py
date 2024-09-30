# setup.py

from setuptools import setup, find_packages

setup(
    name='viper_script',
    version='0.0.1',
    description='A New Fun experience',
    author='Yuvraj Dhiman',
    author_email='yuvraj.dhiman2003@gmail.com',
    url='https://github.com/yuvraj-dhiman/T.U.R.B.O',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'parsel_tongue=parsel_tongue.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
