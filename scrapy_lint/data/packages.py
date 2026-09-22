from packaging.version import Version

from scrapy_lint.packages import Package, VersionConflict

PACKAGES = {
    "scrapy": Package(
        highest_known_version=Version("2.19.0"),
        lowest_safe_version=Version("2.17.0"),
        lowest_supported_version=Version("2.0.1"),
    ),
    "scrapy-crawlera": Package(
        replacements=("scrapy-zyte-smartproxy",),
    ),
    "scrapy-splash": Package(
        replacements=("scrapy-playwright", "scrapy-zyte-api"),
    ),
    "scrapy-zyte-api": Package(
        lowest_supported_version=Version("0.5.1"),
    ),
}

VERSION_CONFLICTS = (
    # Lower versions use the binary export mode of PythonItemExporter, removed
    # in Scrapy 2.11.0, and fail with "TypeError: Unexpected options: binary".
    VersionConflict(
        package="scrapy",
        since=Version("2.11.0"),
        dependency="scrapinghub-entrypoint-scrapy",
        lowest_compatible=Version("0.14.1"),
    ),
)
