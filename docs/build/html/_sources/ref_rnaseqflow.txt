====================
Python Documentation
====================

rnaseqflow is composed of three modules:

:ref:`__main__ <rnaseqflow.__main__>`
=====================================
Provides the entry point for the executable in the function **main()** and argument parsing in **opts()**

.. toctree::
   :maxdepth: 2
   
   modules/module_main

:ref:`workflow <rnaseqflow.workflow>`
=====================================
Provides several classes that are used to execute a series of preprocessing steps on RNAseq data

.. toctree::
   :maxdepth: 2
   
   modules/module_workflow

:ref:`cliutils <rnaseqflow.cliutils>`
=====================================
Provides a class that can intelligently ask the user to provide arguments if the required arguments were not provided at the command line

.. toctree::
   :maxdepth: 2
   
   modules/module_cliutils

    