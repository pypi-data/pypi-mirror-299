

from setuptools import setup, find_packages

setup(
    # Basic package information:
    name='thoughtflow',  
    version='0.0.1',
    packages=find_packages(),  # Automatically find packages in the directory

    # Dependencies:
    install_requires=[
        'numpy>=1.1.1',  
        'pandas>=0.1.1',  
    ], 

    # Metadata for PyPI:
    author          ='James A. Rolfsen',
    author_email    ='james@think.dev', 
	description     ='Short Description',
	url             ='https://github.com/jrolf/rolfdog',    
    long_description='Long Description',
    #long_description=open('README.md').read(),
    # If your README is in markdown:
    #long_description_content_type='text/markdown',
    
    # More classifiers: https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3.12', 
        'License :: OSI Approved :: MIT License',  # Ensure this matches your LICENSE file
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)





