# setup.py
from setuptools import setup, find_packages

setup(
    name='refer-agents',
    version = "0.1.2",
    description='ReFeR: Improving Evaluation and Reasoning through Hierarchy of Models',
    author='Yaswanth and Sreevatsa',
    author_email='yasshu.yaswanth@gmail.com',
    url='https://github.com/yaswanth-iitkgp/ReFeR',
    packages=['refer_agents'],
    install_requires=[
        'openai==1.50.2',
        'tqdm==4.66.5',
        'regex==2024.9.11',
        'together==1.3.0',
        'mistralai==1.1.0',
        'asyncio==3.4.3',
        'google-generativeai==0.8.2',
        'groq==0.11.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)