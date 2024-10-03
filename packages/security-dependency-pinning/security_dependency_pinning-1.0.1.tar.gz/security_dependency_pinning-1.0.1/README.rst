security_dependency_pinning
===========================


Version v1.0.1 as of 2024-10-02 see `Changelog`_

|build_badge| |codeql| |license| |jupyter| |pypi|
|pypi-downloads| |black| |codecov| |cc_maintain| |cc_issues| |cc_coverage| |snyk|



.. |build_badge| image:: https://github.com/bitranox/security_dependency_pinning/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/bitranox/security_dependency_pinning/actions/workflows/python-package.yml


.. |codeql| image:: https://github.com/bitranox/security_dependency_pinning/actions/workflows/codeql-analysis.yml/badge.svg?event=push
   :target: https://github.com//bitranox/security_dependency_pinning/actions/workflows/codeql-analysis.yml

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/bitranox/security_dependency_pinning/master?filepath=security_dependency_pinning.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/security-dependency-pinning?label=PyPI%20Package
   :target: https://badge.fury.io/py/security_dependency_pinning

.. badge until 2023-10-08:
.. https://img.shields.io/codecov/c/github/bitranox/security_dependency_pinning
.. badge from 2023-10-08:
.. |codecov| image:: https://codecov.io/gh/bitranox/security_dependency_pinning/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/security_dependency_pinning

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/security_dependency_pinning?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/security_dependency_pinning/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/security_dependency_pinning?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/security_dependency_pinning/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/security_dependency_pinning?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/security_dependency_pinning/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://snyk.io/test/github/bitranox/security_dependency_pinning/badge.svg
   :target: https://snyk.io/test/github/bitranox/security_dependency_pinning

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/security-dependency-pinning
   :target: https://pypi.org/project/security-dependency-pinning/
   :alt: PyPI - Downloads

A repository dedicated to maintaining a secure, stable environment by pinning critical library versions to protect against vulnerabilities and ensure compatibility.

Purpose
-------
The repository is specifically designed to:

- **Ensure a Secure Environment**: By pinning specific versions of critical libraries, the repository helps in safeguarding against potential security threats by avoiding the use of versions known to have vulnerabilities.

- **Maintain Stability**: Stability in the software environment is ensured by using tested and proven versions of libraries, reducing the risk of crashes or errors due to incompatible library updates.

- **Prevent Compatibility Issues**: Compatibility among various libraries and dependencies is crucial for the smooth operation of software projects. Pinning versions help in avoiding conflicts that might arise from updates in dependencies.

- **Protect Against Vulnerabilities**: The focus on pinning critical libraries is also to protect the software from vulnerabilities that could be exploited if newer, untested versions of the libraries are used.

Key Considerations
------------------
- The practice of pinning should be applied judiciously, focusing on libraries that are critical for security and operational stability.

- Regular review of pinned versions is necessary to ensure that updates addressing security vulnerabilities are incorporated in a timely manner, without compromising the stability of the software environment.

- Coordination among team members is essential to manage the pinned versions effectively and to ensure that all aspects of the software's dependencies are considered.

Conclusion
----------
Security dependency pinning is a foundational practice in maintaining the integrity, security, and reliability of software projects. By adhering to this practice, developers can significantly reduce the risk of introducing security vulnerabilities and compatibility issues into their projects.

----

automated tests, Github Actions, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.8.0 or newer

tested on recent linux with python 3.8, 3.9, 3.10, 3.11, 3.12, pypy-3.9, pypy-3.10, graalpy-24.1 - architectures: amd64

`100% code coverage <https://codeclimate.com/github/bitranox/security_dependency_pinning/test_coverage>`_, flake8 style checking ,mypy static type checking ,tested under `Linux, macOS, Windows <https://github.com/bitranox/security_dependency_pinning/actions/workflows/python-package.yml>`_, automatic daily builds and monitoring

----

- `Try it Online`_
- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/security_dependency_pinning/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/security_dependency_pinning/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/security_dependency_pinning/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/{{rst_include.
repository_slug}}/master?filepath=security_dependency_pinning.ipynb>`_

Usage
-----------

Incorporate the ``security_dependency_pinning`` library into your project's requirements. As a result, the versions of the following libraries will be explicitly specified and maintained:

.. code-block:: bash

    ## Project Requirements
    click
    toml

    ## security pinnings
    # not directly required, pinned to avoid vulnerability CVE-2023-37920
    certifi>=2024.2.2
    # not directly required, pinned to avoid vulnerability CVE-2023-5752
    pip>=24.0
    # not directly required, pinned to avoid vulnerability CVE-2023-43804, CVE-2023-45803
    urllib3>=2.2.0
    # not directly required, pinned to avoid vulnerability CVE-2023-27522
    # uwsgi not available on windows
    # uwsgi not available on graalpy (reports python 3.11 for graalpy 24.1 )
    uwsgi>=2.0.21 ; sys_platform != 'win32' and platform_python_implementation == 'CPython'
    # not directly required, pinned to avoid vulnerability CVE-2023-27522
    zipp>=3.19.1
    # not directly required, pinned to avoid Always-Incorrect Control Flow Implementation
    requests>=2.32.0

Usage from Commandline
------------------------

.. code-block::

   Usage: security_dependency_pinning [OPTIONS] COMMAND [ARGS]...

     A repository dedicated to maintaining a secure, stable environment by
     pinning critical library versions

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     info  get program information

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip:


.. code-block::

    python -m pip --upgrade pip

- to install the latest release from PyPi via pip (recommended):

.. code-block::

    python -m pip install --upgrade security_dependency_pinning


- to install the latest release from PyPi via pip, including test dependencies:

.. code-block::

    python -m pip install --upgrade security_dependency_pinning[test]

- to install the latest version from github via pip:


.. code-block::

    python -m pip install --upgrade git+https://github.com/bitranox/security_dependency_pinning.git


- include it into Your requirements.txt:

.. code-block::

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    security_dependency_pinning

    # for the latest development version :
    security_dependency_pinning @ git+https://github.com/bitranox/security_dependency_pinning.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version, including test dependencies from source code:

.. code-block::

    # cd ~
    $ git clone https://github.com/bitranox/security_dependency_pinning.git
    $ cd security_dependency_pinning
    python -m pip install -e .[test]

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/security_dependency_pinning.git
    $ cd security_dependency_pinning

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    click
    toml

    ## security pinnings
    # not directly required, pinned to avoid vulnerability CVE-2023-37920
    certifi>=2024.2.2
    # not directly required, pinned to avoid vulnerability CVE-2023-5752
    pip>=24.0
    # not directly required, pinned to avoid vulnerability CVE-2023-43804, CVE-2023-45803
    urllib3>=2.2.0
    # not directly required, pinned to avoid vulnerability CVE-2023-27522
    # uwsgi not available on windows
    # uwsgi not available on graalpy (reports python 3.11 for graalpy 24.1 )
    uwsgi>=2.0.21 ; sys_platform != 'win32' and platform_python_implementation == 'CPython'
    # not directly required, pinned to avoid vulnerability CVE-2023-27522
    zipp>=3.19.1
    # not directly required, pinned to avoid Always-Incorrect Control Flow Implementation
    requests>=2.32.0

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/security_dependency_pinning/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v1.0.1
--------
2024-10-01:
    - do not import uwsgi on windows and platform implementations other then cpython, for graalpy 24.1 and jupyter
    - zipp>=3.19.1
    - requests>=2.32.0
    - add graalpy tests
    - setup python@v5
    - codecov token

v1.0.0
--------
2024-03-01: Initial release
    certifi>=2024.2.2  # pinned to avoid vulnerability CVE-2023-37920
    pip>=24.0          # pinned to avoid vulnerability CVE-2023-5752
    uwsgi>=2.0.21; sys_platform != 'win32'  # pinned to avoid vulnerability CVE-2023-27522
    urllib3>=2.2.0     # pinned to avoid vulnerability CVE-2023-43804, CVE-2023-45803

