from setuptools import setup, find_packages

setup(
    name='decorator_collection',
    version='1.0.0',
    description='A collection of basic and advanced Python decorators',
    author='Aiden Metcalfe',
    author_email='avaartshop@outlook.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'jsonschema',
    ],
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown'
)