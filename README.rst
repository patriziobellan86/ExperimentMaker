Experiment Maker:
------------------
Experiment Maker is a software developed to reduce the effort and the time spent when designing prompts
for in-context learning and/or combining multiple prompts in an experimental pipeline.
This package allows you to create custom prompts and pipelines to perform in-context learning with GPT-3.

Our system is composed of two complementary components:

- *Prompt Designer*: supports users to design promptss.
    Research project adopted in "Leveraging pre-trained language models for conversational information seeking from text"

- *Pipeline Maker*: helps users in creating a pipeline by combining multiple prompts.
    Pipeline Maker. This tool is part of the Experiment Maker project. It allows to create custom GPT-3 pipeline.
    Adopted in "Assisted Knowledge Graph Building Using Pre-Trained Language Models"
    This tool also allows to integrate custom python scripts to manipulate results.


Demo video:
------------------
See our tool in action https://youtu.be/5e_XAdI2bPQ


Installation:
------------------

You can choose to install the entire program from pypi

- Experiment Maker
    .. code-block:: sh

        pip install experimentmaker


Or, install one of the two components:

- Prompt Designer
    .. code-block:: sh

        pip install promptdesigner

- Pipeline Maker
    .. code-block:: sh

        pip install pipelinemaker

Execute programs:
------------------

- Experiment Maker:

    .. code-block:: python

        from experimentmaker.experimentmaker import LunchEM
        LunchEM()

To lunch one of the components
- Prompt Designer:

    .. code-block:: python

        from promptdesigner.PromptDesigner import LunchPromptDesigner
        LunchPromptDesigner()

- Pipeline Maker:
    .. code-block:: python

        from pipelinemaker.experimentmaker import LunchExperiment
        LunchExperiment()

Custom Modules (filters)
-------------------------
You can test our custom modules (written in python) contained in the folder filters-scripts.
To create your own custom filter, you simply need to write a python class with a method, or a python function, called 'Parse' that accept a single argument.
The results of a step, or the results of the pipeline are passed as dictionary to the method/function.

 For example, consider the following example function.
 This function receives the results (data variable) and clean the answers by removing unused characters from the text.

    .. code-block:: python

         def Parse(self, data):
            def parseitem(item):
                item = item.replace('-', '', 1)
                item = item.replace("'", '', 1)
                item = item.replace("'", '', 1)
                item = item.strip()
                return item

            if type(data) == str:
                return parseitem(data)
            return [parseitem(item) for item in data]
