.. |br| raw:: html

   <br />

################################################
Welcome to fresnote documentation!
################################################

.. toctree::
   :maxdepth: 3

**F**\ lask **res**\ earch **note**\ book (``fresnote``) is a browser-based note-taking application suitable for managing and organizing personal and research projects.

.. image:: images/main_figure.png
   :width: 600
   :alt: Figure 1
   :align: center

|br|

``fresnote`` is based on the following rationale:

* User creates **projects**.
* Each project has one or more **notebooks**.
* Each notebook has one or more **chapters**.
* Each chapter has one or more **sections**.


************************************
Installation
************************************

``fresnote`` uses Flask as back-end and Bootstrap as front-end. To install ``fresnote`` run:

.. code-block:: bash

    pip install fresnote

The development and testing of ``fresnote`` has been done using ``python 3.8`` with `Flask <https://flask.palletsprojects.com/en/2.3.x/>`_ as the only dependency. Regarding the front-end, the CSS and JS libraries for `Bootsrap <https://getbootstrap.com/>`_, `Jquery <https://jquery.com/>`_, `Quill <https://quilljs.com/>`_, `Toastr <https://github.com/CodeSeven/toastr>`_, `Hightlight <https://highlightjs.org/>`_ and `Katex <https://katex.org/>`_ are included in the installation for offline usage. 


################################################
Usage
################################################

************************************
Start fresnote server
************************************

The first time you use ``fresnote``, create an empty ``.ini`` file. For example ``fresnote.ini``. Then follow the steps below everytime you want to use ``fresnote``.

1. In the command line, run:

.. code-block:: bash

   fresnote -c fresnote.ini

The above command will start the Flask server which by default will be listening at port ``5000``. You can specify different port with the ``-p`` option:

.. code-block:: bash

   fresnote -c fresnote.ini -p 8000

2. Open your preferred browser and enter the following url:

.. code-block::

    http://127.0.0.1:5000/


************************************
Create the first project
************************************



