# -*- coding: utf-8 -*-

from setuptools import setup
    
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False
            
with open('README.md', encoding='utf-8') as f:
    README_TEXT = f.read()
    
setup(
    name='znode',
    version='0.1',
    packages=['znode'],
    python_requires='>=3.0',
    description='',
    long_description = README_TEXT,    
    long_description_content_type='text/markdown',
    url='https://github.com/zmic/znode',
    author='Michael Vanslembrouck',
    license='MIT',
    package_data = {
        '': [],
    },    
    cmdclass={'bdist_wheel': bdist_wheel},    
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
    install_requires=['numpy', 'imageio']
)

      