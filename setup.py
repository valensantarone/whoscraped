from setuptools import setup, find_packages

setup(
    name="whoscraped",
    version="0.1.0",
    author="Valko",
    author_email="valensantarone@gmail.com",
    description="Scrape football data from WhoScored",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.github.com/valensantarone/whoscraped",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "beautifulsoup4",
        "pandas"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)