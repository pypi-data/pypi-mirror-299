from setuptools import setup, find_packages

setup(
    name='qtypi',  # Ensure that this is a unique name
    version='0.1.0',  # Increment the version as you add features
    description='A Python library for quantum state manipulations and quantum gates',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pearl Patel',
    author_email='pearl207@gmail.com',
    url='https://github.com/pearlpatel207/qtypi',  # Update this URL with your GitHub project URL
    packages=find_packages(),
    install_requires=[
        'numpy',  # Ensure that numpy is listed as a requirement
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
    include_package_data=True,  # Include other files like README.md
)
