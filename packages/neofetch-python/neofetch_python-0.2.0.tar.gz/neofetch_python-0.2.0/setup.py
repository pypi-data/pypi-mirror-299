from setuptools import setup, find_packages

setup(
    name="neofetch-python",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "colorama",
        "wmi",
    ],
    entry_points={
        "console_scripts": [
            "neofetch=neofetch:run",
        ],
    },
    author="Your Name",
    author_email="firi8228@gmail.com",
    description="A Python implementation of neofetch",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)