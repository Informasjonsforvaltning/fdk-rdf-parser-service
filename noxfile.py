"""Nox sessions."""
import os
import sys

import nox
from nox_poetry import Session, session

python_versions = ["3.11"]
nox.options.envdir = ".cache"  # To run consecutive nox sessions faster.
locations = "fdk_rdf_parser_service", "tests", "noxfile.py"
nox.options.sessions = (
    "lint",
    "mypy",
    "safety",
    # "unit_tests",
    "integration_tests",
    # "contract_tests",
)


@session(python=python_versions[0])
def cache(session: Session) -> None:
    """Clear cache."""
    session.run(
        "bash",
        "-c",
        "for f in $(find . -maxdepth 1 -name '*cache*'); do rm -rf $f; done",
        external=True,
    )


@session(python=python_versions[0])
def black(session: Session) -> None:
    """Run black code formatter."""
    if os.getenv("CI"):
        print("Skipping black in CI")
        return
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python=python_versions[0])
def isort(session: Session) -> None:
    """Run isort import sorter."""
    if os.getenv("CI"):
        print("Skipping black in CI")
        return
    args = session.posargs or locations
    session.install("isort")
    session.run("isort", *args)


@session(python=python_versions[0])
def fixlint(session: Session) -> None:
    """Run import sort and black."""
    if os.getenv("CI"):
        print("Skipping black in CI")
        return
    session.notify("isort")
    session.notify("black")


@session(python=python_versions[0])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-builtins",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "flake8-rst-docstrings",
        "pep8-naming",
    )
    session.run("flake8", *args)


@session(python=python_versions[0])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install(".", "mypy", "pytest")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python=python_versions[0])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs
    session.install(
        ".",
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-docker",
        "pytest-aiohttp",
        "requests",
    )
    session.run(
        "pytest",
        "-rA",
        "--cov",
        *args,
    )


@session(python=python_versions)
def unit_tests(session: Session) -> None:
    """Run the unit test suite."""
    args = session.posargs
    session.install(".", "coverage[toml]", "pytest")
    # -rA shows extra test summary info regardless of test result
    session.run(
        "pytest",
        "-m",
        "unit",
        "-rA",
        *args,
    )


@session(python=python_versions)
def integration_tests(session: Session) -> None:
    """Run the integration test suite."""
    args = session.posargs
    session.install(
        ".",
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-aiohttp",
        "pytest-docker",
        "requests",
        "types-requests",
    )
    # -rA shows extra test summary info regardless of test result
    session.run(
        "pytest",
        "-m",
        "integration",
        "-rA",
        *args,
    )


# @session(python=python_versions[0])
# def contract_tests(session: Session) -> None:
#     """Run the contract test suite."""
#     args = session.posargs
#     session.install(".")
#     session.install("pytest", "pytest-docker", "requests", "types-requests")
#     # -rA shows extra test summary info regardless of test result
#     session.run(
#         "pytest",
#         "-m",
#         "contract",
#         "-rA",
#         *args,
#     )


@session(python=python_versions[0])
def coverage(session: Session) -> None:
    """Create report and upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@session(python=python_versions[0])
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    ignore = [
        "48547",  # rdflib
    ]
    ignore_args = [f"--ignore={i}" for i in ignore]
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run(
        "safety", "check", "--full-report", f"--file={requirements}", *ignore_args
    )
