'''
Created on Dec 25, 2015

@author: justinpalpant
'''
import unittest
from rnaseqflow.workflow import Workflow
import os

class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.w = Workflow()
        self.files = ['blahblah_AAAAAA_blah_R01_001.txt'
                      'blahblah_AAAAAA_blah_R01_002.txt'
                      'blahblah_AAAAAA_blah_R02_001.txt'
                      'blahblah_AAAAAA_blah_R02_002.txt'
                      'blahblah_AAAAAA_blah_R02_003.txt'
                      'blahblah_AAAAAG_blah_R01_001.txt'
                      'blahblah_AAAAAG_blah_R01_002.txt'
                      'blahblah_AAAAAG_blah_R01_003.txt'
                      'blahblah_AAAAAG_blah_R02_001.txt'
                      'blahblah_AAAAAG_blah_R02_002.txt'
                      'blahblah_AAAAAG_blah_R02_003.txt'
                      'blahblah_AAAAAG_blah_R02_004.txt'
                      'blahblah_AAAAAG_blah_R02_005.txt'
                      'blahblah_ACTAGC_blah_R01_001.txt'
                      'blahblah_ACTAGC_blah_R01_002.txt'
                      'blahblah_ACTAGC_blah_R01_003.txt'
                      'blahblah_ACTAGC_blah_R01_004.txt']
        
    def tearDown(self):
        pass


    def test_get_sequence_id(self):
        ids = ['AAAAAA']*5 + ['AAAAAG']*8 + ['ACTAGC']*4
        
        for filename, id in zip(self.files, ids):
            self.assertEqual(self.w.get_sequence_id(filename), id)
        
    
    def test_get_part_num_from_filename(self):
        part_nums = ['001', '002', '001', '002']
        pass
    
    
    def test_get_direction_id_from_filename(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()