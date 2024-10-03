from setuptools import setup, find_packages

setup(
    name='simple-cal-1',  # Replace with your package name
    version='0.1.1',   # Initial version
    packages=find_packages(),
    install_requires=[],  # List your package dependencies here
    author='Visa',
    author_email='ahvisa1@gmail.com',
    description='Just a simple calculator class that has basic functionality of calculator',
    long_description=open('README.md').read(),  # Make sure to have a README.md
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/mypackage',  # GitHub or other project URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Specify the Python version
)
