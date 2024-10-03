from setuptools import setup, find_packages

setup(
    name='TMail',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'bs4'
    ],
    description='Disposable Temporary Email',
    author='Errucha',
    url='https://github.com/mbulung/TMail',
)

