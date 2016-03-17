.. _ref_intro:

Introduction
============

rnaseqflow is an open-source Python package written to make preprocessing RNAseq
files more convenient.  It continues to be developed actively and is in the
early stages of development.  It provides the ability to automate and pipeline several operations
that would otherwise be performed manually.

rnaseqflow currently supports the following operations:
   * Discovery of files using recursive directory search with extension matching
   * Merging files using intelligent filename pattern matching
   * Trimming adapter sequences using fastq-mcf, either in single- or paired-end mode
   
These operations may be chained together, with one operation acting on the files found or created
by the previous operation, to create a complete preprocessing workflow.
   
rnaseqflow is composed of two parts: a :ref:`command line interface <ref_cli>` and a
:ref:`Python package <ref_pythonapi>`. See the respective pages for information on how to use
rnaseqflow.

rnaseqflow is constantly expanding and being developed, with more operations to be supported.  To 
request support for a specific operation, request a feature, or report a bug, please create an issue
at the GitHub repository below.  

GitHub repository:
`jarvis-lab-rnaseq-flow <https://github.com/jpalpant/jarvis-lab-rnaseq-flow>`_

Circle CI Status of master branch: |circlecibuild|

.. |circlecibuild| image:: https://circleci.com/gh/jpalpant/jarvis-lab-rnaseq-flow.png?style=shield