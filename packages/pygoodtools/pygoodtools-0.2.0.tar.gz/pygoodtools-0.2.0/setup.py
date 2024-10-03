from setuptools import setup, find_packages

setup(
    name='pygoodtools',
    version='0.2.0',
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
    description="""
                This script sets up the 'goodtools' package using setuptools.

                Attributes:
                    name (str): The name of the package.
                    version (str): The version of the package.
                    packages (list): A list of all Python import packages that should be included in the distribution package.
                    install_requires (list): A list of dependencies required by the package.
                    entry_points (dict): A dictionary of entry points, specifying what scripts should be made available to the command line.
                    author (str): The name of the package author.
                    author_email (str): The email address of the package author.
                    description (str): A short description of the package.
                    long_description (str): A detailed description of the package, typically read from a README file.
                    long_description_content_type (str): The format of the long description (e.g., 'text/markdown').
                    url (str): The URL for the package's homepage.
                    classifiers (list): A list of classifiers that provide some additional metadata about the package.
                    python_requires (str): The Python version requirement for the package.
                """,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/massonskyi/goodtools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)