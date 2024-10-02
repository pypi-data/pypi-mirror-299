from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("josecythoncompiler.compiler", ["josecythoncompiler/compiler.py"])
]

setup(
    name='josecythoncompiler',
    ext_modules=cythonize(extensions),
    zip_safe=False,
    version='0.2',
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