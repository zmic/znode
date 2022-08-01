# -*- coding: utf-8 -*-

from setuptools import setup
            
with open('README.md', encoding='utf-8') as f:
    README_TEXT = f.read()
    
'''
Python 3.3 added implicit namespace packages from PEP 420. All that is required to create a native namespace package is that you just omit __init__.py from the namespace package directory.
'''    
setup(
    name='znode',
    version='0.1',
    packages=['znode'],
    python_requires='>=3.3',
    description='',
    long_description = README_TEXT,    
    long_description_content_type='text/markdown',
    url='https://github.com/zmic/znode',
    author='Michael Vanslembrouck',
    license='MIT',     
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
    install_requires=['numpy', 'imageio']
)

      