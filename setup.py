from setuptools import setup, find_packages

setup(
    name='track-cli',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'track=track.main:main',
        ],
    },
    install_requires=[
        'matplotlib',
        'pandas',
        'prettytable',
        'pyarrow'
    ],
)