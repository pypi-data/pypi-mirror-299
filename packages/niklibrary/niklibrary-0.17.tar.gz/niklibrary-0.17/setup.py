from setuptools import setup, find_packages

setup(
    name="niklibrary",
version="0.17",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.sh', '*.yml'],
        'NikGapps.helper': ['assets/*'],
        'NikGapps.helper.assets': ['*'],
    },
    author="Nikhil Menghani",
    author_email="nikhil@menghani.com",
    description="A short description of your project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/nikhilmenghani/niklibrary",
    install_requires=[
        'colorama>=0.4.6',
        'pytz>=2024.1',
        'pysftp>=0.2.9',
        'PyYAML>=6.0.2',
        'psutil>=6.0.0',
        'setuptools>=72.1.0',
        'requests>=2.32.3',
        'GitPython>=3.1.43',
        'pexpect>=4.9.0',
        'PyGithub>=2.3.0',
        'python-gitlab>=4.7.0',
        'cryptography>=43.0.0',
        'python-dotenv~=1.0.1'
    ],
    entry_points={
        'console_scripts': [
            'niklibrary=main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.12',
)