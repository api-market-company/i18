.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/i18.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/i18
    .. image:: https://readthedocs.org/projects/i18/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://i18.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/i18/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/i18

    .. image:: https://img.shields.io/conda/vn/conda-forge/i18.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/i18
    .. image:: https://pepy.tech/badge/i18/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/i18
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/i18

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

.. image:: https://img.shields.io/pypi/v/i18.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/i18/

|

===
i18
===


    Apply nlp tasks into some grammar (i.e. html, yaml, json)

Installation from Pypi
======================

.. code-block:: bash

   pip install i18

Installation from Git
=====================

.. code-block:: bash

   pip install git+https://github.com/api-market-company/i18.git


CLI
=====================

Apply i18 in Batch
+++++++++++++++++++
.. code-block:: bash

   find . -name '*.blade.php' | xargs -P 8 -I {} i18 -s {} 2>"error.txt" | jq -s | jq 'reduce .[] as $item ({}; .en += $item.en | .es += $item.es)' > translation.json


Python
=====================
Consult our `notebooks`_ to learn more. We recommend you starting with `Getting started`_.

.. _notebooks: https://github.com/api-market-company/i18/tree/main/notebooks 
.. _Getting started: https://github.com/api-market-company/i18/blob/main/notebooks/getting-started.ipynb


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.4. For details and usage
information on PyScaffold see https://pyscaffold.org/.
