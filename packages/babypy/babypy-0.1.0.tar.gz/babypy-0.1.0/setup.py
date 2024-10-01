from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="babypy",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simplified Python library for beginners",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jagath-sajjan/babypy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "pygame",
        "requests",
        "beautifulsoup4",
        "Pillow",
        "nltk",
        "Flask",
        "cryptography",
        "geopy",
        "pyttsx3",
        "qrcode",
        "PyPDF2",
        "selenium",
        "seaborn",
        "scikit-learn",
        "opencv-python",
        "PyAudio",
    ],
)