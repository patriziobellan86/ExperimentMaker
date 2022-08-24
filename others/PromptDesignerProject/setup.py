from setuptools import find_packages, setup

_REQUIRED = ['openai', 'fpdf', 'Pillow', 'promptdesignerdataset']
_EXTRAS = []
setup(
    name='promptdesigner',
    version='0.0.3',
    packages=find_packages(),
    install_requires=_REQUIRED,
    # extras_require=_EXTRAS,
    url='https://github.com/patriziobellan86/ExperimentMaker',
    license='MIT',
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
        ],
    author='Patrizio Bellan',
    include_package_data=True,
    long_description='Prompt Designer is a component of Experiment Maker. It allows to create prompts to perform in-context learning with GPT-3',
    long_description_content_type='text/x-rst',
    author_email='patrizio.bellan@gmail.com',
    description='Prompt Designer is a component of Experiment Maker. It allows to create prompts to perform in-context learning with GPT-3'
)
