
from setuptools import find_packages, setup

setup(
    name='milea-demo',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['milea_base>=0.5'],
    author='red-pepper-services',
    author_email='pypi@schiegg.at',
    description='Milea Framework - Milea Demo Module',
    license='MIT',
)
