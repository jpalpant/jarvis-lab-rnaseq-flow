'''
Created on Dec 25, 2015

@author: justinpalpant
'''
import unittest
from rnaseqflow.workflow import Workflow

class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.w = Workflow(dummy=True)
        self.files = ['blahblah_AAAAAA_blah_R1_001.txt'
                      'blahblah_AAAAAA_blah_R1_002.txt'
                      'blahblah_AAAAAA_blah_R2_001.txt'
                      'blahblah_AAAAAA_blah_R2_002.txt'
                      'blahblah_AAAAAA_blah_R2_003.txt'
                      'blahblah_AAAAAG_blah_R1_001.txt'
                      'blahblah_AAAAAG_blah_R1_002.txt'
                      'blahblah_AAAAAG_blah_R1_003.txt'
                      'blahblah_AAAAAG_blah_R2_001.txt'
                      'blahblah_AAAAAG_blah_R2_002.txt'
                      'blahblah_AAAAAG_blah_R2_003.txt'
                      'blahblah_AAAAAG_blah_R2_004.txt'
                      'blahblah_AAAAAG_blah_R2_005.txt'
                      'blahblah_ACTAGC_blah_R1_001.txt'
                      'blahblah_ACTAGC_blah_R1_002.txt'
                      'blahblah_ACTAGC_blah_R1_003.txt'
                      'blahblah_ACTAGC_blah_R1_004.txt']
        
    def tearDown(self):
        pass


    def test_get_sequence_id(self):
        ids = ['AAAAAA']*5 + ['AAAAAG']*8 + ['ACTAGC']*4
        
        
    
    def test_get_part_num_from_filename(self):
        part_nums = ['001', '002', '001', '002']
        pass
    
    
    def test_get_direction_id_from_filename(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()