'''
Created on Mar 15, 2016

@author: justinpalpant
'''
import unittest
import mock
import os
from argparse import Namespace

from rnaseqflow.cliutils import ArgFiller, trim, firstline, all_subclasses


class ArgFillerTest(unittest.TestCase):
    """Tests for functions and classes in rnaseqflow.cliutils

    Long docstring for testing
    """

    FIXTURES = os.path.join(os.path.dirname(__file__),
                            'fixtures')

    ADAPTER_FILE = os.path.join(FIXTURES, 'test_adapters.fasta')

    def setUp(self):
        self.empty_args = Namespace()
        self.af = ArgFiller(self.empty_args)
        pass

    def tearDown(self):
        pass

    def test_fill_root(self):
        with mock.patch('__builtin__.raw_input', return_value=self.FIXTURES):
            self.af.fill(['root'])

        self.assertEqual(self.empty_args.root, self.FIXTURES)

        with mock.patch('__builtin__.raw_input', return_value='junk'):
            self.af.fill(['root'])

        self.assertEqual(self.empty_args.root, self.FIXTURES)

    def test_fill_ext(self):
        with mock.patch('__builtin__.raw_input', return_value='.fastq'):
            self.af.fill(['ext'])

        self.assertEqual(self.empty_args.ext, '.fastq')

        with mock.patch('__builtin__.raw_input', return_value='junk'):
            self.af.fill(['ext'])

        self.assertEqual(self.empty_args.ext, '.fastq')

    def test_fill_blocksize(self):
        with mock.patch('__builtin__.raw_input', return_value='100'):
            self.af.fill(['blocksize'])

        self.assertEqual(self.empty_args.blocksize, 100)

        with mock.patch('__builtin__.raw_input', return_value='junk'):
            self.af.fill(['blocksize'])

        self.assertEqual(self.empty_args.blocksize, 100)

    def test_fill_adapters(self):
        with mock.patch('__builtin__.raw_input', return_value=self.ADAPTER_FILE):
            self.af.fill(['adapters'])

        self.assertEqual(self.empty_args.adapters, self.ADAPTER_FILE)

        with mock.patch('__builtin__.raw_input', return_value='junk'):
            self.af.fill(['adapters'])

        self.assertEqual(self.empty_args.adapters, self.ADAPTER_FILE)

    def test_fill_fastq_args(self):
        with mock.patch('__builtin__.raw_input', return_value='-q 30'):
            self.af.fill(['fastq_args'])

        self.assertEqual(self.empty_args.fastq_args, '-q 30')

        with mock.patch('__builtin__.raw_input', return_value='junk'):
            self.af.fill(['fastq_args'])

        self.assertEqual(self.empty_args.fastq_args, '-q 30')

    def test_fill_quiet(self):
        self.af.fill(['quiet'])

        self.assertFalse(self.empty_args.quiet)

        self.empty_args.quiet = True
        self.af.fill(['quiet'])

        self.assertTrue(self.empty_args.quiet)

    def test_trim(self):
        correct_docstring = "Tests for functions and classes in " \
            "rnaseqflow.cliutils\n\n" \
            "Long docstring for testing"

        self.assertEqual(trim(self.__doc__), correct_docstring)
        self.assertEqual(trim(None), '')

    def test_firstline(self):
        correct_firstline = "Tests for functions and classes in rnaseqflow.cliutils"

        self.assertEqual(firstline(self.__doc__), correct_firstline)
        self.assertEqual(firstline(None), '')

    def test_all_subclasses(self):

        class Base(object):
            pass

        self.assertListEqual(all_subclasses(Base), [])

        class Inherited1(Base):
            pass

        self.assertListEqual(all_subclasses(Base), [Inherited1])

        class Inherited2(Base):
            pass

        self.assertListEqual(all_subclasses(Base), [Inherited1, Inherited2])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
