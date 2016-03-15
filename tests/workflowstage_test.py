'''
Created on Dec 25, 2015

@author: justinpalpant

Copyright 2015 Justin Palpant

This file is part of the Jarvis Lab RNAseq Workflow program.

RNAseq Workflow is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

RNAseq Workflow is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
RNAseq Workflow. If not, see http://www.gnu.org/licenses/.
'''
import unittest
import os
from argparse import Namespace
import fnmatch
import logging

from rnaseqflow.workflow import Workflow, FindFiles, MergeSplitFiles, FastQMCFTrimSolo

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s in %(name)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)


class TestWorkflow(unittest.TestCase):

    FIXTURES = os.path.join(os.path.dirname(__file__),
                            'fixtures')

    INPUTS = os.path.join(FIXTURES, 'input_samples')

    OUTPUTS = os.path.join(FIXTURES, 'output_samples')
    MERGE_FIXTURES = os.path.join(OUTPUTS, 'MergeSplitTest')
    TRIM_FIXTURES = os.path.join(OUTPUTS, 'FastQMCFTrimSoloTest')

    ADAPTER_FILE = os.path.join(FIXTURES, 'test_adapters.fasta')

    def setUp(self):
        self.w = Workflow()
        self.files_to_remove = set()
        self.directories_to_remove = set()

    def tearDown(self):
        for f in self.files_to_remove:
            os.remove(f)

        for d in self.directories_to_remove:
            os.rmdir(d)

    def test_FindFiles(self):
        args = Namespace(root=self.INPUTS, ext='.fastq')

        ff = FindFiles(args)

        foundfiles = set()
        for root, _, files in os.walk(self.INPUTS):
            for basename in files:
                if fnmatch.fnmatch(basename, '*.fastq'):
                    filename = os.path.join(root, basename)
                    foundfiles.add(filename)

        self.assertSetEqual(ff.run(None), foundfiles)

        args = Namespace(root=self.INPUTS, ext='.fastq.gz')

        ff = FindFiles(args)

        foundfiles = set()
        for root, _, files in os.walk(self.INPUTS):
            for basename in files:
                if fnmatch.fnmatch(basename, '*.fastq.gz'):
                    filename = os.path.join(root, basename)
                    foundfiles.add(filename)

        self.assertSetEqual(ff.run(None), foundfiles)

    def test_MergeSplitFiles(self):
        args = Namespace(root=self.INPUTS, ext='.fastq', blocksize=1024)

        merger = MergeSplitFiles(args)

        foundfiles = set()
        for root, _, files in os.walk(self.INPUTS):
            for basename in files:
                if fnmatch.fnmatch(basename, '*.fastq'):
                    filename = os.path.join(root, basename)
                    foundfiles.add(filename)

        merged_files = merger.run(foundfiles)

        self.files_to_remove.update(merged_files)

        merge_fixtures = set()
        for root, _, files in os.walk(self.MERGE_FIXTURES):
            for basename in files:
                if fnmatch.fnmatch(basename, '*.fastq'):
                    filename = os.path.join(root, basename)
                    merge_fixtures.add(filename)

        self.assertSetEqual({os.path.basename(f) for f in merged_files},
                            {os.path.basename(f) for f in merge_fixtures})

        for f in merged_files:
            other_f = next(
                fn for fn in merge_fixtures if os.path.basename(fn) == os.path.basename(f))

            self.assertEqual(os.path.basename(f), os.path.basename(other_f))

            self.assertEqual(open(f, 'rb').read(), open(other_f, 'rb').read(),
                             'Files named {0} do not match'.format(
                os.path.basename(f),
            )
            )

    def test_FastQMCFTrimSolo(self):
        args = Namespace(root=self.INPUTS, ext='.fastq', blocksize=1024,
                         adapters=self.ADAPTER_FILE, fastq_args='-q 30 -l 50')

        finder = FindFiles(args)
        merger = MergeSplitFiles(args)
        trimmer = FastQMCFTrimSolo(args)

        found_files = finder.run(None)
        merged_files = merger.run(found_files)

        self.files_to_remove.update(merged_files)

        trimmed_files = trimmer.run(merged_files)

        self.files_to_remove.update(trimmed_files)

        trim_fixtures = set()
        for root, _, files in os.walk(self.TRIM_FIXTURES):
            for basename in files:
                if fnmatch.fnmatch(basename, '*.fastq'):
                    filename = os.path.join(root, basename)
                    trim_fixtures.add(filename)

        self.assertSetEqual({os.path.basename(f) for f in trimmed_files},
                            {os.path.basename(f) for f in trim_fixtures})

        for f in trimmed_files:
            other_f = next(
                fn for fn in trim_fixtures if os.path.basename(fn) == os.path.basename(f))

            self.assertEqual(os.path.basename(f), os.path.basename(other_f))

            self.assertEqual(open(f, 'rb').read(), open(other_f, 'rb').read(),
                             'Files named {0} do not match'.format(
                os.path.basename(f),
            )
            )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']

    unittest.main()
