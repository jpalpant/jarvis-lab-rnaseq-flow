'''
Created on Dec 25, 2015

@author: justinpalpant
'''
import unittest
from rnaseqflow.workflow import Workflow


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.w = Workflow()
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
