from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "linear_regression",
        sources=["linear_regression.cpp"],
    )
]

setup(
    name="linear-regression-cpp",
    version="1.0",
    author="Himanshu Rawat",
    author_email="himanshurw56@gmail.com",
    description="A Python package for linear regression using C++",
    ext_modules=cythonize(ext_modules),
)