'''
Created on Dec 14, 2015

@author: justinpalpant
'''
import subprocess
from subprocess import CalledProcessError
import platform

def main():
    #Try to get the qt things using homebrew
    if platform.system() == 'Darwin':
        get_with_brew('sip')
        get_with_brew('qt')
        get_with_brew('pyqt')
    elif platform.system() == 'Windows':
        get_with_choco('???')
    

def get_with_brew(program):
    try: 
        print 'Beginning installation of {0} with brew'.format(program)
        subprocess.check_output(['brew', 'install', program])
    except CalledProcessError as e:
        print 'CalledProcessError error({0}) during command'.format(e.returncode, e.cmd)
        print 'Error output: {0}'.format(e.output)
    except OSError as e:
        print "OSError error({0}): {1}".format(e.errno, e.strerror)
        print 'Likely brew is not installed'
        print 'Please install Homebrew - http://brew.sh/' 
    else:
        print 'Installation of {0} successful!'.format(program)
        
        
def get_with_choco(program):
    try:
        print 'Beginning installation of {0} with choco'.format(program)
        subprocess.check_output(['choco', 'install', program])
    except CalledProcessError as e:
        print 'CalledProcessError error({0}) during command'.format(e.returncode, e.cmd)
        print 'Error output: {0}'.format(e.output)
    except OSError as e:
        print "OSError error({0}): {1}".format(e.errno, e.strerror)
        print 'Likely Chocolatey is not installed'
        print 'Please install Chocolatey - https://chocolatey.org/' 
    else:
        print 'Installation of {0} successful!'.format(program)


if __name__ == '__main__':
    main()