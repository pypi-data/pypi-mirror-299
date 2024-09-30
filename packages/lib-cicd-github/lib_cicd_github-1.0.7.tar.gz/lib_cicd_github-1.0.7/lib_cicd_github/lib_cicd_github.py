# STDLIB
import os
import pathlib
import subprocess
import sys
import time
from typing import List

# OWN
import lib_log_utils
import cli_exit_tools


# run{{{
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
    # run}}}

    command = command.strip()
    lib_log_utils.setup_handler()

    if show_command:
        command_description = command
    else:
        command_description = "***secret***"

    lib_log_utils.banner_success(
        f"Action: {description}\nCommand: {command_description}",
        banner=banner,
    )
    tries = retry
    while True:
        try:
            subprocess.run(command, shell=True, check=True)
            lib_log_utils.banner_success(f"Success: {description}", banner=False)
            break
        except Exception as exc:
            tries = tries - 1
            # try 3 times, because sometimes connection or other errors on the CICD Cloud Instance
            if tries:
                lib_log_utils.banner_spam(
                    f"Retry in {sleep} seconds: {description}\nCommand: {command_description}",
                    banner=False,
                )
                time.sleep(sleep)
            else:
                if show_command:
                    exc_message = str(exc)
                else:
                    exc_message = "Command ***secret*** returned non-zero exit status"
                lib_log_utils.banner_error(
                    f"Error: {description}\nCommand: {command_description}\n{exc_message}",
                    banner=True,
                )
                if hasattr(exc, "returncode"):
                    if exc.returncode is not None:  # type: ignore
                        sys.exit(exc.returncode)  # type: ignore
                sys.exit(1)  # pragma: no cover
        finally:
            try:
                # on Windows under github actions we have got "ValueError: underlying buffer has been detached"
                cli_exit_tools.flush_streams()
            except ValueError:
                pass


# get_branch{{{
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
    # get_branch}}}

    github_ref = get_env_data("GITHUB_REF")
    github_head_ref = get_env_data("GITHUB_HEAD_REF")
    github_event_name = get_env_data("GITHUB_EVENT_NAME")

    if github_event_name == "pull_request":
        branch = github_head_ref
    elif github_event_name == "release":
        branch = "release"
    elif github_event_name == "push":
        if github_ref:
            branch = github_ref.split("/")[-1]
        else:
            branch = f"unknown branch, event={github_event_name}"
    else:
        branch = f"unknown branch, event={github_event_name}"
    return branch


# install{{{
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
    # install}}}
    if dry_run:
        return
    pip_prefix = get_pip_prefix()
    run(
        description="install pip",
        command=" ".join([pip_prefix, "install --upgrade pip"]),
    )
    run(
        description="install setuptools",
        command=" ".join([pip_prefix, "install --upgrade setuptools"]),
    )

    if is_do_pip_install_test():
        run(
            description="pip install package in editable(develop) mode",
            command=" ".join([pip_prefix, "install --editable .[test]"]),
        )
    elif is_do_pip_install():
        run(
            description="pip install package",
            command=" ".join([pip_prefix, "install ."]),
        )
    else:
        lib_log_utils.banner_spam("package will be not installed")


# script{{{
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
    # script}}}
    if dry_run:
        return
    lib_log_utils.setup_handler()
    command_prefix = get_env_data("cPREFIX")
    package_name = get_env_data("PACKAGE_NAME")
    python_prefix = get_python_prefix()
    pip_prefix = get_pip_prefix()

    if do_flake8_tests():
        run(description="flake8 tests", command=f"{python_prefix} -m flake8 --statistics --benchmark")
    else:
        lib_log_utils.banner_spam("flake8 tests disabled on this build")

    if is_run_mypy_tests():
        run_mypy_tests(package_name=package_name, python_prefix=python_prefix)
    else:
        lib_log_utils.banner_spam("mypy tests disabled on this build")

    if do_pytest():
        if do_coverage():
            option_codecov = f"--cov={package_name}"
        else:
            lib_log_utils.banner_spam("coverage disabled on this build")
            option_codecov = ""
        run(description="run pytest", command=f"{python_prefix} -m pytest {option_codecov}")
    else:
        lib_log_utils.banner_spam("pytest disabled on this build")

    if do_check_cli():
        cli_command = get_env_data("CLI_COMMAND").strip()
        run(description="check CLI command", command=f"{command_prefix} {cli_command} --version")

    if do_build_docs():
        rst_include_source = os.getenv("RST_INCLUDE_SOURCE", "")
        rst_include_target = os.getenv("RST_INCLUDE_TARGET", "")
        rst_include_source_name = pathlib.Path(rst_include_source).name
        rst_include_target_name = pathlib.Path(rst_include_target).name
        run(
            description=f"rst rebuild {rst_include_target_name} from {rst_include_source_name}",
            command=f"{command_prefix} rst_include include {rst_include_source} {rst_include_target}",
        )
    else:
        lib_log_utils.banner_spam("rebuild doc file is disabled on this build")

    if do_build() or do_build_test():
        run(
            description="upgrade building system",
            command=" ".join([pip_prefix, "install --upgrade build"]),
        )

        run(
            description="upgrade twine",
            command=" ".join([pip_prefix, "install --upgrade twine"]),
        )

        run(
            description="build wheel and sdist",
            command=" ".join([python_prefix, "-m build"]),
        )

        run(
            description="check distributions",
            command=" ".join([python_prefix, "-m twine check dist/*"]),
        )

        list_dist_directory()


# after_success{{{
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
    # after_success}}}

    if dry_run:
        return

    if do_coverage():
        coverage_report()
        coverage_codecov()
        coverage_codeclimate()
    else:
        lib_log_utils.banner_spam("coverage is disabled")


def coverage_report() -> None:
    """ create coverage report """
    command_prefix = get_env_data("cPREFIX")
    run(description="coverage report", command=f"{command_prefix} coverage report")


def coverage_codecov() -> None:
    """ upload coverage to codecov, except on scheduled builds """
    command_prefix = get_env_data("cPREFIX")
    if do_upload_codecov():
        if is_scheduled():
            lib_log_utils.banner_spam("this is a scheduled build, therefore we dont upload codecov coverage AGAIN , because of codecov error 'Too many "
                                      "uploads to this commit.'")
        else:
            warn_if_no_codecov_token()
            slug = get_env_data("GITHUB_REPOSITORY").strip()
            run(description="coverage upload to codecov", command=f"{command_prefix} codecov --slug {slug}")
    else:
        lib_log_utils.banner_spam("codecov upload disabled")


def warn_if_no_codecov_token() -> None:
    slug = get_env_data("GITHUB_REPOSITORY").strip()
    codecov_token = get_env_data("CODECOV_TOKEN").strip()
    if not codecov_token:
        lib_log_utils.banner_spam(f"please pass the Repository Secret CODECOV_TOKEN for {slug} under "
                                  f"https://github.com/{slug}/settings/secrets/actions")


def coverage_codeclimate() -> None:
    """ upload coverage to codeclimate, except on scheduled builds """
    cc_test_reporter_id = get_env_data("CC_TEST_REPORTER_ID").strip()
    if do_upload_code_climate() and cc_test_reporter_id:
        if is_scheduled():
            lib_log_utils.banner_spam("this is a scheduled build, therefore we dont upload test results to codeclimate")
        else:
            if is_ci_runner_os_macos() or is_ci_runner_os_linux():
                download_code_climate_test_reporter_on_linux_or_macos()
                upload_code_climate_test_report_on_linux_or_macos()
            elif is_ci_runner_os_windows():
                lib_log_utils.banner_warning('Code Climate: no working "codeclimate-test-reporter" for Windows available, Nov. 2021')
            else:
                lib_log_utils.banner_warning("Code Climate Coverage - unknown RUNNER_OS ")
    else:
        lib_log_utils.banner_spam("Code Climate Coverage is disabled, or missing CC_TEST_REPORTER_ID")


def download_code_climate_test_reporter_on_linux_or_macos() -> None:
    download_link = ""
    if is_ci_runner_os_macos():
        download_link = "https://codeclimate.com/downloads/test-reporter/test-reporter-latest-darwin-amd64"
    elif is_ci_runner_os_linux():
        download_link = "https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64"
    else:
        lib_log_utils.banner_warning("Code Climate Coverage - unknown RUNNER_OS ")

    run(
        description="download code climate test reporter",
        command=f"curl -L {download_link} > ./cc-test-reporter",
    )
    run(
        description="set permissions for code climate test reporter",
        banner=False,
        command="chmod +x ./cc-test-reporter",
    )


def upload_code_climate_test_report_on_linux_or_macos() -> None:
    # Test Exit Code is always zero here, since the previous step on github actions completed without error
    test_exit_code = 0
    cc_test_reporter_id = get_env_data("CC_TEST_REPORTER_ID").strip()
    run(
        description="code climate test report upload",
        command=f"./cc-test-reporter after-build --exit-code {test_exit_code} --id {cc_test_reporter_id}",
    )


# deploy{{{
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
    # deploy}}}

    if dry_run:
        return
    pypi_api_upload_token = get_env_data("PYPI_UPLOAD_API_TOKEN").strip()
    if not pypi_api_upload_token:
        lib_log_utils.banner_warning("can not deploy, because secret PYPI_UPLOAD_API_TOKEN is missing")
    elif do_deploy():
        if not dry_run:  # pragma: no cover
            run(
                description="upload to pypi",
                command=" ".join(
                    [
                        get_python_prefix(),
                        "-m twine upload --repository-url https://upload.pypi.org/legacy/ -u __token__ -p",
                        pypi_api_upload_token,
                        "--skip-existing",
                        "dist/*",
                    ]
                ),
                show_command=False,
            )  # pragma: no cover
    else:
        lib_log_utils.banner_spam("pypi deploy is disabled on this build")


def list_dist_directory() -> None:
    """dir the dist directory if exists"""
    command_prefix = get_env_data("cPREFIX")
    if pathlib.Path("./dist").is_dir():
        run(description="list ./dist directory", command=f"{command_prefix} ls -l ./dist")
    else:
        lib_log_utils.banner_warning('no "./dist" directory found')


def get_pip_prefix() -> str:
    """
    get the pip_prefix including the command prefix like : 'wine python -m pip'

    >>> # test
    >>> if 'cPREFIX' in os.environ:
    ...    discard = get_pip_prefix()
    """
    c_parts: List[str] = list()
    c_parts.append(os.getenv("cPREFIX", ""))
    c_parts.append(os.getenv("cPIP", ""))
    command_prefix = " ".join(c_parts).strip()
    return command_prefix


def get_python_prefix() -> str:
    """
    get the python_prefix including the command prefix like : 'wine python'

    >>> # test
    >>> if 'cPREFIX' in os.environ:
    ...    discard = get_python_prefix()
    """
    c_parts: List[str] = list()
    c_parts.append(os.getenv("cPREFIX", ""))
    c_parts.append(os.getenv("cPYTHON", ""))
    python_prefix = " ".join(c_parts).strip()
    return python_prefix


def get_github_eventname() -> str:
    """
    see: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows
    get the github eventname  like:
    schedule, push, pull_request, release

    >>> # test
    >>> assert get_github_eventname() == get_env_data("GITHUB_EVENT_NAME")
    """
    github_event_name = get_env_data("GITHUB_EVENT_NAME")
    return github_event_name


def get_github_username() -> str:
    """
    get the github username like 'bitranox' (the OWNER of the Repository !)

    >>> # test
    >>> discard = get_github_username()
    """
    return get_env_data("GITHUB_REPOSITORY_OWNER")


def is_run_mypy_tests() -> bool:
    """
    if mypy should be run

    Parameter
    ---------
    MYPY_DO_TESTS
        from environment

    Examples:

    >>> # Setup
    >>> save_do_mypy = os.getenv('MYPY_DO_TESTS')

    >>> # BUILD_TEST != 'True'
    >>> os.environ['MYPY_DO_TESTS'] = 'false'
    >>> assert not is_run_mypy_tests()

    >>> # BUILD_TEST == 'true'
    >>> os.environ['MYPY_DO_TESTS'] = 'True'
    >>> assert is_run_mypy_tests()

    >>> # Teardown
    >>> if save_do_mypy is None:
    ...     os.unsetenv('MYPY_DO_TESTS')
    ... else:
    ...     os.environ['MYPY_DO_TESTS'] = save_do_mypy
    """

    if os.getenv("MYPY_DO_TESTS", "").lower() == "true":
        return True
    else:
        return False


def do_pytest() -> bool:
    """
    if pytest should be run

    Parameter
    ---------
    PYTEST_DO_TESTS
        from environment

    Examples:

    >>> # Setup
    >>> save_do_pytest = os.getenv('PYTEST_DO_TESTS')

    >>> # BUILD_TEST != 'True'
    >>> os.environ['PYTEST_DO_TESTS'] = 'false'
    >>> assert not do_pytest()

    >>> # BUILD_TEST == 'true'
    >>> os.environ['PYTEST_DO_TESTS'] = 'True'
    >>> assert do_pytest()

    >>> # Teardown
    >>> if save_do_pytest is None:
    ...     os.unsetenv('PYTEST_DO_TESTS')
    ... else:
    ...     os.environ['PYTEST_DO_TESTS'] = save_do_pytest
    """
    if os.getenv("PYTEST_DO_TESTS", "").lower() == "true":
        return True
    else:
        return False


def do_coverage() -> bool:
    """
    if coverage should be run (via pytest)

    Parameter
    ---------
    DO_COVERAGE
        from environment

    Examples:

    >>> # Setup
    >>> save_do_coverage = os.getenv('DO_COVERAGE')

    >>> # BUILD_TEST != 'True'
    >>> os.environ['DO_COVERAGE'] = 'false'
    >>> assert not do_coverage()

    >>> # BUILD_TEST == 'true'
    >>> os.environ['DO_COVERAGE'] = 'True'
    >>> assert do_coverage()

    >>> # Teardown
    >>> if save_do_coverage is None:
    ...     os.unsetenv('DO_COVERAGE')
    ... else:
    ...     os.environ['DO_COVERAGE'] = save_do_coverage
    """
    return get_env_data("DO_COVERAGE").lower() == "true"


def do_upload_codecov() -> bool:
    """
    if code coverage should be uploaded to codecov

    Parameter
    ---------
    DO_COVERAGE_UPLOAD_CODECOV
        from environment

    Examples:

    >>> # Setup
    >>> save_upload_codecov = os.getenv('DO_COVERAGE_UPLOAD_CODECOV')

    >>> # BUILD_TEST != 'True'
    >>> os.environ['DO_COVERAGE_UPLOAD_CODECOV'] = 'false'
    >>> assert not do_upload_codecov()

    >>> # BUILD_TEST == 'true'
    >>> os.environ['DO_COVERAGE_UPLOAD_CODECOV'] = 'True'
    >>> assert do_upload_codecov()

    >>> # Teardown
    >>> if save_upload_codecov is None:
    ...     os.unsetenv('DO_COVERAGE_UPLOAD_CODECOV')
    ... else:
    ...     os.environ['DO_COVERAGE_UPLOAD_CODECOV'] = save_upload_codecov

    """
    return get_env_data("DO_COVERAGE_UPLOAD_CODECOV").lower() == "true"


def do_upload_code_climate() -> bool:
    """
    if code coverage should be uploaded to code climate

    Parameter
    ---------
    DO_COVERAGE_UPLOAD_CODE_CLIMATE
        from environment

    Examples:

    >>> # Setup
    >>> save_upload_code_climate = os.getenv('DO_COVERAGE_UPLOAD_CODE_CLIMATE')

    >>> # BUILD_TEST != 'True'
    >>> os.environ['DO_COVERAGE_UPLOAD_CODE_CLIMATE'] = 'false'
    >>> assert not do_upload_code_climate()

    >>> # BUILD_TEST == 'true'
    >>> os.environ['DO_COVERAGE_UPLOAD_CODE_CLIMATE'] = 'True'
    >>> assert do_upload_code_climate()

    >>> # Teardown
    >>> if save_upload_code_climate is None:
    ...     os.unsetenv('DO_COVERAGE_UPLOAD_CODE_CLIMATE')
    ... else:
    ...     os.environ['DO_COVERAGE_UPLOAD_CODE_CLIMATE'] = save_upload_code_climate
    """
    return get_env_data("DO_COVERAGE_UPLOAD_CODE_CLIMATE").lower() == "true"


def is_do_pip_install() -> bool:
    # "DO_SETUP_INSTALL" is deprecated and will be replaced with "DO_PIP_INSTALL"
    do_pip_install = get_env_data("DO_SETUP_INSTALL").lower() == "true" or get_env_data("DO_PIP_INSTALL").lower() == "true"
    return do_pip_install


def is_do_pip_install_test() -> bool:
    # "DO_SETUP_INSTALL_TEST" is deprecated and will be replaced with "DO_PIP_INSTALL_TEST"
    do_pip_install_test = get_env_data("DO_SETUP_INSTALL_TEST").lower() == "true" or get_env_data("DO_PIP_INSTALL_TEST").lower() == "true"
    return do_pip_install_test


def do_check_cli() -> bool:
    return get_env_data("DO_CLI_TEST").lower() == "true"


def do_build_docs() -> bool:
    """
    if README.rst should be rebuilt

    Parameter
    ---------
    BUILD_DOCS
        from environment, "True" or "False"
    RST_INCLUDE_SOURCE
        from environment, the source template file
    RST_INCLUDE_TARGET
        from environment, the target file


    Examples:

    >>> # Setup
    >>> save_build_docs = get_env_data('BUILD_DOCS')
    >>> save_rst_include_source = get_env_data('RST_INCLUDE_SOURCE')
    >>> save_rst_include_target = get_env_data('RST_INCLUDE_TARGET')

    >>> # BUILD_DOCS != 'true'
    >>> set_env_data('BUILD_DOCS', 'false')
    >>> set_env_data('RST_INCLUDE_SOURCE', '')
    >>> set_env_data('RST_INCLUDE_TARGET', '')
    >>> assert do_build_docs() == False

    >>> # BUILD_DOCS == 'true', no source, no target
    >>> set_env_data('BUILD_DOCS', 'true')
    >>> set_env_data('RST_INCLUDE_SOURCE', '')
    >>> set_env_data('RST_INCLUDE_TARGET', '')
    >>> assert do_build_docs() == False

    >>> # BUILD_DOCS == 'true', no source
    >>> set_env_data('BUILD_DOCS', 'true')
    >>> set_env_data('RST_INCLUDE_SOURCE', '')
    >>> set_env_data('RST_INCLUDE_TARGET', 'some_target')
    >>> assert do_build_docs() == False

    >>> # BUILD_DOCS == 'true', source and target
    >>> set_env_data('BUILD_DOCS', 'true')
    >>> set_env_data('RST_INCLUDE_SOURCE', 'some_source')
    >>> set_env_data('RST_INCLUDE_TARGET', 'some_target')
    >>> assert do_build_docs() == True

    >>> # Teardown
    >>> set_env_data('BUILD_DOCS', save_build_docs)
    >>> set_env_data('RST_INCLUDE_SOURCE', save_rst_include_source)
    >>> set_env_data('RST_INCLUDE_TARGET', save_rst_include_target)
    """
    if get_env_data("BUILD_DOCS").lower() != "true":
        return False

    if not get_env_data("RST_INCLUDE_SOURCE"):
        return False

    if not get_env_data("RST_INCLUDE_TARGET"):
        return False
    else:
        return True


def do_flake8_tests() -> bool:
    """
    if we should do flake8 tests

    Parameter
    ---------
    DO_FLAKE8_TESTS
        from environment

    Examples:

    >>> # Setup
    >>> save_flake8_test = os.getenv('DO_FLAKE8_TESTS')

    >>> # DO_FLAKE8_TESTS != 'true'
    >>> os.environ['DO_FLAKE8_TESTS'] = 'false'
    >>> assert not do_flake8_tests()

    >>> # DO_FLAKE8_TESTS == 'true'
    >>> os.environ['DO_FLAKE8_TESTS'] = 'True'
    >>> assert do_flake8_tests()

    >>> # Teardown
    >>> if save_flake8_test is None:
    ...     os.unsetenv('DO_FLAKE8_TESTS')
    ... else:
    ...     os.environ['DO_FLAKE8_TESTS'] = save_flake8_test
    """
    if os.getenv("DO_FLAKE8_TESTS", "").lower() == "true":
        return True
    else:
        return False


def do_build() -> bool:
    """
    if a build (sdist and wheel) should be done

    Parameter
    ---------
    BUILD
        from environment

    Examples:

    >>> # Setup
    >>> save_build = os.getenv('BUILD')

    >>> # BUILD_TEST != 'True'
    >>> os.environ['BUILD'] = 'false'
    >>> assert not do_build()

    >>> # BUILD_TEST == 'true'
    >>> os.environ['BUILD'] = 'True'
    >>> assert do_build()

    >>> # Teardown
    >>> if save_build is None:
    ...     os.unsetenv('BUILD')
    ... else:
    ...     os.environ['BUILD'] = save_build
    """
    if os.getenv("BUILD", "").lower() == "true":
        return True
    else:
        return False


def do_build_test() -> bool:
    """
    if a build should be created for test purposes

    Parameter
    ---------
    BUILD_TEST
        from environment

    Examples:

    >>> # Setup
    >>> save_build_test = os.getenv('BUILD_TEST')

    >>> # BUILD_TEST != 'True'
    >>> os.environ['BUILD_TEST'] = 'false'
    >>> assert not do_build_test()

    >>> # BUILD_TEST == 'true'
    >>> os.environ['BUILD_TEST'] = 'True'
    >>> assert do_build_test()

    >>> # Teardown
    >>> if save_build_test is None:
    ...     os.unsetenv('BUILD_TEST')
    ... else:
    ...     os.environ['BUILD_TEST'] = save_build_test
    """
    if os.getenv("BUILD_TEST", "").lower() == "true":
        return True
    else:
        return False


def is_pypy3() -> bool:
    """
    if it is a pypy3 build

    Parameter
    ---------
    matrix.python-version
        from environment

    Examples:

    >>> # Setup
    >>> save_python_version = get_env_data('matrix.python-version')

    >>> # Test
    >>> set_env_data('matrix.python-version', 'pypy-3.7')
    >>> assert is_pypy3() == True

    >>> set_env_data('matrix.python-version', '3.9')
    >>> assert is_pypy3() == False

    >>> # Teardown
    >>> set_env_data('matrix.python-version', save_python_version)
    """
    return get_env_data("matrix.python-version").lower().startswith("pypy-3")


def is_ci_runner_os_windows() -> bool:
    """
    if the ci runner os is windows

    Parameter
    ---------
    runner.os
        from environment

    Examples:

    >>> # Setup
    >>> save_gha_os_name = get_env_data('RUNNER_OS')

    >>> # runner.os == 'linux'
    >>> set_env_data('RUNNER_OS', 'Linux')
    >>> assert is_ci_runner_os_windows() == False

    >>> # RUNNER_OS == 'windows'
    >>> set_env_data('RUNNER_OS', 'Windows')
    >>> assert is_ci_runner_os_windows() == True

    >>> # Teardown
    >>> set_env_data('RUNNER_OS', save_gha_os_name)
    """
    return get_env_data("RUNNER_OS").lower() == "windows"


def is_ci_runner_os_linux() -> bool:
    """
    if the ci runner os is linux

    Parameter
    ---------
    runner.os
        from environment

    Examples:

    >>> # Setup
    >>> save_gha_os_name = get_env_data('RUNNER_OS')

    >>> # runner.os == 'linux'
    >>> set_env_data('RUNNER_OS', 'Linux')
    >>> assert is_ci_runner_os_linux() == True

    >>> # RUNNER_OS == 'windows'
    >>> set_env_data('RUNNER_OS', 'Windows')
    >>> assert is_ci_runner_os_linux() == False

    >>> # Teardown
    >>> set_env_data('RUNNER_OS', save_gha_os_name)
    """
    return get_env_data("RUNNER_OS").lower() == "linux"


def is_ci_runner_os_macos() -> bool:
    """
    if the ci runner os is macos

    Parameter
    ---------
    RUNNER_OS
        from environment

    Examples:

    >>> # Setup
    >>> save_gha_os_name = get_env_data('RUNNER_OS')

    >>> # runner.os == 'linux'
    >>> set_env_data('RUNNER_OS', 'Linux')
    >>> assert is_ci_runner_os_macos() == False

    >>> # RUNNER_OS == 'macOS'
    >>> set_env_data('RUNNER_OS', 'macOS')
    >>> assert is_ci_runner_os_macos() == True

    >>> # Teardown
    >>> set_env_data('RUNNER_OS', save_gha_os_name)
    """
    return get_env_data("RUNNER_OS").lower() == "macos"


def do_deploy() -> bool:
    """
    if we should deploy
    if (DEPLOY_SDIST  or DEPLOY_WHEEL) and is_release()

    Parameter
    ---------
    DEPLOY_SDIST
        from environment
    DEPLOY_WHEEL
        from environment
    GITHUB_EVENT_NAME
        from environment

    Examples:

    >>> # Setup
    >>> save_github_event_name = get_env_data('GITHUB_EVENT_NAME')
    >>> save_build = get_env_data('BUILD')

    >>> # no Tagged Commit
    >>> set_env_data('GITHUB_EVENT_NAME', 'push')
    >>> assert False == do_deploy()

    >>> # Tagged Commit, DEPLOY_SDIST, DEPLOY_WHEEL != True
    >>> set_env_data('GITHUB_EVENT_NAME', 'release')
    >>> set_env_data('BUILD', '')
    >>> assert False == do_deploy()

    >>> # Tagged Commit, DEPLOY_SDIST == True
    >>> set_env_data('GITHUB_EVENT_NAME', 'release')
    >>> set_env_data('BUILD', 'True')
    >>> assert True == do_deploy()

    >>> # Teardown
    >>> set_env_data('GITHUB_EVENT_NAME', save_github_event_name)
    >>> set_env_data('BUILD', save_build)
    """
    return do_build() and is_release()


def is_release() -> bool:
    """
    Returns True, if this is a release (and then we deploy to pypi probably)
    """
    return get_github_eventname() == "release"


def is_scheduled() -> bool:
    """
    Returns True, if this is a scheduled run
    """
    return get_github_eventname() == "schedule"


def get_env_data(env_variable: str) -> str:
    """
    >>> # Setup
    >>> save_mypy_path = get_env_data('MYPYPATH')

    >>> # Test
    >>> set_env_data('MYPYPATH', 'some_test')
    >>> assert get_env_data('MYPYPATH') == 'some_test'

    >>> # Teardown
    >>> set_env_data('MYPYPATH', save_mypy_path)
    """
    if env_variable in os.environ:
        env_data = os.environ[env_variable]
    else:
        env_data = ""
    return env_data


def set_env_data(env_variable: str, env_str: str) -> None:
    os.environ[env_variable] = env_str


def is_github_actions_active() -> bool:
    """
    if we are on github actions environment

    >>> # Test
    >>> assert is_github_actions_active() == is_github_actions_active()
    """
    return bool(get_env_data("CI") and get_env_data("GITHUB_WORKFLOW") and get_env_data("GITHUB_RUN_ID"))


def run_mypy_tests(package_name: str, python_prefix: str) -> None:
    crate_mypy_cache_directory()
    mypy_options = get_env_data("MYPY_OPTIONS")
    run(description="mypy tests", command=f"{python_prefix} -m mypy -p {package_name} {mypy_options}")


def crate_mypy_cache_directory() -> None:
    path_mypy_cache_dir = pathlib.Path.cwd() / '.mypy_cache'
    path_mypy_cache_dir.mkdir(exist_ok=True)


if __name__ == "__main__":
    print(
        b'this is a library only, the executable is named "lib_cicd_github_cli.py"',
        file=sys.stderr,
    )
