from setuptools import setup, find_packages

setup(
    name='jira-batch-create',
    version='0.1.0',
    author='Szmodry',
    author_email='szmodry@gmail.com',
    description='A package for creating Jira issues in batch',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/szmodry/jira-batch-create',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)
