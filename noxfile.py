# mypy: disallow-untyped-defs=False, disallow-untyped-calls=False

import glob

import nox

nox.options.sessions = ["lint"]
nox.options.reuse_existing_virtualenvs = True


@nox.session(
    python=["3.7", "3.8", "3.9", "3.10", "3.11", "pypy3.7", "pypy3.8", "pypy3.9"]
)
def tests(session):
    def coverage(*args):
        session.run("python", "-m", "coverage", *args)

    session.install("-r", "tests/requirements.txt")
    session.install(".")

    if "pypy" not in session.python:
        coverage(
            "run",
            "--source",
            "packaging_legacy",
            "-m",
            "pytest",
            "--strict-markers",
            *session.posargs,
        )
        coverage("report", "-m", "--fail-under", "100")
    else:
        # Don't do coverage tracking for PyPy, since it's SLOW.
        session.run(
            "python",
            "-m",
            "pytest",
            "--capture=no",
            "--strict-markers",
            *session.posargs,
        )


@nox.session(python="3.9")
def lint(session):
    # Run the linters (via pre-commit)
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)

    # Check the distribution
    session.install("build", "twine")
    session.run("pyproject-build")
    session.run("twine", "check", *glob.glob("dist/*"))
