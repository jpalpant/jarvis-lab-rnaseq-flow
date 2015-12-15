'''
Created on Dec 13, 2015

@author: justinpalpant

This file is part of the Jarvis Lab RNAseq Workflow program.

RNAseq Workflow is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

RNAseq Workflow is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
RNAseq Workflow. If not, see http://www.gnu.org/licenses/.

To build this module using pyinstaller, use something like:

pyinstaller --distpath=./{packagefolder}/executables --name={packagename}_{platform} 
        --paths=./{packagefolder} {packagefolder}/__main__.py
        
Called from the project folder (same level as setup.py)
    
--distpath puts the executable somewhere that is NOT /dist
--paths makes sure to include all modules inside rnaseqflow, like the critical
    ones, which does not happen by default
--name makes sure the output name isn't __main__

Make a pip installable package by calling 
    python setup.py sdist --formats=gztar,zip
In order to include the executables in the package, make sure MANIFEST.in 
    includes the line 'recursive-include executables'
For the executable to be called from the path, make sure that entry_points has
    'console_scripts': ['rnaseqflow=rnaseqflow.__main__:run_as_executable']
For the package to be importable, make sure packages=['rnaseqflow'] and that 
    install_requires=[list of package names, as in PyPI]
In order to be able to run python -m rnaseqflow, all Qt packages must be
    pre-installed before calling pip install {tar.gz filename}
'''


from setuptools import setup
import os
from setuptools.command import sdist


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='rnaseqflow',
      version='0.1.0',
      description='RNASeq Preprocessor',
      author='Justin Palpant',
      author_email='justin@palpant.us',
      url='https://github.com/jpalpant/jarvis-lab-rnaseq-flow',
      license = "GPLv3",
      long_description=read('README.md'),
      packages=['rnaseqflow'],
      install_requires=['neurolab'],
      entry_points = {
        'console_scripts': ['rnaseqflow=rnaseqflow.__main__:run_as_executable'],
      },
      include_package_data=True,
      exclude_package_data = { '': ['Test Files/*', 'build/*', 'dist/*', '*.spec'] }
      )