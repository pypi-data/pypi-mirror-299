from setuptools import setup, find_packages

setup(
    name='jupsolhelp',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests', 
    ],
    entry_points={
        'console_scripts': [
            'jupsolhelp=jupsolhelp.helper:init_helper',
        ],
    },
)
