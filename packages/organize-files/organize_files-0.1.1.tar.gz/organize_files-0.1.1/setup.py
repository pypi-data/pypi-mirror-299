
from setuptools import setup, find_packages

setup(
    name='organize-files',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'file-organizer=file_organizer.organizer:main',
        ],
    },
    install_requires=[],
    description="A simple Python file organizer to categorize files by extension",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shivain2393/file-organizer-python',  
    author='Shivain Sagar',
    author_email='shivain.sagar@gmail.com',
    license='MIT',
)
