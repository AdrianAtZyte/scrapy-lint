from __future__ import annotations

from inspect import cleandoc

from . import NO_ISSUE, Cases, ExpectedIssue, File, cases, iter_issues
from .helpers import check_project

DEPRECATION_VERSION = "2.14.0"
PARTIAL_FREEZE = ExpectedIssue(
    "SCP13 incomplete requirements freeze",
    path="requirements.txt",
)


def deprecated_argument_issue(line: int, column: int) -> ExpectedIssue:
    return ExpectedIssue(
        f"SCP51 deprecated argument: deprecated in scrapy "
        f"{DEPRECATION_VERSION}; keep the crawler from from_crawler() and use "
        f"its spider attribute instead",
        line=line,
        column=column,
        path="a.py",
    )


DEPRECATED_ARGUMENT_CASES: Cases = (
    *(
        (
            (
                File(f"scrapy=={version}", path="requirements.txt"),
                File(cleandoc(code), path="a.py"),
            ),
            (PARTIAL_FREEZE, *iter_issues(issues)),
            {},
        )
        for version, code, issues in (
            # Every affected method, and untouched neighbors.
            (
                DEPRECATION_VERSION,
                """
            class MyMiddleware:
                def process_request(self, request, spider):
                    pass

                def process_response(self, request, response, spider):
                    pass

                def process_exception(self, request, exception, spider):
                    pass

                def process_spider_input(self, response, spider):
                    pass

                async def process_spider_output(self, response, result, spider):
                    pass

                def process_spider_exception(self, response, exception, spider):
                    pass

                def process_item(self, item, spider):
                    pass

                def open_spider(self, spider):
                    pass

                def close_spider(self, spider):
                    pass

                async def fetch(self, request, spider):
                    pass

                def parse(self, response, spider):
                    pass
            """,
                (
                    deprecated_argument_issue(2, 39),
                    deprecated_argument_issue(5, 50),
                    deprecated_argument_issue(8, 52),
                    deprecated_argument_issue(11, 45),
                    deprecated_argument_issue(14, 60),
                    deprecated_argument_issue(17, 60),
                    deprecated_argument_issue(20, 33),
                    deprecated_argument_issue(23, 26),
                    deprecated_argument_issue(26, 27),
                    deprecated_argument_issue(29, 35),
                ),
            ),
            # Keyword-only and positional-only parameters.
            (
                DEPRECATION_VERSION,
                """
            class MyPipeline:
                name = "x"

                def process_item(self, item, /, *, spider):
                    pass

                def open_spider(self, spider=None):
                    pass

                def close_spider(self, *, spider=None):
                    pass
            """,
                deprecated_argument_issue(4, 39),
            ),
            # Older Scrapy versions.
            (
                "2.13.2",
                """
            class MyPipeline:
                def process_item(self, item, spider):
                    pass
            """,
                NO_ISSUE,
            ),
            # Functions outside a class body.
            (
                DEPRECATION_VERSION,
                """
            def process_item(item, spider):
                pass
            """,
                NO_ISSUE,
            ),
        )
    ),
    # No frozen Scrapy version.
    (
        (
            File(
                "class MyPipeline:\n    def process_item(self, item, spider):\n"
                "        pass",
                path="a.py",
            ),
        ),
        NO_ISSUE,
        {},
    ),
)


def deprecated_method_issue(line: int, column: int) -> ExpectedIssue:
    return ExpectedIssue(
        "SCP52 deprecated method: deprecated in scrapy 2.16.0; "
        "use form2request instead",
        line=line,
        column=column,
        path="a.py",
    )


DEPRECATED_METHOD_CASES: Cases = tuple(
    (
        File(cleandoc(code), path="a.py"),
        tuple(iter_issues(issues)),
        {},
    )
    for code, issues in (
        # Every supported way to reach the class.
        (
            """
            from scrapy import FormRequest
            from scrapy.http import FormRequest as AliasedFormRequest
            import scrapy

            FormRequest.from_response(response)
            AliasedFormRequest.from_response(response)
            scrapy.FormRequest.from_response(response)
            scrapy.http.FormRequest.from_response(response)
            """,
            (
                deprecated_method_issue(5, 0),
                deprecated_method_issue(6, 0),
                deprecated_method_issue(7, 0),
                deprecated_method_issue(8, 0),
            ),
        ),
        # Same method name on something else, and the class without the method.
        (
            """
            from scrapy import FormRequest

            Foo.from_response(response)
            from_response(response)
            FormRequest(url)
            """,
            NO_ISSUE,
        ),
        # An alias of a class that is not FormRequest.
        (
            """
            from scrapy import Request as FormRequest2

            FormRequest2.from_response(response)
            """,
            NO_ISSUE,
        ),
    )
)


@cases(DEPRECATED_ARGUMENT_CASES)
def test_deprecated_argument(files, expected, options):
    check_project(files, expected, options)


@cases(DEPRECATED_METHOD_CASES)
def test_deprecated_method(files, expected, options):
    check_project(files, expected, options)
