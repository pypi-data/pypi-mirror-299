# setup.py

from setuptools import setup, find_packages

setup(
    name='volkanoban',
    version='0.1.1',
    author='Dr. Volkan OBAN',
    author_email='volkanobn@gmail.com',
    description='A library for data analysis and supervised learning modeling using various powerful machine learning techniques.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'lime',
        'xgboost',
        'lightgbm',
        'catboost',
        'plotly',
        'tabulate',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
