from setuptools import setup, find_packages

setup(
    name='jamblaki_skillset',  # Replace with your package’s name
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "openai"
    ],
    author='Jamblaki',  
    author_email='jamblaki@test.com',
    description='A library of skills defined for Jamblaki',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',

)