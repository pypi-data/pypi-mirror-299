from setuptools import setup, find_packages

setup(
    name='bald-jonga',
    version='0.1.0',
    description='A Python library that intercepts print statements automatically.',
    author='Mateus Elias',
    author_email='meap@cin.ufpe.br',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
