from setuptools import setup
from Cython.Build import cythonize
import os

def find_py_files(path):
    py_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py") and file != "setup.py":
                py_files.append(os.path.join(root, file))
    return py_files

setup(
    name="cython_build",
    ext_modules=cythonize(
        find_py_files("."),
        compiler_directives={'language_level': "3"},
        build_dir="build"
    ),
    zip_safe=False,
)
