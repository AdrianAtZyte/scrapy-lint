from __future__ import annotations

from ast import (
    AsyncFunctionDef,
    Attribute,
    Call,
    ClassDef,
    FunctionDef,
    ImportFrom,
    Name,
)
from typing import TYPE_CHECKING

from packaging.version import Version

from scrapy_lint.data.methods import DEPRECATED_ARGUMENTS
from scrapy_lint.finders.unsupported import (
    VALID_REQUEST_IMPORT_PATHS,
    import_path_from_attribute,
)
from scrapy_lint.issues import DEPRECATED_ARGUMENT, DEPRECATED_METHOD, Issue, Pos

if TYPE_CHECKING:
    from ast import AST, arg, arguments, expr
    from collections.abc import Generator

    from scrapy_lint.context import Context

FROM_RESPONSE_DETAIL = "deprecated in scrapy 2.16.0; use form2request instead"


def iter_required_args(args: arguments) -> Generator[arg]:
    positional = args.posonlyargs + args.args
    if args.defaults:
        positional = positional[: -len(args.defaults)]
    yield from positional
    for keyword, default in zip(args.kwonlyargs, args.kw_defaults, strict=True):
        if default is None:
            yield keyword


class DeprecatedArgumentIssueFinder:  # pylint: disable=too-few-public-methods
    def __init__(self, context: Context) -> None:
        self.project = context.project

    def __call__(self, node: AST) -> Generator[Issue]:
        assert isinstance(node, ClassDef)
        version = self.project.frozen_requirements.get("scrapy")
        if version is None:
            return
        for child in node.body:
            if not isinstance(child, (AsyncFunctionDef, FunctionDef)):
                continue
            deprecated_arguments = DEPRECATED_ARGUMENTS.get(child.name)
            if not deprecated_arguments:
                continue
            for argument in iter_required_args(child.args):
                versioning = deprecated_arguments.get(argument.arg)
                if versioning is None:
                    continue
                deprecated_in = versioning.deprecated_in
                assert isinstance(deprecated_in, Version)
                if version < deprecated_in:
                    continue
                yield Issue(
                    DEPRECATED_ARGUMENT,
                    Pos.from_node(argument),
                    f"deprecated in scrapy {deprecated_in}; "
                    f"{versioning.sunset_guidance}",
                )


class DeprecatedMethodIssueFinder:
    """Report calls to deprecated Scrapy methods.

    Handles ``ImportFrom`` nodes to learn the local names of the classes those
    methods belong to, and ``Call`` nodes to report the calls themselves.
    """

    def __init__(self) -> None:
        self.form_request_names = {"FormRequest"}

    def __call__(self, node: AST) -> Generator[Issue]:
        if isinstance(node, ImportFrom):
            self.track_import(node)
            return
        assert isinstance(node, Call)
        func = node.func
        if (
            isinstance(func, Attribute)
            and func.attr == "from_response"
            and self.is_form_request(func.value)
        ):
            yield Issue(DEPRECATED_METHOD, Pos.from_node(node), FROM_RESPONSE_DETAIL)

    def track_import(self, node: ImportFrom) -> None:
        if not node.module or node.module.split(".")[0] != "scrapy":
            return
        for alias in node.names:
            if alias.name == "FormRequest" and alias.asname:
                self.form_request_names.add(alias.asname)

    def is_form_request(self, node: expr) -> bool:
        if isinstance(node, Name):
            return node.id in self.form_request_names
        return (
            isinstance(node, Attribute)
            and node.attr == "FormRequest"
            and import_path_from_attribute(node.value)
            in VALID_REQUEST_IMPORT_PATHS["FormRequest"]
        )
