from setuptools import find_packages, setup
import os

def read(fname):
    """
    Utility function to read the README file. Used for the long_description.
    :param fname:
    :return:
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

_REQUIRED = ['Pillow', 'openai',  'promptdesignerdataset']
_EXTRAS = []
setup(
    name='pipelinemaker',
    version='0.0.4',
    packages=find_packages(),
    install_requires=_REQUIRED,
    # extras_require=_EXTRAS,
    python_requires='!=2.7, >=3.5.*',
    url='https://github.com/patriziobellan86/ExperimentMaker',
    license='MIT',
    classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",

            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Information Technology",

            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",

            "Topic :: Scientific/Engineering",
            "Topic :: Utilities",
        ],
keywords=["huggingface", "PET", "dataset", "benchmark", "process extraction from text",
              "natural language processing", "nlp", "business process management", "bpm"],
    author='Patrizio Bellan',
    include_package_data=True,
    long_description=read("README.rst"),
    long_description_content_type='text/x-rst',
    author_email='patrizio.bellan@gmail.com',
    description='Pipeline Maker. This tool is part of the Experiment Maker project. It allows to create custom GPT-3 pipeline'
)
