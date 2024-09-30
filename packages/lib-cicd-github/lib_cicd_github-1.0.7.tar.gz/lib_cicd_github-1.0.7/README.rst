lib_cicd_github
===============


Version v1.0.7 as of 2024-09-30 see `Changelog`_

|build_badge| |codeql| |license| |jupyter| |pypi|
|pypi-downloads| |black| |codecov| |cc_maintain| |cc_issues| |cc_coverage| |snyk|



.. |build_badge| image:: https://github.com/bitranox/lib_cicd_github/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/bitranox/lib_cicd_github/actions/workflows/python-package.yml


.. |codeql| image:: https://github.com/bitranox/lib_cicd_github/actions/workflows/codeql-analysis.yml/badge.svg?event=push
   :target: https://github.com//bitranox/lib_cicd_github/actions/workflows/codeql-analysis.yml

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/bitranox/lib_cicd_github/master?filepath=lib_cicd_github.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/lib-cicd-github?label=PyPI%20Package
   :target: https://badge.fury.io/py/lib_cicd_github

.. badge until 2023-10-08:
.. https://img.shields.io/codecov/c/github/bitranox/lib_cicd_github
.. badge from 2023-10-08:
.. |codecov| image:: https://codecov.io/gh/bitranox/lib_cicd_github/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/lib_cicd_github

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/lib_cicd_github?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/lib_cicd_github/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/lib_cicd_github?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/lib_cicd_github/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/lib_cicd_github?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/lib_cicd_github/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://snyk.io/test/github/bitranox/lib_cicd_github/badge.svg
   :target: https://snyk.io/test/github/bitranox/lib_cicd_github

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/lib-cicd-github
   :target: https://pypi.org/project/lib-cicd-github/
   :alt: PyPI - Downloads

small utils for github actions:
 - print colored banners
 - wrap commands into run/success/error banners, with automatic retry
 - resolve the branch to test, based on the environment variables

----

automated tests, Github Actions, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.8.0 or newer

tested on recent linux with python 3.8, 3.9, 3.10, 3.11, 3.12, pypy-3.9, pypy-3.10, graalpy-24.1 - architectures: amd64

`100% code coverage <https://codeclimate.com/github/bitranox/lib_cicd_github/test_coverage>`_, flake8 style checking ,mypy static type checking ,tested under `Linux, macOS, Windows <https://github.com/bitranox/lib_cicd_github/actions/workflows/python-package.yml>`_, automatic daily builds and monitoring

----

- `Try it Online`_
- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/lib_cicd_github/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/lib_cicd_github/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/lib_cicd_github/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/{{rst_include.
repository_slug}}/master?filepath=lib_cicd_github.ipynb>`_

Usage
-----------

- run a command passed as string

.. code-block:: bash

    # to be used in the github action YAML File
    # run a command passed as string, wrap it in colored banners, retry 3 times, sleep 30 seconds when retry
    $> lib_cicd_github_cli run "description" "command -some -options" --retry=3 --sleep=30


- get the branch to work on from environment variables

.. code-block:: bash

    $> BRANCH=$(lib_cicd_github_cli get_branch)

python methods:

- install, installs all needed dependencies to build and deploy the project

.. code-block:: python

    def install(dry_run: bool = True) -> None:
        """
        upgrades pip, setuptools, wheel and pytest-pycodestyle


        Parameter
        ---------
        cPIP
            from environment, the command to launch pip, like "python -m pip"


        Examples
        --------

        >>> # Test
        >>> if is_github_actions_active():
        ...     install(dry_run=True)

        """

- script, run all tests

.. code-block:: python

    def script(dry_run: bool = True) -> None:
        """
        jobs to run in CICD section "script":
        - run setup.py test
        - run pip with install option test
        - run pip standard install
        - test the CLI Registration
        - install the test requirements
        - install codecov
        - install pytest-codecov
        - run pytest coverage
        - run mypy strict
            - if MYPY_STRICT="True"
        - rebuild the rst files (resolve rst file includes)
            - needs RST_INCLUDE_SOURCE, RST_INCLUDE_TARGET set and BUILD_DOCS="True"
        - check if deployment would succeed, if setup.py exists and not a tagged build

        Parameter
        ---------
        cPREFIX
            from environment, the command prefix like 'wine' or ''
        cPIP
            from environment, the command to launch pip, like "python -m pip"
        cPYTHON
            from environment, the command to launch python, like 'python' or 'python3' on MacOS
        CLI_COMMAND
            from environment, must be set in CICD configuration file - the CLI command to test with option --version
        MYPY_STRICT
            from environment, if pytest with mypy --strict should run
        PACKAGE_NAME
            from environment, the package name to pass to mypy
        BUILD_DOCS
            from environment, if rst file should be rebuilt
        RST_INCLUDE_SOURCE
            from environment, the rst template with rst includes to resolve
        RST_INCLUDE_TARGET
            from environment, the rst target file
        DEPLOY_WHEEL
            from environment, if a wheel should be generated
            only if setup.py exists and on non-tagged builds (there we deploy for real)
        dry_run
            if set, this returns immediately - for CLI tests


        Examples
        --------
        >>> # test
        >>> script()

        """

- after_success, upload code coverage and codeclimate reports

.. code-block:: python

    def after_success(dry_run: bool = True) -> None:
        """
        jobs to run in CICD "after_success":
            - coverage report
            - codecov
            - codeclimate report upload

        it will not run on dry_run or on scheduled event - we dont need to upload
        coverage AGAIN on scheduled run.

        Parameter
        ---------
        cPREFIX
            from environment, the command prefix like 'wine' or ''
        cPIP
            from environment, the command to launch pip, like "python -m pip"
        CC_TEST_REPORTER_ID
            from environment, must be set in CICD configuration file
        dry_run
            if set, this returns immediately - for CLI tests



        Examples
        --------
        >>> # test
        >>> after_success()

        """

- deploy, deploy to pypi

.. code-block:: python

    def deploy(dry_run: bool = True) -> None:
        """
        uploads sdist and wheels to pypi on success


        Parameter
        ---------
        cPREFIX
            from environment, the command prefix like 'wine' or ''
        PYPI_UPLOAD_API_TOKEN
            from environment, passed as secure, encrypted variable via the GitHub repository secrets
        DEPLOY_SDIST, DEPLOY_WHEEL
            from environment, one of it needs to be true
        dry_run
            if set, this returns immediately - for CLI tests


        Examples
        --------
        >>> # test
        >>> deploy()

        """

- get_branch, determine the branch to work on

.. code-block:: python

    def get_branch() -> str:
        """
        Returns the branch to work on :
            <branch>    for push, pull requests, merge
            'release'   for tagged releases


        Parameter
        ---------
        github.ref, github.head_ref, github.event_name, github.job
            from environment

        Result
        ---------
        the branch


        Exceptions
        ------------
        none


        ==============  ===================  ===================  ===================  ===================
        Build           github.ref           github.head_ref      github.event_name    github.job
        ==============  ===================  ===================  ===================  ===================
        Push            refs/heads/<branch>  ---                  push                 build
        Custom Build    refs/heads/<branch>  ---                  push                 build
        Pull Request    refs/pull/xx/merge   <branch>             pull_request         build
        Merge           refs/heads/<branch>  ---                  push                 build
        Publish Tagged  refs/tags/<tag>      ---                  release              build
        ==============  ===================  ===================  ===================  ===================

        >>> # Setup
        >>> github_ref_backup = get_env_data('GITHUB_REF')
        >>> github_head_ref_backup = get_env_data('GITHUB_HEAD_REF')
        >>> github_event_name_backup = get_env_data('GITHUB_EVENT_NAME')

        >>> # test Push
        >>> set_env_data('GITHUB_REF', 'refs/heads/development')
        >>> set_env_data('GITHUB_HEAD_REF', '')
        >>> set_env_data('GITHUB_EVENT_NAME', 'push')
        >>> assert get_branch() == 'development'

        >>> # test Push without github.ref
        >>> set_env_data('GITHUB_REF', '')
        >>> set_env_data('GITHUB_HEAD_REF', '')
        >>> set_env_data('GITHUB_EVENT_NAME', 'push')
        >>> assert get_branch() == 'unknown branch, event=push'

        >>> # test PR
        >>> set_env_data('GITHUB_REF', 'refs/pull/xx/merge')
        >>> set_env_data('GITHUB_HEAD_REF', 'master')
        >>> set_env_data('GITHUB_EVENT_NAME', 'pull_request')
        >>> assert get_branch() == 'master'

        >>> # test Publish
        >>> set_env_data('GITHUB_REF', 'refs/tags/v1.1.15')
        >>> set_env_data('GITHUB_HEAD_REF', '')
        >>> set_env_data('GITHUB_EVENT_NAME', 'release')
        >>> assert get_branch() == 'release'

        >>> # test unknown event_name
        >>> set_env_data('GITHUB_REF', '')
        >>> set_env_data('GITHUB_HEAD_REF', '')
        >>> set_env_data('GITHUB_EVENT_NAME', 'unknown_event')
        >>> assert get_branch() == 'unknown branch, event=unknown_event'

        >>> # Teardown
        >>> set_env_data('GITHUB_REF', github_ref_backup)
        >>> set_env_data('GITHUB_HEAD_REF', github_head_ref_backup)
        >>> set_env_data('GITHUB_EVENT_NAME', github_event_name_backup)

        """

- run, usually used internally

.. code-block:: python

    def run(
        description: str,
        command: str,
        retry: int = 3,
        sleep: int = 30,
        banner: bool = True,
        show_command: bool = True,
    ) -> None:
        """
        runs and retries a command passed as string and wrap it in "success" or "error" banners


        Parameter
        ---------
        description
            description of the action, shown in the banner
        command
            the command to launch
        retry
            retry the command n times, default = 3
        sleep
            sleep for n seconds between the commands, default = 30
        banner
            if to use banner for run/success or just colored lines.
            Errors will be always shown as banner
        show_command
            if the command is shown - take care not to reveal secrets here !


        Result
        ---------
        none


        Exceptions
        ------------
        none


        Examples
        ------------

        >>> run('test', "unknown command", sleep=0)
        Traceback (most recent call last):
            ...
        SystemExit: ...

        >>> run('test', "unknown command", sleep=0, show_command=False)
        Traceback (most recent call last):
            ...
        SystemExit: ...

        >>> run('test', "echo test")
        >>> run('test', "echo test", show_command=False)

        """

- github actions yml File example

.. code-block:: yaml

    # This workflow will install Python dependencies, run tests and lint with a variety of Python versions
    # For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

    name: Python package

    on:
      push:
        branches: [ master, development ]
      pull_request:
        branches: [ master, development ]
      release:
        branches: [ master, development ]
        # release types see : https://docs.github.com/en/actions/reference/events-that-trigger-workflows#release
        # he prereleased type will not trigger for pre-releases published from draft releases, but the published type will trigger.
        # If you want a workflow to run when stable and pre-releases publish, subscribe to published instead of released and prereleased.
        types: [published]

      schedule:
          # * is a special character in YAML, so you have to quote this string
          # | minute | hour (UTC) | day of month (1-31) | month (1-2) | day of week (0-6 or SUN-SAT)
          # every day at 05:40 am UTC - avoid 05:00 because of high load at the beginning of every hour
          - cron:  '40 5 * * *'


    jobs:

      build:
        runs-on: ${{ matrix.os }}

        env:
            # prefix before commands - used for wine, there the prefix is "wine"
            cPREFIX: ""
            # command to launch python interpreter (it's different on macOS, there we need python3)
            cPYTHON: "python"
            # command to launch pip (it's different on macOS, there we need pip3)
            cPIP: "python -m pip"
            # switch off wine fix me messages
            WINEDEBUG: fixme-all

            # PYTEST
            PYTEST_DO_TESTS: "True"

            # FLAKE8 tests
            DO_FLAKE8_TESTS: "True"

            # MYPY tests
            MYPY_DO_TESTS: "True"
            MYPY_OPTIONS: "--follow-imports=normal --ignore-missing-imports --install-types --no-warn-unused-ignores --non-interactive --strict"
            MYPYPATH: "./.3rd_party_stubs"

            # coverage
            DO_COVERAGE: "True"
            DO_COVERAGE_UPLOAD_CODECOV: "True"
            DO_COVERAGE_UPLOAD_CODE_CLIMATE: "True"

            # package name
            PACKAGE_NAME: "lib_cicd_github"
            # the registered CLI Command
            CLI_COMMAND: "lib_cicd_github"
            # the source file for rst_include (rebuild rst file includes)
            RST_INCLUDE_SOURCE: "./.docs/README_template.rst"
            # the target file for rst_include (rebuild rst file includes)
            RST_INCLUDE_TARGET: "./README.rst"
            # make Code Climate Code Coverage Secret available in Environment
            CC_TEST_REPORTER_ID: ${{ secrets.CC_TEST_REPORTER_ID }}
            # make CODECOV_TOKEN Secret available in Environment
            CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
            # make PyPi API token available in Environment
            PYPI_UPLOAD_API_TOKEN: ${{ secrets.PYPI_UPLOAD_API_TOKEN }}
            # additional Environment Variables:

        strategy:
          matrix:
            include:
              # https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners#supported-software
              # https://github.com/actions/setup-python/blob/main/docs/advanced-usage.md#available-versions-of-python-and-pypy

              - os: windows-latest
                python-version: "3.12"
                env:
                  cEXPORT: "SET"
                  BUILD_DOCS: "False"
                  BUILD: "False"
                  BUILD_TEST: "False"
                  MYPY_DO_TESTS: "True"
                  # Setup tests
                  DO_SETUP_INSTALL: "False"
                  DO_SETUP_INSTALL_TEST: "True"
                  # Test registered CLI Command
                  DO_CLI_TEST: "True"


              - os: ubuntu-latest
                python-version: "3.8"
                env:
                  BUILD_DOCS: "False"
                  BUILD: "True"
                  BUILD_TEST: "True"
                  MYPY_DO_TESTS: "True"
                  DO_SETUP_INSTALL: "True"
                  DO_SETUP_INSTALL_TEST: "True"
                  DO_CLI_TEST: "True"

              - os: ubuntu-latest
                python-version: "3.9"
                env:
                  BUILD_DOCS: "False"
                  BUILD: "True"
                  BUILD_TEST: "True"
                  MYPY_DO_TESTS: "True"
                  DO_SETUP_INSTALL: "True"
                  DO_SETUP_INSTALL_TEST: "True"
                  DO_CLI_TEST: "True"

              - os: ubuntu-latest
                python-version: "3.10"
                env:
                  BUILD_DOCS: "False"
                  BUILD: "True"
                  BUILD_TEST: "True"
                  MYPY_DO_TESTS: "True"
                  DO_SETUP_INSTALL: "True"
                  DO_SETUP_INSTALL_TEST: "True"
                  DO_CLI_TEST: "True"

              - os: ubuntu-latest
                python-version: "3.11"
                env:
                  BUILD_DOCS: "True"
                  BUILD: "True"
                  BUILD_TEST: "True"
                  MYPY_DO_TESTS: "True"
                  DO_SETUP_INSTALL: "True"
                  DO_SETUP_INSTALL_TEST: "True"
                  DO_CLI_TEST: "True"

              - os: ubuntu-latest
                python-version: "3.12"
                env:
                  BUILD_DOCS: "True"
                  BUILD: "True"
                  BUILD_TEST: "True"
                  MYPY_DO_TESTS: "True"
                  DO_SETUP_INSTALL: "True"
                  DO_SETUP_INSTALL_TEST: "True"
                  DO_CLI_TEST: "True"

              - os: ubuntu-latest
                python-version: "pypy-3.9"
                env:
                  BUILD_DOCS: "False"
                  BUILD: "True"
                  BUILD_TEST: "True"
                  MYPY_DO_TESTS: "True"
                  DO_SETUP_INSTALL: "True"
                  DO_SETUP_INSTALL_TEST: "True"
                  DO_CLI_TEST: "True"

              - os: ubuntu-latest
                python-version: "pypy-3.10"
                env:
                  BUILD_DOCS: "False"
                  BUILD: "True"
                  BUILD_TEST: "True"
                  MYPY_DO_TESTS: "True"
                  DO_SETUP_INSTALL: "True"
                  DO_SETUP_INSTALL_TEST: "True"
                  DO_CLI_TEST: "True"

              - os: ubuntu-latest
                python-version: "graalpy-24.1"
                env:
                  BUILD_DOCS: "True"
                  BUILD: "True"
                  BUILD_TEST: "True"
                  MYPY_DO_TESTS: "True"
                  DO_SETUP_INSTALL: "True"
                  DO_SETUP_INSTALL_TEST: "True"
                  DO_CLI_TEST: "True"

              - os: macos-latest
                python-version: "3.12"
                env:
                  cPREFIX: ""               # prefix before commands - used for wine, there the prefix is "wine"
                  cPYTHON: "python3"        # command to launch python interpreter (it's different on macOS, there we need python3)
                  cPIP: "python3 -m pip"    # command to launch pip (it's different on macOS, there we need pip3)
                  BUILD_DOCS: "False"
                  BUILD: "True"
                  BUILD_TEST: "True"
                  MYPY_DO_TESTS: "True"
                  # Setup tests
                  DO_SETUP_INSTALL: "True"
                  DO_SETUP_INSTALL_TEST: "True"
                  # Test registered CLI Command
                  DO_CLI_TEST: "True"


        name: "${{ matrix.os }} Python ${{ matrix.python-version }}"

        steps:
        # see : https://github.com/actions/checkout
        - uses: actions/checkout@v4

        - name: Setting up Python ${{ matrix.python-version }}
          # see: https://github.com/actions/setup-python
          uses: actions/setup-python@v5
          with:
            python-version: ${{ matrix.python-version }}

        - name: Install dependencies
          # see: https://github.community/t/github-actions-new-bug-unable-to-create-environment-variables-based-matrix/16104/3
          env: ${{ matrix.env }}             # make matrix env variables accessible
          # lib_cicd_github install: upgrades pip, setuptools, wheel and pytest-pycodestyle
          run: |
            ${{ env.cPIP }} install git+https://github.com/bitranox/lib_cicd_github.git
            lib_cicd_github install

        - name: Debug - printenv and colortest
          env:
            # make matrix env variables accessible
            ${{ matrix.env }}
          shell: bash
          run: |
            # export for current step
            export "BRANCH=$(lib_cicd_github get_branch)"
            # export for subsequent steps
            echo "BRANCH=$BRANCH" >> $GITHUB_ENV
            log_util --level=SPAM  "working on branch $BRANCH"
            log_util --level=SPAM  "GITHUB_REF $GITHUB_REF"
            log_util --level=VERBOSE "github.base_ref: ${{ github.base_ref }}"
            log_util --level=VERBOSE "github.event: ${{ github.event }}"
            log_util --level=VERBOSE "github.event_name: ${{ github.event_name }}"
            log_util --level=VERBOSE "github.head_ref: ${{ github.head_ref }}"
            log_util --level=VERBOSE "github.job: ${{ github.job }}"
            log_util --level=VERBOSE "github.ref: ${{ github.ref }}"
            log_util --level=VERBOSE "github.repository: ${{ github.repository }}"
            log_util --level=VERBOSE "github.repository_owner: ${{ github.repository_owner }}"
            log_util --level=VERBOSE "runner.os: ${{ runner.os }}"
            log_util --level=VERBOSE "matrix.python-version: ${{ matrix.python-version }}"
            printenv
            log_util --colortest

        - name: Run Tests
          env:
            # make matrix env variables accessible
            ${{ matrix.env }}
          shell: bash
          run: |
            # export for current step
            export "BRANCH=$(lib_cicd_github get_branch)"
            # export for subsequent steps
            echo "BRANCH=$BRANCH" >> $GITHUB_ENV
            # run the tests
            lib_cicd_github script

        - name: After Success
          env:
            ${{matrix.env }}
          shell: bash
          continue-on-error: true
          run: |
            lib_cicd_github after_success

        - name: Deploy
          env:
            # see: https://docs.github.com/en/actions/reference/context-and-expression-syntax-for-github-actions#github-context
            # see : https://github.com/rlespinasse/github-slug-action
            # make matrix env variables accessible
            ${{matrix.env }}
          shell: bash
          run: |
            lib_cicd_github deploy

Usage from Commandline
------------------------

.. code-block::

   Usage: lib_cicd_github [OPTIONS] COMMAND [ARGS]...

     CI/CD (Continuous Integration / Continuous Delivery) - utils for github
     actions

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     after_success  coverage reports
     deploy         deploy on pypi
     get_branch     get the branch to work on
     info           get program informations
     install        updates pip, setuptools, wheel, pytest-pycodestyle
     run            run string command wrapped in run/success/error banners
     script         updates pip, setuptools, wheel, pytest-pycodestyle

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip:


.. code-block::

    python -m pip --upgrade pip

- to install the latest release from PyPi via pip (recommended):

.. code-block::

    python -m pip install --upgrade lib_cicd_github


- to install the latest release from PyPi via pip, including test dependencies:

.. code-block::

    python -m pip install --upgrade lib_cicd_github[test]

- to install the latest version from github via pip:


.. code-block::

    python -m pip install --upgrade git+https://github.com/bitranox/lib_cicd_github.git


- include it into Your requirements.txt:

.. code-block::

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    lib_cicd_github

    # for the latest development version :
    lib_cicd_github @ git+https://github.com/bitranox/lib_cicd_github.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version, including test dependencies from source code:

.. code-block::

    # cd ~
    $ git clone https://github.com/bitranox/lib_cicd_github.git
    $ cd lib_cicd_github
    python -m pip install -e .[test]

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/lib_cicd_github.git
    $ cd lib_cicd_github

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
    cli_exit_tools
    lib_detect_testenv
    lib_log_utils
    rst_include

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/lib_cicd_github/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v1.0.7
--------
2024-09-29:
    - codecov pass slug and CODECOV_TOKEN

v1.0.6
--------
2023-10-12:
    - do not upload codecov to codeclimate on scheduled builds

v1.0.5
--------
2023-10-09:
    - implement PyPI Upload API Token

v1.0.4
--------
2023-10-09:
    - repair scheduled run detection

v1.0.3
--------
2023-10-08:
    - do not upload codecov on scheduled builds, because of error
      'Too many uploads to this commit.' when upload codecov again and again.

v1.0.2
--------
2023-07-21:
    - create mypy cache dir '.mypy_cache'
    - require minimum python 3.8
    - remove python 3.7 tests
    - introduce PEP517 packaging standard
    - introduce pyproject.toml build-system
    - remove mypy.ini
    - remove pytest.ini
    - remove setup.cfg
    - remove setup.py
    - remove .bettercodehub.yml
    - remove .travis.yml
    - update black config
    - clean ./tests/test_cli.py
    - add codeql badge
    - move 3rd_party_stubs outside the src directory to ``./.3rd_party_stubs``
    - add pypy 3.10 tests
    - add python 3.12-dev tests

v1.0.1.2
---------
2022-06-02: update to github actions checkout@v3 and setup-python@v3

v1.0.1
--------
2022-03-29: remedy mypy Untyped decorator in cli

v1.0.0
---------
2022-03-25:
 - initial pypi release
 - update documentation and tests
 - list ./dist dir if existing

v0.0.1
---------
2021-08-23: initial release

