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

def run_as_package():
    """This method is called when you use python -m {package}
    
    It requires that all the important packages (including Qt, et al.) be
    available in the Python path, correctly installed.
    """
    print 'Please select the module to run:'
    print '1. Workflow'
    print '0: Quit'
    
    key = int(input('Make a selection: '))
    
    if key == 1:
        w = workflow.Workflow()
        w.execute()

def run_as_executable():
    """This method is the one put on the PATH by pip install
    
    It assumes that pip install completes successfully, but does not need Qt
    to be installed, or any other package, because it just finds the built
    executable and calls that.  It selects the correct executable for the
    platform and calls it, nothing else.
    
    Coincidentally, that executable is just a built version of this __main__.py,
    run as __name__==__main__ and executing the run_as_package() function above
    
    Funny how things work out, eh?
    """
    import pkg_resources
    import subprocess
    import platform

    print 'Running RNASeqFlow as a compiled executable'
    sys = platform.system()
    
    if sys == 'Windows':
        print 'You have Windows!  Using .exe'
        rm = pkg_resources.ResourceManager()
        win_exe = rm.resource_filename(__name__, "executables/rnaseqflow_win/rnaseqflow_win.exe")
        print 'Executable: ', win_exe
    elif sys == 'Darwin':
        print 'You have Mac!  Using executable'
        rm = pkg_resources.ResourceManager()
        mac_exe = rm.resource_filename(__name__, "executables/rnaseqflow_osx/rnaseqflow_osx")
        print 'Executable: ', mac_exe
        pid = subprocess.Popen([mac_exe])
    else:
        print "Your operating system is not recognizable"
        print ("Cannot run RNASeqFlow as an executable - please install all",
                "necessary modules and run as python -m rnaseqflow")
   

if __name__ == '__main__':
    run_as_package()
    #run_as_executable()