from setuptools import setup, find_packages
from setuptools import setup
import os

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

setup(
  name = 'AutoPrep',         
  packages = ['AutoPrep'],   
  version =  'v3.0.0',      
  license='MIT',        
  description = 'AutoPrep is an automated preprocessing pipeline with univariate anomaly marking', 
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Jörg Adelhelm',                  
  author_email = 'adeljoe@gmx.de', 
  url = 'https://github.com/JAdelhelm/AutoPrepn', 

  keywords = ["anomaly-detection", "preprocessing", "automated", "automated-preprocessing", "cleaning"],

  install_requires=[          
          'scikit-learn',
          'numpy',
          'pandas',
          "category_encoders",
          "bitstring"
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',   
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',    
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
