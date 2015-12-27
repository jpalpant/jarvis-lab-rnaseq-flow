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
import re
import shutil

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
            
        self.buffersize = 128*1024 #bytes
                
    def execute(self):
        '''Allows the user to select a directory and processes all files within
        that directory
        
        This function is the primary function of the Workflow class.  All other
        functions are written as support for this function, at the moment
        '''
        
        if not self.fastq:
            print "fastq-mcf wasn't found - aborting"
            return
        
        folder = str(QtGui.QFileDialog.getExistingDirectory(parent=None, 
                    caption='Select main folder'))
        
        self.find_files(folder, '*.txt')
        print self.files
        self.organize_filenames()
        print self.file_groups

            
    def organize_filenames(self):
        '''Organizes a list of paths by sequence_id, part number, and direction 
           
        This method requires that self.files already be populated.  If it is not,
        this method will not do anything.  If it is, this method sets
        self.file_groups to be a dictionary mapping 
            (sequence_id, dir):{part_num:path, part_num:path,...}
        '''
        #Step 1: Group files by (sequence_id, direction) : [list of files]
        initial_dict = {}
        
        for path in self.files:
            sequence_id = self.get_sequence_id(os.path.basename(path))
            dir = self.get_direction_id(os.path.basename(path))
            
            if not (sequence_id and dir):
                continue
            
            if (sequence_id, dir) in initial_dict:
                initial_dict[(sequence_id, dir)].append(path)
            else:
                initial_dict[(sequence_id, dir)] = [path]
        
        #Step 2: Replace [list of filenames] with a dict {part_num: path}
        #The keys are the same as the previous dict, (sequence_id, dir) as key
        self.file_groups = {}
        for identifier, matched_files in initial_dict.items():
            indexed_map = {}
            for path in matched_files:
                idx = self.get_part_num(os.path.basename(path))
                if idx is not 0:
                    indexed_map[idx] = path
            
            self.file_groups[identifier] = indexed_map
        
    def merge_files(self):
        
        pass
    
    def find_files(self, directory, pattern):
        '''Recursively walk a directory and return filenames matching pattern'''
        self.files = []
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    self.files = self.files + [filename]
    
    def get_sequence_id(self, filename):
        '''Gets the six-letter RNA sequence that identifies the RNAseq file
        
        Returns a six character string that is the ID, or an empty string if no
        identifying sequence is found.'''
        
        p = re.compile('[ACTG]{6}')

        m = p.search(filename)
        if m is None:
            return ''
        else:
            return m.group()
        
        
    def get_direction_id(self, filename):
        '''Gets the direction identifier from an RNAseq filename
        
        A direction identifier is either R01 or R02, indicating a forward or a
        backwards read, respectively.
        '''
        
        p = re.compile('R\d{2}')
        
        m = p.search(filename)
        if m is None:
            return ''
        else:
            return m.group()
        
    def get_part_num(self, filename):
        '''Returns an integer indicating the file part number of the selected
        RNAseq file
        
        RNAseq files, due to their size, are split into many smaller files, each
        of which is given a three digit file part number (e.g. 001, 010).  This
        method returns that part number as an integer.
        
        This requires that there only be one sequence of three digits in the
        filename
        '''
        p = re.compile('\d{3}')
        
        m = p.search(filename)
        if m is None:
            return 0
        else:
            return int(m.group())
        
        
def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    
    window = Workflow()
    window.execute()
    

    
    

if __name__ == '__main__':
    main()