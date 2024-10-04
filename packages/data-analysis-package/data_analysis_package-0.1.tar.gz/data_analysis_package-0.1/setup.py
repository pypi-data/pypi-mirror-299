from setuptools import setup, find_packages

setup(
    name='data_analysis_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'scipy',
    ],
    description='A custom data analysis package.',
    author='Dhavasu',
    license='MIT',
)
