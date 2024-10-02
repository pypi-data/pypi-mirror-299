from setuptools import setup
from Cython.Build import cythonize

setup(
    name='josecython',
    ext_modules=cythonize("josecython/compiler.py"),
    zip_safe=False,
    version='0.2',
    packages=['josecython'],
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
