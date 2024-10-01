from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("cprotobuf.internal", ["cprotobuf/internal.pyx"])
]

setup(
    ext_modules=cythonize(extensions),
)
