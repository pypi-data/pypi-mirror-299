from setuptools import setup, find_packages

setup(
    name="Subha_Package",  # Replace with your package name
    version="0.1.0",
    author="Subha",
    author_email="subhaplatinum@gmail.com",
    description="Basic definitions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/your-repo",  # Replace with your repo
    packages=find_packages(),  # Automatically find your package modules
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
