from setuptools import setup, find_packages

setup(
    name="GitAdmin",
    version="0.1.1",
    description="CLI tool for quick GitHub repository management and viewing.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Jared T Ponting",
    author_email="jaredtponting@gmail.com",
    url="https://github.com/JaredTPonting/GHManager",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [
            "GitAdmin=GitAdmin.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">3.6"
)