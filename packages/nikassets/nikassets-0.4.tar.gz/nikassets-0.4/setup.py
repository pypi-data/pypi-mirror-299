from setuptools import setup, find_packages

setup(
    name="nikassets",
version="0.4",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.sh', '*.yml'],
        'nikassets.helper': ['assets/*'],
        'nikassets.helper.assets': ['*'],
    },
    author="Nikhil Menghani",
    author_email="nikhil@menghani.com",
    description="A short description of your project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/nikhilmenghani/nikassets",
    install_requires=[
        'setuptools>=72.1.0',
    ],
    entry_points={
        'console_scripts': [
            'nikassets=main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.12',
)