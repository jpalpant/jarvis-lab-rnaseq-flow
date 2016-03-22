.. _ref_cli:

Command Line Interface
======================

While rnaseqflow is a Python package, most users will have need only of the
command line entry point installed by setuptools, call with::
	
	$ rnaseqflow
              
General help is available with the "--help" argument::

	$ rnaseqflow --help
   
Which displays the following output::

   usage: rnaseqflow [--help [{all,stages}]]
                     [--logging {debug,info,warning,error,critical}] [--version]
                     [--stages [STAGES [STAGES ...]]] [--root ROOT] [--ext EXT]
                     [--blocksize BLOCKSIZE] [--adapters ADAPTERS]
                     [--fastq FASTQ] [--fastq_args FASTQ_ARGS] [--quiet]
   
   Preprocess RNAseq files.
   
   optional arguments:
     --help [{all,stages}]
                           Display this help or detailed help on a topic
     --logging {debug,info,warning,error,critical}
                           Logging level (default: info)
     --version             show program's version number and exit
     --stages [STAGES [STAGES ...]]
                           Add stages
     --root ROOT           The root directory to be searched for RNAseq files
     --ext EXT             The file extension to search for
     --blocksize BLOCKSIZE
                           The size of the copy block (in kB) for merge
                           operations
     --adapters ADAPTERS   FastA adapters file to use
     --fastq FASTQ         Location of the fastq-mcf executable
     --fastq_args FASTQ_ARGS
                           Specify arguments to be passed to fastq-mcf
     --quiet               Silence extraneous console output
     
Common Use Case
---------------



     
Arguments
---------

:--help: Display information about the program. ::

   $ rnaseqflow --help all
   $ rnaseqflow --help
   $ rnaseqflow --help stages
   
   **--help all** is identical to **--help**.
   Details on **--help stages** are found below
   
:--logging: Followed by one of the arguments listed, to set the console log level ::

   $ rnaseqflow --logging debug

:--version: Display's the version of the program ::

   $ rnaseqflow --version
   rnaseqflow 0.2.1

:--stages: Asks for one or more stage specifiers which determine the actual workflow
   to be carried out.  Stage specifiers should space-delimited.  No default.
   See *--help stages* for more information. ::
   
   $rnaseqflow --stages 1 2
   
   Finds the stages with the specifiers '1' and '2' (if they exist)
   These stages are then chained together and executed in sequence
   Any informatino needed by these stages not passed at the command line will be requested
   
:--root: Should be followed by a complete path to the directory in which all 
   operations should be carried out. No default. ::
   
   $rnaseqflow --root /Users/myname/Documents/rnaseqdatafolder

:--ext: Should be followed by a file extension (with the dot, e.g. '.fastq') 
   which will be used for all operations.  No default. ::
   
   $rnaseqflow --ext .fastq

:--blocksize: Should be followed by an integer number of kilobytes; specifies 
   the blocksize for use in file operations, such as file concatenation.  Default value 1024 (kB). ::
   
   $rnaseqflow --blocksize 1024

:--adapters: Should be followed by the complete path to the FASTA adapter file to be used by all stages.  No default. ::

   $rnaseqflow --adapters /Users/myname/Documents/rnaseqdatafolder/myadapters.fasta
   
:--fastq_args: Should be followed by a quoted string to pass directly to fastq-mcf, if fastq-mcf will be used.  No default. ::

   $rnaseqflow --fastq_args "-q 30 -l 50"
   
   This will make sure that when fastq-mcf is invoked is is invoked with these arguments.
   Do not use this argument if fastq-mcf will not be used in your program.
   
:--quiet: Does not need to be followed by anything; if true, attempts to silence as much console output as possible.
   Does not affect output from logging, which is controlled with the **--logging** argument.  Default is not quiet. ::
   
   $rnaseqflow --quiet
   
If an argument is needed by any part of the workflow specified with the 
**--stages* argument and it is not provided, or if it has been provided 
incorrectly, the user will be asked to provide that argument before the program
begins.
  
Stages
------
 
 The **--help stages** argument will display information similar to the following ::
 
   $rnaseqflow --help stages
   The following WorkflowStages are available:
   1: FindFiles
       Find files recursively in a folder
   
       Input:
           No input is required for this WorkflowStage
       Output:
           A flat set of file path strings
       Args used:
           * --root: the folder in which to start the search
           * --ext: the file extention to search for
       
   2: MergeSplitFiles
       Merge files by the identifying sequence and direction
   
       Input:
           An iterable of file names to be grouped and merged
       Output:
           A flat set of merged filenames
       Args used:
          * --root: the folder where merged files will be placed
          * --ext: the file extention to be used for the output files
          * --blocksize: number of kilobytes to use as a copy block size
       
   3.0: FastQMCFTrimSolo
       Trim adapter sequences from files using fastq-mcf one file at a time
   
       Input:
           A flat set of files to be passed into fastq-mcf file-by-file
       Output:
           A flat set of trimmed file names
       Args used:
          * --root: the folder where trimmed files will be placed
          * --adapters: the filepath of the fasta adapters file
          * --fastq: the location of the fastq-mcf executable
          * --fastq_args: a string of arguments to pass directly to fastq-mcf
          * --quiet: silence fastq-mcf's output if given
   
       
   3.1: FastQMCFTrimPairs
       Trim adapter sequences from files using fastq-mcf in paired-end mode
   
       Input:
           A flat set of files to be passed into fastq-mcf in pairs
       Output:
           A flat set of trimmed file names
       Args used:
          * --root: the folder where trimmed files will be placed
          * --adapters: the filepath of the fasta adapters file
          * --fastq: the location of the fastq-mcf executable
          * --fastq_args: a string of arguments to pass directly to fastq-mcf
          * --quiet: silence fastq-mcf's output if given
   
In each case, the information about the stage is structured as follows:

- First, the stage's specifier or *spec*, followed by a colon and the stage name.
- Second, a short description of the stage's function
- Third, a description of what the stage produces as output, and what it must receive as input.
  This is useful when chaining stages together - make sure each stage's output is
  compatible with the input of the next stage
- Fourth, a list of arguments that the stage will require.  They need not be 
  provided at the command line, but they can be.  If they are not, the user will
  be asked to provide them before the workflow begins to execute.
  
  
The stage's specifier is what is to be provided to the **--stages** argument when
the executable is called.  With the specifiers above one could call the following command ::

 $rnaseqflow --stages 1 2 3.1

to create a workflow with will recursively find files with a given extension, 
merge any split files found by the first stage using the logic in the 
MergeSplitFiles stage, and trim adapters from the merged files using fastq-mcf passing in merged files one at a time. 

Since no other arguments are provided, the user will be asked to provide all arguments needed
by these stages, such as a file extension, a root directory, an adapter file, etc.

.. note:: Make sure to use the specifiers given by your console's output from **--help stages**, not the specifiers here.  The specifiers in your installation may be different than in those used here.  The **--help stages** argument attempts to intelligently find all possible available stages.

The stage name will be visible in logging statements from that stages.
