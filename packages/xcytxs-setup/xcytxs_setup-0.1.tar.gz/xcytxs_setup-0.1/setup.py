from setuptools import setup, find_packages

setup(
    name="xcytxs-setup",  # Package name
    version="0.1",        # Version
    author="xcyt",   # Your name
    author_email="xcytdev@gmail.com",  # Your email
    description="An automated setup tool for configuring services and installing dependencies.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/xcytxs/setup",  # Project repository URL
    packages=find_packages(),  # Find all packages
    install_requires=['pip'],  # Ensure pip is available
    entry_points={
        'console_scripts': [
            'xcytxs-setup = xcytxs_setup.main:main',  # CLI command entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  # Corrected
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
