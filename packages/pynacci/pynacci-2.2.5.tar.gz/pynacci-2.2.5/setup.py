# setup.py

from setuptools import setup

setup(
    name='pynacci',  
    version='2.2.5',  
    description='Una librería para trabajar con la serie de Fibonacci',
    long_description=open('README.md', encoding='utf-8').read(),  
    long_description_content_type='text/markdown',  
    author='Pablo Álvaro',  
    author_email='palvaroh2000@gmail.com',  
    license='MIT',  
    py_modules=['pynacci'], 
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent', 
    ],
    python_requires='>=3.6',  
    keywords='fibonacci mathematics generator golden ratio', 
    url='https://github.com/pabblo2000/pynacci',  
)

