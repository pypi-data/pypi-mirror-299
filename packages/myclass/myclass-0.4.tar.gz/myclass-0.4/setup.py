from setuptools import setup, find_packages

setup(
    name='myclass',
    version='0.4',
    packages=find_packages(where='dist'),
    package_dir={'': 'dist'},
    install_requires=[],  # Adicione aqui suas dependências se houver
)
