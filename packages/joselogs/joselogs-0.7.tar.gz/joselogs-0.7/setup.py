# setup.py

from setuptools import setup, find_packages

setup(
    name='joselogs',
    version='0.7',
    packages=find_packages(),
    package_data={
        '': ['pyarmor_runtime/*'],  # Incluir todos os arquivos da pasta pyarmor_runtime
    },
    description='A simple logger with sum functionality',
    author='Jose Eduardo',
    author_email='josedumoura@gmail.com',
    url='https://github.com/seunome/joselogs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
