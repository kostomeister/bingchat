from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bingchat", 
    version="0.1.0",
    author="Hermes Trismegistus",
    author_email="gadersd@gmail.com",
    description="Python interface for Bing AI chatbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gadersd/bingchat",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.7.2",
        "webdriver-manager>=3.8.5"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
