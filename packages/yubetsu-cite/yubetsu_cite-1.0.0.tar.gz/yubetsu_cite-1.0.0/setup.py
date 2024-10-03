from setuptools import setup, find_packages

setup(
    name='yubetsu_cite',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    author='Yubetsu',
    author_email='info@yubetsu.com',
    description='Yubetsu Cite is a Python tool that simplifies the generation of academic citations in various formats.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yubetsu/yubetsu-cite-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
