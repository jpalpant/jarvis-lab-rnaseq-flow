"""
Created on Dec 12, 2015

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
"""

import logging
import subprocess
import os
import fnmatch
import re
import shutil
import sys
from abc import ABCMeta, abstractmethod, abstractproperty


def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def firstline(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    return lines[0]


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]


class Workflow(object):
    """
    Execute a simple series of steps used to preprocess RNAseq files
    """
    logger = logging.getLogger('rnaseqflow.Workflow')

    def __init__(self):
        """
        Initialize a workflow by checking for necessary shell programs
        """

        self.items = []

        try:
            with open(os.devnull, "w") as fnull:
                subprocess.call(['fastq-mcf'], stdout=fnull, stderr=fnull)
        except OSError:
            self.fastq = False
        else:
            self.logger.info('Using fastq-mcf')
            self.fastq = True

        self.buffersize = 1024 * 1024  # in bytes; aka 128kB
        self.extension = '.fastq.gz'

    def append(self, item):
        """Add a WorkflowStage to the workflow

        Arguments:
            item - a WorkflowStage to execute
        """

        self.items.append(item)

    def insert(self, idx, item):
        """Insert a WorkflowStage into the workflow

        Arguments:
            item - a WorkflowStage to execute
        """

        self.items.insert(idx, item)

    def execute(self):
        """Allows the user to select a directory and processes all files within
        that directory

        This function is the primary function of the Workflow class.  All other
        functions are written as support for this function, at the moment
        """

        current_input = None
        for item in self.items:
            next_input = item.execute(current_input)
            current_input = next_input

        if not self.fastq:
            self.logger.error("fastq-mcf wasn't found - terminating execution")
            if not self.dummy:
                return

        self.out_folder = os.path.join(self.root_folder, 'preprocessed')

        self.adapters = str(QFileDialog.getOpenFileName(parent=None,
                                                        caption='Select adapters file'))

        try:
            os.makedirs(self.out_folder)
        except OSError:
            if not os.path.isdir(self.out_folder):
                raise

        print 'Enter the minimum quality q for fastq-mcf'
        self.min_q = self.get_integer_input()

        print 'Enter the value of the -l flag: '
        self.l_value = self.get_integer_input()

        self.logger.info('Finding all %s files', self.extension)
        self.find_files(self.root_folder, '*' + self.extension)
        self.logger.debug('Files found: %s', str(self.files))

        self.logger.info('Organizing files')
        self.organize_filenames()
        self.logger.debug('Files organized: %s', str(self.file_groups))

        self.logger.info('Merging files by group')
        self.merge_files()
        self.logger.debug('Merged files: %s', str(self.merged_files))

        self.logger.info('Stripping adapters from merged files')
        self.strip_files()
        self.logger.debug('Stripped files: %s', str(self.stripped_files))

    def organize_filenames(self):
        """Organizes a list of paths by sequence_id, part number, and direction

        This method requires that self.files already be populated.  If it is
        not, this method will not do anything.  If it is, this method sets
        self.file_groups to be a dictionary mapping
            (sequence_id, dir):{part_num:path, part_num:path,...}
        """

        # Step 1: Group files by (sequence_id, direction) : [list of files]
        initial_dict = {}

        for path in self.files:
            sequence_id = Workflow.get_sequence_id(os.path.basename(path))
            direction = Workflow.get_direction_id(os.path.basename(path))

            if not (sequence_id and direction):
                continue

            if (sequence_id, direction) in initial_dict:
                initial_dict[(sequence_id, direction)].append(path)
            else:
                initial_dict[(sequence_id, direction)] = [path]

        # Step 2: Replace [list of filenames] with a dict {part_num: path}
        # The keys are the same as the previous dict, (sequence_id, dir) as key
        self.file_groups = {}
        for identifier, matched_files in initial_dict.items():
            indexed_map = {}
            for path in matched_files:
                idx = Workflow.get_part_num(os.path.basename(path))
                if idx is not 0:
                    indexed_map[idx] = path

            if indexed_map:
                self.file_groups[identifier] = indexed_map

    def merge_files(self):
        """Merges all files in self.file_groups by group and places them in the
        root directory self.out_folder"""
        self.merged_files = []

        for i, (fileid, files) in enumerate(self.file_groups.items()):
            outfile_name = 'merged_' + \
                fileid[0] + '_' + fileid[1] + self.extension
            outfile_path = os.path.join(self.out_folder, outfile_name)
            self.logger.info(
                'Building file %d of %d: %s', i + 1, len(self.file_groups),
                outfile_path)
            with open(outfile_path, 'wb') as outfile:
                for j in range(1, max(files.keys()) + 1):
                    try:
                        infile = files[j]
                    except KeyError:
                        self.logger.error(
                            'Part %03d not found, terminating construction'
                            ' of %s', j, outfile_path)
                        break

                    self.logger.debug(
                        'Merging file %d of %d: %s', j, max(files.keys()),
                        infile)

                    if self.dummy:
                        outfile.write('Dummy {:03d}\n'.format(j))
                    else:
                        shutil.copyfileobj(
                            open(infile, 'rb'), outfile, self.buffersize)

            self.merged_files.append(outfile_path)

    def strip_files(self):
        self.stripped_files = []

        for i, fname in enumerate(self.merged_files):
            outfile_name = 'trimmed_' + os.path.basename(fname)
            outfile_path = os.path.join(os.path.dirname(fname), outfile_name)
            cmd = ['fastq-mcf', self.adapters, fname, '-q',
                   str(self.min_q), '-l', str(self.l_value), '-x', '0.5', '-o', outfile_path]
            self.logger.info(
                'Stripping adapters for file %d of %d', i + 1, len(self.merged_files))
            self.logger.debug('Calling %s', str(cmd))

            if self.dummy:
                self.logger.info('Creating dummy file %s', outfile_name)
                Workflow.touch(outfile_path)
            else:
                subprocess.call(cmd)

            if os.path.isfile(outfile_path):
                self.stripped_files.append(outfile_path)

    def find_files(self, directory, pattern):
        """Recursively walk a directory and return filenames matching pattern"""
        self.files = []
        for root, _, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    self.files.append(filename)

    @staticmethod
    def touch(path):
        with open(path, 'a'):
            os.utime(path, None)

    @staticmethod
    def get_sequence_id(filename):
        """Gets the six-letter RNA sequence that identifies the RNAseq file

        Returns a six character string that is the ID, or an empty string if no
        identifying sequence is found."""

        p = re.compile('.*[ACTG]{6}')

        m = p.search(filename)
        if m is None:
            return ''
        else:
            return m.group()

    @staticmethod
    def get_direction_id(filename):
        """Gets the direction identifier from an RNAseq filename

        A direction identifier is either R01 or R02, indicating a forward or a
        backwards read, respectively.
        """

        p = re.compile('R\d{1}')

        m = p.search(filename)
        if m is None:
            return ''
        else:
            return m.group()

    @staticmethod
    def get_part_num(filename):
        """Returns an integer indicating the file part number of the selected
        RNAseq file

        RNAseq files, due to their size, are split into many smaller files, each
        of which is given a three digit file part number (e.g. 001, 010).  This
        method returns that part number as an integer.

        This requires that there only be one sequence of three digits in the
        filename
        """
        p = re.compile('_\d{3}')

        m = p.search(filename)
        if m is None:
            return 0
        else:
            text = m.group()
            return int(text[1:])

    def get_integer_input(self):
        while True:
            try:
                input_value = int(raw_input('Please enter an integer: '))
            except ValueError:
                self.logger.warning(
                    "That doesn't appear to be an integer, please try again.")
                continue
            else:
                break

        return input_value


class WorkflowStage(object):
    """Interfaces for a stage of a Workflow

    Subclasses must override the run method, which takes and verifies arbitrary
    input, processes it, and returns some output
    """
    __metaclass__ = ABCMeta

    logger = logging.getLogger('rnaseqflow.WorkflowStage')

    @abstractmethod
    def run(self, input):
        """Attempt to process the provided input according to the rules of the
        subclass

        Arguments:
            input - an arbitrary input to be processed, usually a list of file
                names or file-like objects.  The subclass must typecheck the
                input as necessary, and define what input it takes

        Returns:
            output - the results of the processing of this workflow item
        """
        pass

    @abstractproperty
    def spec(self):
        """Abstract class property, override with @classmethod

        Used by the help method to specify available WorkflowItems
        """

        pass

    @classmethod
    def shorthelp(cls):
        helpstrings = []

        helpstrings.append('The following WorkflowItems are available:\n')

        for sub in all_subclasses(cls):
            helpstrings.append(
                '{0}: {1}\n{2}\n'.format(sub.spec, sub.__name__, firstline(sub.__doc__)))

        helpstrings.append('Use "--help stages" for more details')
        return ''.join(helpstrings)

    @classmethod
    def longhelp(cls):
        helpstrings = []

        helpstrings.append('The following WorkflowItems are available:\n')

        for sub in all_subclasses(cls):
            helpstrings.append(
                '{0}: {1}\n    {2}\n'.format(sub.spec, sub.__name__, sub.__doc__))

        return ''.join(helpstrings)


class FindFilesRecursive(WorkflowStage):
    """Find files recursively in a folder

    Input:
        No input is required for this WorkflowStage
    Output:
        A flat list of file path strings
    Args used:
        --root: the folder in which to start the search
        --ext: the file extention to search for
    """

    logger = logging.getLogger('rnaseqflow.WorkflowStage.FindFilesFlatItem')
    spec = '1A'


class FindFilesFlat(WorkflowStage):
    """Find files in a folder without recursion into subfolders

    Input:
        No input is required for this WorkflowStage
    Output:
        A flat list of file path strings
    Args used:
        --root: the folder in which to start the search
        --ext: the file extention to search for
    """

    logger = logging.getLogger(
        'rnaseqflow.WorkflowStage.FindFilesRecursiveItem')
    spec = '1B'


class MergeSplitFiles(WorkflowStage):
    """Find files in a folder without recursion into subfolders

    Input:
        A flat list of files to be grouped and merged
    Output:
        A flat list of merged filenames
    Args used:
        --blocksize: number of kilobytes to use as a copy block size
    """

    logger = logging.getLogger('rnaseqflow.WorkflowStage.MergeSplitFilesItem')
    spec = '2'


class FastQMCFTrimSolo(WorkflowStage):
    """Find files in a folder without recursion into subfolders

    Input:
        A flat list of files to be passed into fastq-mcf one at a time
    Output:
        A flat list of trimmed file names
    Args used:
        --adapters: the filepath of the fasta adapters file
        --fastq: a string of arguments to pass directly to fastq-mcf
    """

    logger = logging.getLogger('rnaseqflow.WorkflowStage.FastQMCFTrimItem')
    spec = '3'

    def __init__(self, args):
        """Run all checks needed to create a FastQMCFTrimItem

        Check that fastq-mcf exists in the system
        Specify the fasta adapter file and any arguments
        """

        try:
            with open(os.devnull, "w") as fnull:
                subprocess.call([args.fastq], stdout=fnull, stderr=fnull)
        except OSError:
            self.logger.error(
                'fastq-mcf not found, cannot use FastQMCFTrimItem')
            raise
        else:
            self.logger.info('fastq-mcf found')
            self.fastq_command = args.fastq

        if not args.adapters:
            print "fasta adapter file not yet specified"
            self.adapters = raw_input(
                "Please specify the .fasta adapter file location")
        else:
            self.adapters = args.adapters

        if not args.fastq_args:
            print "fastq arguments not yet specified"
            self.fasta_args = raw_input(
                "Please specify an optional .fastq argument string (e.g. '-q 30 -x 0.5'): ")
        else:
            self.fastq_args = args.fastq_args


def main():
    pass

if __name__ == '__main__':
    main()
