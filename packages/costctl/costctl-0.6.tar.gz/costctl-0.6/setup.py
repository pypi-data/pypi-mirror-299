from setuptools import setup, find_packages

setup(
    name='costctl',
    version='0.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'costctl=costctl.main:cli',
        ],
    },
    
)

