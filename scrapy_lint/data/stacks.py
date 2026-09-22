from packaging.version import Version

from scrapy_lint.data.python import STACK_PYTHON

# Feature version of Scrapy that the newest Scrapy Cloud stack comes with.
# Stacks with a suffix, e.g. 1.5-slim, are variants of an unsuffixed stack.
LATEST_STACK_SCRAPY_VERSION = max(
    Version(stack) for stack in STACK_PYTHON if "-" not in stack
)
