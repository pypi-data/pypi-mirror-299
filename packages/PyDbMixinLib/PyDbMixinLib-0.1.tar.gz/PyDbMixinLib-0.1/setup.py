from setuptools import setup, find_packages

setup(
    name='PyDbMixinLib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.95.0',
        'sqlalchemy>=1.4',
    ],
    author='ArtemTaU',
    description='A mixin for working with databases in FastAPI using SQLAlchemy.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ArtemTaU/PyDbMixinLib',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Framework :: FastAPI',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6'
)
