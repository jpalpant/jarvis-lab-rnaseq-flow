.. _ref_cli:

Command Line Interface
======================

While rnaseqflow is a Python package, most users will have need only of the
command line entry point installed by setuptools::
	
	$ rnaseqflow [--help [{all,stages}]]
	             [--logging {debug,info,warning,error,critical}] [--version]
	             [--stages [STAGES [STAGES ...]]] [--root ROOT] [--ext EXT]
	             [--blocksize BLOCKSIZE] [--adapters ADAPTERS]
	             [--fastq FASTQ] [--fastq_args FASTQ_ARGS] [--quiet]
              
General help is available with the "--help" argument::

	$ rnaseqflow --help