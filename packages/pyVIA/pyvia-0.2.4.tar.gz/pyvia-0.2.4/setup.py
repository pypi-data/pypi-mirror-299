import setuptools
import sys
from setuptools import setup
from warnings import warn
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='pyVIA',
    version='0.2.04', ##Sep 30, 2024
    packages=['pyVIA',],
    license='MIT',
    author_email = 'shobana.venkat88@gmail.com',
    url = 'https://github.com/ShobiStassen/VIA',
    setup_requires = ['numpy>=1.17','pybind11'],
    python_requires = ">=3.8",
    install_requires=['pybind11','numpy>=1.17','scipy','pandas>=0.25','hnswlib','igraph','leidenalg>=0.7.0', 'scikit-learn', 'termcolor','pygam', 'matplotlib','scanpy','umap-learn>=0.5.0','phate','datashader', 'scikit-image', 'pillow','wget','gdown','seaborn','pecanpy','holoviews'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
