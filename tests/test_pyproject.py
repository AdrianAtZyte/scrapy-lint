from __future__ import annotations

from tests.helpers import check_project

from . import NO_ISSUE, Cases, ExpectedIssue, File, cases

CASES: Cases = (
    # Dependencies declared in pyproject.toml are read when there is no
    # requirements file.
    (
        (
            File("", path="scrapy.cfg"),
            File(
                '[project]\nname = "a"\ndependencies = ["scrapy"]\n',
                path="pyproject.toml",
            ),
            File("settings['SCRAPY_POET_CACHE']", path="a.py"),
        ),
        ExpectedIssue(
            "SCP31 missing setting requirement: scrapy-poet",
            column=9,
            path="a.py",
        ),
        {},
    ),
    (
        (
            File("", path="scrapy.cfg"),
            File(
                '[project]\nname = "a"\ndependencies = ["scrapy"]\n'
                '\n[project.optional-dependencies]\npoet = ["scrapy-poet"]\n',
                path="pyproject.toml",
            ),
            File("settings['SCRAPY_POET_CACHE']", path="a.py"),
        ),
        NO_ISSUE,
        {},
    ),
    (
        (
            File("", path="scrapy.cfg"),
            File(
                '[project]\nname = "a"\ndependencies = ["scrapy==2.6.3"]\n',
                path="pyproject.toml",
            ),
            File("settings['REQUEST_FINGERPRINTER_IMPLEMENTATION']", path="a.py"),
        ),
        ExpectedIssue(
            "SCP29 setting needs upgrade: added in scrapy 2.7.0",
            column=9,
            path="a.py",
        ),
        {},
    ),
    # A requirements file takes precedence over pyproject.toml.
    (
        (
            File("", path="scrapy.cfg"),
            File(
                '[project]\nname = "a"\ndependencies = ["scrapy", "scrapy-poet"]\n',
                path="pyproject.toml",
            ),
            File("scrapy\n", path="requirements.txt"),
            File("settings['SCRAPY_POET_CACHE']", path="a.py"),
        ),
        (
            ExpectedIssue(
                "SCP13 incomplete requirements freeze",
                path="requirements.txt",
            ),
            ExpectedIssue(
                "SCP31 missing setting requirement: scrapy-poet",
                column=9,
                path="a.py",
            ),
        ),
        {},
    ),
)


@cases(CASES)
def test(
    files: File | list[File],
    expected: ExpectedIssue | list[ExpectedIssue] | None,
    options,
):
    check_project(files, expected, options)
