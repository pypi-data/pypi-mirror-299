from setuptools import setup
from Cython.Build import cythonize

setup(
    name='josecythoncompiler',
    ext_modules=cythonize("josecythoncompiler/compiler.py"),
    zip_safe=False,
    version='0.1',
    packages=['josecythoncompiler'],
    description='Um projeto simples usando Cython.',
    author='Jose Eduardo',
    author_email='josedumoura@exgmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
