from setuptools import setup, find_packages

with open('README.md','r') as f:
    description = f.read()

setup(
    name='autosort_neuron',
    version='0.0.1.1',
    packages=find_packages(),
    install_requires=[
        'spikeinterface==0.95.1',
        'torch==1.12.1',
        'pandas'
    ],
    
    long_description=description,
    long_description_content_type='text/markdown',

)