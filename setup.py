from setuptools import Extension, setup
from Cython.Build import cythonize


extensions = [
    Extension("elnino_core", ["elnino_core.py"]),
]


setup(
    name="elnino",
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    ),
)
