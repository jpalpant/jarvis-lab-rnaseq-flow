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
'''
import workflow
import logging

def main():
    """This method is called when you use python -m {package}
    
    It requires that all the important packages (including Qt, et al.) be
    available in the Python path, correctly installed.
    """
    logging.info('Starting workflow selection')
    
    print 'Please select the module to run:'
    print '1. Workflow'
    print '2. Workflow (dry-run)'
    print '0: Quit'
    
    key = int(input('Make a selection: '))
    
    if key == 1:
        w = workflow.Workflow()
        w.execute()
    elif key == 2:
        w = workflow.Workflow(dummy=True)
        w.execute()
        
    logging.info('Terminating')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()