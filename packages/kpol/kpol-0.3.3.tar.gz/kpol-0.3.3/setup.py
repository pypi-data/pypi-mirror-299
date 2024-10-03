from setuptools import setup, find_packages

setup(
    name="kpol",
    version="0.3.3",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here if any
    author="Dr. Kurian Polachan",
    author_email="kurian.polachan@iiitb.ac.in",
    description="A simple arithmetic operations package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://sites.google.com/view/cdwl/contact",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
