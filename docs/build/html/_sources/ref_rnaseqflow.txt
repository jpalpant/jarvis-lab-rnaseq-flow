====================
Python Documentation
====================

rnaseqflow is composed of three modules - **__main__**, **workflow**, and **cliutils**

* **__main__** provides the console entry point for the program for the user. 
* **workflow** provides several classes that are used to execute a series of preprocessing steps on RNAseq data
* **cliutils** provides a class that can intelligently ask the user to provide arguments if the required arguments were not provided at the command line

``rnaseqflow.__main__``
=======================
.. autofunction:: rnaseqflow.__main__.main
.. autofunction:: rnaseqflow.__main__.opts

``rnaseqflow.workflow``
=======================
.. autoclass:: rnaseqflow.workflow.Workflow
    :members:
    :private-members:
    
.. autoclass:: rnaseqflow.workflow.WorkflowStage
    :members:
    :private-members:

.. autoclass:: rnaseqflow.workflow.FindFiles
    :members:
    :private-members:
    :show-inheritance:
    
.. autoclass:: rnaseqflow.workflow.MergeSplitFiles
    :members:
    :private-members:
    :show-inheritance:

.. autoclass:: rnaseqflow.workflow.FastQMCFTrimSolo
    :members:
    :private-members:
    :show-inheritance:
    
.. autoclass:: rnaseqflow.workflow.FastQMCFTrimPairs
    :members:
    :private-members:
    :show-inheritance: 
      
``rnaseqflow.cliutils``
=======================
.. autoclass:: rnaseqflow.cliutils.ArgFiller
    :members:
    :private-members:
    
.. autofunction:: rnaseqflow.cliutils.all_subclasses
.. autofunction:: rnaseqflow.cliutils.trim
.. autofunction:: rnaseqflow.cliutils.firstline

    