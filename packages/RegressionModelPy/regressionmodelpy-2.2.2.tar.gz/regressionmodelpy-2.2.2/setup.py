from setuptools import setup, find_packages

setup(
    name='RegressionModelPy',
    version='2.2.2',
    description='A simple linear regression library',
    author='DocJenny',
    author_email='dadoktor8@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'openpyxl'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
