from setuptools import setup, find_packages

setup(
    name="dolby",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # List any dependencies here
    author="credrole",
    author_email="credrole@gmail.com",
    description="The most advanced virtual assistant for your operating system",
    long_description=open("README.md").read(),  # If you have a README
    long_description_content_type="text/markdown",
    url="https://github.com/credrole/dolby",  # Update with your URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust as necessary
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
