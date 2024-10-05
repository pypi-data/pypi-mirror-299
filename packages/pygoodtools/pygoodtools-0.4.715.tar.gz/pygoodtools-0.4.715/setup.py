"""
Модуль для настройки пакета 'pygoodtools' с использованием setuptools.
"""

import os
import re
import sys
import subprocess
import platform
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
# from packaging.version import Version

# class CMakeExtension(Extension):
#     def __init__(self, name, sourcedir=''):
#         Extension.__init__(self, name, sources=[])
#         self.sourcedir = os.path.abspath(sourcedir)

# class CMakeBuild(build_ext):
#     def run(self):
#         try:
#             out = subprocess.check_output(['cmake', '--version'])
#         except OSError:
#             raise RuntimeError("CMake must be installed to build the following extensions: " +
#                                ", ".join(e.name for e in self.extensions))

#         if platform.system() == "Windows":
#             cmake_version = Version(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
#             if cmake_version < Version("3.1.0"):
#                 raise RuntimeError("CMake >= 3.1.0 is required on Windows")

#         for ext in self.extensions:
#             self.build_extension(ext)

#     def build_extension(self, ext):
#         extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
#         cmake_args = [
#             '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
#             '-DPYTHON_EXECUTABLE=' + sys.executable
#         ]
#         build_args = []

#         if platform.system() == "Windows":
#             cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE=' + extdir]
#             build_args += ['--config', 'Release']

#         if not os.path.exists(self.build_temp):
#             os.makedirs(self.build_temp)
#         subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp)
#         subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pygoodtools',
    version='0.4.715',
    packages=find_packages(),
    install_requires=[
        # Укажите зависимости вашего проекта здесь
        # Например: 'requests', 'numpy'
    ],
    entry_points={
        'console_scripts': [
            # Укажите консольные скрипты вашего проекта здесь
            # Например: 'goodtools=goodtools.cli:main'
        ],
    },
    author='Massonskyi',
    author_email='massonskyi@icloud.ru',
    description='This script sets up the "goodtools" package using setuptools.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/massonskyi/goodtools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    # ext_modules=[CMakeExtension('pygoodtools')],
    # cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)