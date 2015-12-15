'''
Created on Dec 13, 2015

@author: justinpalpant
'''

def main():
    print 'Please select the module to run:'
    print '1. Workflow'
    print '0: Quit'
    
    key = int(input('Make a selection: '))
    
    if key == 1:
        print 'Starting a preprocessing workflow...'
        try:
            from PyQt4 import QtGui
        except ImportError:
            #foo = input('PyQt is not installed - install now? (Y/N) ')
            import qt_acquire
            qt_acquire.main()
        else:
            from workflow import Workflow
            w = Workflow()
            w.execute()
    

if __name__ == '__main__':
    main()