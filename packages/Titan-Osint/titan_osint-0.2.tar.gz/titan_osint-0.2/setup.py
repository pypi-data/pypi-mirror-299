from setuptools import setup, find_packages

setup(
    name="Titan_Osint",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pycryptodome",
        "pypiwin32",
        "beautifulsoup4",
	"colorama",
	"pycryptodome",
	"pycryptodomex",
    ],
    author="HeartWay",
    author_email="HeartWay_c.y@proton.me",
    description="A powerful OSINT tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HeartWay-Project/Titan-Multitool",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    entry_points={
        'console_scripts': [
            'search=osint_lib.cli:main',
        ],
    },
)
