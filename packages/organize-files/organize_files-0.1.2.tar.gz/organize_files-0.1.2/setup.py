from setuptools import setup, find_packages

setup(
    name='organize-files',  # This is the package name as seen on PyPI
    version='0.1.2',
    packages=find_packages(),  # This will find the package under the directory
    entry_points={
        'console_scripts': [
            'file-organizer=organize_files.organizer:main',  # Adjusted to underscore
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
