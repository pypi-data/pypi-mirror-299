from setuptools import setup, find_packages

setup(
    name="settle.africa",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests", "python-dotenv"],
    test_suite="tests",
    author="AbdulHaleem Nasredeen",
    author_email="sales@settle.africa",
    description="A Python package for interacting with The Settle API",
    url="https://github.com/insolify/settle/python-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
