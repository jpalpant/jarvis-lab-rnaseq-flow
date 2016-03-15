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
import readline
readline.parse_and_bind("tab: complete")


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


class WorkflowStage(object):
    """Interfaces for a stage of a Workflow

    Subclasses must override the run method, which takes and verifies arbitrary
    input, processes it, and returns some output
    """
    __metaclass__ = ABCMeta

    logger = logging.getLogger('rnaseqflow.WorkflowStage')

    @abstractmethod
    def run(self, stage_input):
        """Attempt to process the provided input according to the rules of the
        subclass

        Arguments:
            stage_input - an arbitrary input to be processed, usually a list of
                file names or file-like objects.  The subclass must typecheck
                the input as necessary, and define what input it takes

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
    def get_integer_input(cls, message):
        while True:
            try:
                input_value = int(raw_input(message))
            except ValueError:
                cls.logger.warning(
                    "That doesn't appear to be an integer, please try again.")
                continue
            else:
                break

        return input_value

    @classmethod
    def shorthelp(cls):
        helpstrings = []

        helpstrings.append('The following WorkflowItems are available:\n')

        for sub in all_subclasses(cls):
            helpstrings.append(
                '{0}: {1}\n{2}\n'.format(
                    sub.spec, sub.__name__, firstline(sub.__doc__)))

        helpstrings.append('Use "--help stages" for more details')
        return ''.join(helpstrings)

    @classmethod
    def longhelp(cls):
        helpstrings = []

        helpstrings.append('The following WorkflowItems are available:\n')

        for sub in all_subclasses(cls):
            helpstrings.append(
                '{0}: {1}\n    {2}\n'.format(
                    sub.spec, sub.__name__, sub.__doc__))

        return ''.join(helpstrings)


class FindFiles(WorkflowStage):
    """Find files recursively in a folder

    Input:
        No input is required for this WorkflowStage
    Output:
        A flat list of file path strings
    Args used:
        --root: the folder in which to start the search
        --ext: the file extention to search for
    """

    logger = logging.getLogger('rnaseqflow.WorkflowStage.FindFiles')
    spec = '1A'

    def __init__(self, args):
        """Prepare the recursive file finder

        Check that a root directory is provided, or ask for one
        Make sure the search extension is valid
        """

        if not args.root:
            print 'No root directory provided with --root'
            args.root = raw_input('Type the root directory path: ')

        self.root = args.root

        if not os.path.isdir(self.root):
            self.logger.error(
                'Invalid root directory {0} provided, not a '
                'directory'.format(self.root))
            raise TypeError('Invalid root directory')

        if not args.ext:
            print 'No file extension provided with --ext'
            args.ext = raw_input(
                'Enter a file extension (e.g. .fastq, .fastq.gz): ')

        self.ext = args.ext

    def run(self, stage_input):
        """Run the recursive file finding stage

        Arguments:
            stage_input - not used, only for the interface

        Returns:
            A flat list of files found with the correct extension
        """

        self.logger.info('Beginning stage')

        outfiles = []
        for root, _, files in os.walk(self.root):
            for basename in files:
                if fnmatch.fnmatch(basename, "*" + self.ext):
                    filename = os.path.join(root, basename)
                    outfiles.append(filename)

        self.logger.info('Found {0} files'.format(len(outfiles)))

        return outfiles


class MergeSplitFiles(WorkflowStage):
    """Find files in a folder without recursion into subfolders

    Input:
        A flat list of files to be grouped and merged
    Output:
        A flat list of merged filenames
    Args used:
        --root: the folder where merged files will be placed
        --ext: the file extention to be used for the output files
        --blocksize: number of kilobytes to use as a copy block size
    """

    logger = logging.getLogger('rnaseqflow.WorkflowStage.MergeSplitFiles')
    spec = '2'

    def __init__(self, args):
        """Prepare for the merge file stage

        Check for a root directory and a blocksize
        """

        if not args.root:
            print 'No root directory provided with --root'
            args.root = raw_input('Type the root directory path: ')

        self.root = args.root

        if not os.path.isdir(self.root):
            self.logger.error(
                'Invalid root directory {0} provided'
                ', not a directory'.format(self.root))
            raise TypeError('Invalid root directory')

        self.outdir = os.path.join(self.root, 'merged')
        try:
            os.makedirs(self.outdir)
        except OSError:
            if not os.path.isdir(self.outdir):
                raise

        if not args.blocksize:
            print 'No copy operation blocksize set with --blocksize'
            args.blocksize = self.get_integer_input(
                'Enter a blocksize in kB (e.g. 1024): ')

        self.blocksize = args.blocksize

        if not args.ext:
            print 'No file extension provided with --ext'
            args.ext = raw_input(
                'Enter a file extension (e.g. .fastq, .fastq.gz): ')

        self.ext = args.ext

    def run(self, stage_input):
        """Run the merge files operation

        Arguments:
            stage_input - a list of files to be organized and merged

        Returns:
            A flat list of merged files
        """
        self.logger.info('Beginning stage')

        organized = self._organize_files(stage_input)

        merged_files = []

        for i, (fileid, files) in enumerate(organized.iteritems()):
            outfile_name = 'merged_' + \
                fileid[0] + '_' + fileid[1] + self.ext
            outfile_path = os.path.join(self.outdir, outfile_name)

            self.logger.info(
                'Building file {0:d} of {1:d}: {2}'.format(
                    i + 1, len(organized), outfile_path))

            with open(outfile_path, 'wb') as outfile:
                for j, infile in enumerate(files):
                    if j != self._get_part_num(infile):
                        self.logger.error(
                            'Part {0:03d} not found, terminating construction'
                            ' of {1}'.format(j, outfile_path))
                        break

                    self.logger.debug(
                        'Merging file %d of %d: %s', j, max(files.keys()),
                        infile)

                    shutil.copyfileobj(
                        open(infile, 'rb'), outfile, 1024 * self.blocksize)

            merged_files.append(outfile_path)

        self.logger.info('Created {0} merged files'.format(len(merged_files)))

        return merged_files

    def _organize_files(self, files):
        """Organizes a list of paths by sequence_id, part number, and direction

        Arguments:
            files - a flat list of RNAseq file names

        Returns:
           A dictionary - (sequence_id, dir):list(paths in ascending order)
        """

        mapping = {}

        for path in files:
            sequence_id = self._get_sequence_id(os.path.basename(path))
            direction = self._get_direction_id(os.path.basename(path))

            if not (sequence_id and direction):
                self.logger.warning('Discarding file {0} - could not find '
                                    'sequence ID and direction using '
                                    'regular expressions'.format(
                                        os.path.basename(path)))
                continue

            try:
                mapping[(sequence_id, direction)].append(path)
            except KeyError:
                mapping[(sequence_id, direction)] = [path]

        for key, lst in mapping.iteritems():
            mapping[key] = sorted(lst, key=self._get_part_num)

    @staticmethod
    def _get_sequence_id(filename):
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
    def _get_direction_id(filename):
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
    def _get_part_num(filename):
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


class FastQMCFTrimSolo(WorkflowStage):
    """Find files in a folder without recursion into subfolders

    Input:
        A flat list of files to be passed into fastq-mcf one at a time
    Output:
        A flat list of trimmed file names
    Args used:
        --root: the folder where merged files will be placed
        --adapters: the filepath of the fasta adapters file
        --fastq: a string of arguments to pass directly to fastq-mcf
    """

    logger = logging.getLogger('rnaseqflow.WorkflowStage.FastQMCFTrim')
    spec = '3'

    def __init__(self, args):
        """Run all checks needed to create a FastQMCFTrimItem

        Check that fastq-mcf exists in the system
        Specify the fasta adapter file and any arguments
        """

        if not args.root:
            print 'No root directory provided with --root'
            args.root = raw_input('Type the root directory path: ')

        self.root = args.root

        if not os.path.isdir(self.root):
            self.logger.error(
                'Invalid root directory {0} provided'
                ', not a directory'.format(self.root))
            raise TypeError('Invalid root directory')

        self.outdir = os.path.join(self.root, 'trimmed')
        try:
            os.makedirs(self.outdir)
        except OSError:
            if not os.path.isdir(self.outdir):
                raise

        try:
            with open(os.devnull, "w") as fnull:
                subprocess.call(['fastq-mcf'], stdout=fnull, stderr=fnull)
        except OSError:
            self.logger.error(
                'fastq-mcf not found, cannot use FastQMCFTrimSolo')
            raise
        else:
            self.logger.info('fastq-mcf found')

        if not args.adapters:
            print "fasta adapter file not yet specified"
            args.adapters = raw_input(
                "Please specify the .fasta adapter file location")

        self.adapters = args.adapters

        if not args.fastq_args:
            print "fastq arguments not yet specified"
            args.fasta_args = raw_input(
                "Please specify an optional .fastq argument string (e.g. '-q 30 -x 0.5'): ")

        self.fastq_args = args.fastq_args

    def run(self, stage_input):
        """Trim files one at a time using fastq-mcf

        Arguments:
            stage_input - a flat list of file names

        Returns:
            A flat list of trimmed file names
        """

        self.logger.info('Beginning stage')
        trimmed_files = []

        for i, fname in enumerate(stage_input):
            outfile_name = 'trimmed_' + os.path.basename(fname)
            outfile_path = os.path.join(self.outdir, outfile_name)
            cmd = ['fastq-mcf', self.adapters, fname] + \
                self.fastq_args.split() + ['-o', outfile_path]

            self.logger.info(
                'Stripping adapters for file %d of %d', i + 1,
                len(self.merged_files))

            self.logger.debug('Calling %s', str(cmd))

            subprocess.call(cmd)

            trimmed_files.append(outfile_path)

        self.logger.info('Trimmed {0} files'.format(len(trimmed_files)))

        return trimmed_files
