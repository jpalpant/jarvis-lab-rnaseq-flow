'''
Created on Dec 12, 2015

@author: justinpalpant

Copyright 2015 Justin Palpant

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
'''
from PyQt4 import QtGui
import subprocess
import os, fnmatch

class Workflow():
    '''
    Execute a simple series of steps used to preprocess RNAseq files
    '''


    def __init__(self):
        '''
        Initialize a workflow by checking for necessary shell programs
        '''
        
        try: 
            pid = subprocess.Popen(['fastq-mcf','-h'], )
            pid.kill()
        except OSError:
            print 'fastq-mcf not found'
            self.fastq = False
        else:
            print 'Using fastq-mcf'
            self.fastq = True
            
        try: 
            pid = subprocess.Popen(['cat'])
            retcode = pid.kill()
        except OSError:
            print 'cat not found, using Python-based filecopy (expect delays)'
            self.cat = False
        else:
            print 'Using cat'
            self.cat = True
        
        
    def execute(self):
        if not self.fastq:
            print "fastq-mcf wasn't found - aborting"
            return
        import sys
        app = QtGui.QApplication(sys.argv)
        
        folder = str(QtGui.QFileDialog.getExistingDirectory(parent=None, 
                    caption='Select directories'))
        
        files_list = self.find_files(folder, '*.txt')
        
        for f in files_list:
            print f


    def find_files(self, directory, pattern):
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename
    
    

        
        
def main():
    window = Workflow()
    
    window.execute()


if __name__ == '__main__':
    main()