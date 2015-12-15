'''
Created on Dec 13, 2015

@author: justinpalpant
'''
#YOU USE SDIST YOU IDIOT
#NOT BDIST
#IF YOU WANT TO CALL pip install rnaseqflow...

from setuptools import setup

setup(name='rnaseqflow',
      version='0.1.0',
      description='RNASeq Preprocessor',
      author='Justin Palpant',
      author_email='justin@palpant.us',
      url='https://github.com/jpalpant/jarvis-lab-rnaseq-flow',
      packages=['rnaseqflow'],
      install_requires=['neurolab'],
      entry_points = {
        'console_scripts': ['rnaseqflow=rnaseqflow.__main__:run_as_executable'],
      }
      )