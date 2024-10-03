from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pop-autocar3', 
    version='0.0.1',
    author="hanback-lab",
    author_email="lab@hanback.co.kr",
    description="AIoT AutoCar3 library for pop",
    install_requires=[
        "pop-genlib",
        "traitlets",
        "pyaudio",
        "librosa",
        "ipywidgets",
        "opencv-python"
    ],
    long_description=long_description,
    python_requires='>=3.6',
    long_description_content_type="text/markdown",
    packages= find_packages(exclude = ['docs', '__pycache__/']),
    include_package_data=True,   
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
