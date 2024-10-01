from setuptools import setup, find_packages

setup(
    name='holidaylist',
    version='0.2',
    packages=find_packages(),
    install_requires=['requests'],
    description='A simple Python client for fetching holiday data.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
