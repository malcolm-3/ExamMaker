# ExamMaker

[![PyPI](https://img.shields.io/pypi/v/exammaker?style=flat-square)](https://pypi.python.org/pypi/exammaker/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/exammaker?style=flat-square)](https://pypi.python.org/pypi/exammaker/)
[![PyPI - License](https://img.shields.io/pypi/l/exammaker?style=flat-square)](https://pypi.python.org/pypi/exammaker/)
[![Coookiecutter - Wolt(fork)](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)


---

**Documentation**: [https://malcolm-3.github.io/exammaker](https://malcolm-3.github.io/exammaker)

**Source Code**: [https://github.com/malcolm-3/exammaker](https://github.com/malcolm-3/exammaker)

**PyPI**: [https://pypi.org/project/exammaker/](https://pypi.org/project/exammaker/)

---

Tool for generating exams in PDF

## Installation

```sh
pip install exammaker
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.9+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](https://github.com/malcolm-3/exammaker/tree/master/docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [GitHub Pages page](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/malcolm-3/exammaker/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/malcolm-3/exammaker/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/malcolm-3/exammaker/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatting (`ruff format`), linters (e.g. `ruff` and `mypy`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
