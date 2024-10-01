import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytorch_visualizer",
    version="0.1.0",
    author="Oluwaseun Ale-Alaba",
    author_email="carmichael8821@gmail.com",
    description="A neural network visualization engine, built for pytorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tony-Ale/pytorch_visualizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    
    install_requires=[
        "numpy>=1.26.4",
        "pygame>=2.6.0",
        "torch>=2.3.1",
    ],
)