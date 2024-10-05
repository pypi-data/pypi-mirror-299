from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="winlnks",
    version="0.2.2",
    py_modules=["winlnks"],
    entry_points={
        'console_scripts': [
            'winlnks = winlnks:main',
        ],
    },
    description="Windows LNK File Parser and Creator",
    author="BIG",
    keywords=["lnk", "shortcut", "windows"],
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'colorama',
        'asciitoart',
    ],

    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
