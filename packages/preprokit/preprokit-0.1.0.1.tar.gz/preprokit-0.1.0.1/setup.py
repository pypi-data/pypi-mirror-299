from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='preprokit',
    version='0.1.0.1',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    extra_requires = {
        'pytest': '>8.2',
        'pandas': '>2.1'
    },
    keywords="preprokit, preprocessing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/shammeer-s/preprokit',
    author='Mohammed Shammeer',
    author_email='mohammedshammeer.s@gmail.com',
    description='preprokit is a comprehensive data preprocessing library designed to streamline the data preparation process for data scientists and machine learning practitioners. The library provides an intuitive interface and robust functionalities to handle various preprocessing tasks, ensuring that users can efficiently prepare their datasets for analysis and modeling.'
)