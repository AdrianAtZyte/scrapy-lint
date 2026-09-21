from __future__ import annotations

from packaging.version import Version

from scrapy_lint.imports import ImportedObject
from scrapy_lint.versions import UNKNOWN_UNSUPPORTED_VERSION, Versioning


def _discouraged(
    deprecated_in: str,
    sunset_guidance: str | None = None,
) -> ImportedObject:
    """Return an entry that is already worth dropping on any supported
    version, e.g. an implementation detail, or one whose replacement predates
    the deprecation."""
    return ImportedObject(
        versioning=Versioning(
            deprecated_in=Version(deprecated_in),
            sunset_guidance=sunset_guidance,
        ),
        discouraged_in=UNKNOWN_UNSUPPORTED_VERSION,
    )


_FORM_REQUEST = ImportedObject(
    versioning=Versioning(
        deprecated_in=Version("2.16.0"),
        undeprecated_in=Version("2.17.0"),
        sunset_guidance="use the form2request library instead",
    ),
)
_INTERNAL_2_15 = _discouraged("2.15.0")
_INTERNAL_2_17 = _discouraged("2.17.0")
_MAYBE_DEFERRED = _discouraged(
    "2.14.0",
    "use twisted.internet.defer.maybeDeferred instead",
)
_SUNSET_2_16 = Versioning(
    deprecated_in=Version("2.13.0"),
    removed_in=Version("2.16.0"),
)
_REMOVED_IN_2_16 = ImportedObject(versioning=_SUNSET_2_16)

# Functions of w3lib.url that scrapy.utils.url re-exported.
_W3LIB_URL_FUNCTIONS = (
    "add_or_replace_parameter",
    "add_or_replace_parameters",
    "any_to_uri",
    "canonicalize_url",
    "file_uri_to_path",
    "is_url",
    "parse_data_uri",
    "parse_url",
    "path_to_file_uri",
    "safe_download_url",
    "safe_url_string",
    "url_query_cleaner",
    "url_query_parameter",
)

# Import paths of modules and objects that have been deprecated or removed. An
# entry for a module covers every object within it.
IMPORTS = {
    "scrapy.FormRequest": _FORM_REQUEST,
    "scrapy.core.downloader.contextfactory.AcceptableProtocolsContextFactory": (
        _INTERNAL_2_15
    ),
    "scrapy.core.downloader.contextfactory.ScrapyClientContextFactory": _INTERNAL_2_15,
    "scrapy.core.downloader.contextfactory.load_context_factory_from_settings": (
        _INTERNAL_2_15
    ),
    "scrapy.core.downloader.handlers.http": _discouraged(
        "2.14.0",
        "import HTTP11DownloadHandler from scrapy.core.downloader.handlers.http11 "
        "instead",
    ),
    "scrapy.core.downloader.handlers.http10": _REMOVED_IN_2_16,
    "scrapy.core.downloader.tls.DEFAULT_CIPHERS": _INTERNAL_2_17,
    "scrapy.core.downloader.tls.METHOD_TLS": _INTERNAL_2_17,
    "scrapy.core.downloader.tls.METHOD_TLSv10": _INTERNAL_2_17,
    "scrapy.core.downloader.tls.METHOD_TLSv11": _INTERNAL_2_17,
    "scrapy.core.downloader.tls.METHOD_TLSv12": _INTERNAL_2_17,
    "scrapy.core.downloader.tls.ScrapyClientTLSOptions": _INTERNAL_2_15,
    "scrapy.core.downloader.tls.openssl_methods": _INTERNAL_2_17,
    "scrapy.core.downloader.webclient": _REMOVED_IN_2_16,
    "scrapy.downloadermiddlewares.ajaxcrawl": _REMOVED_IN_2_16,
    "scrapy.extensions.statsmailer.StatsMailer": ImportedObject(
        versioning=Versioning(
            deprecated_in=Version("2.15.0"),
            sunset_guidance=(
                "handle the spider_closed signal to send your own notifications instead"
            ),
        ),
    ),
    "scrapy.http.FormRequest": _FORM_REQUEST,
    "scrapy.http.request.form": _FORM_REQUEST,
    "scrapy.mail.MailSender": ImportedObject(
        versioning=Versioning(
            deprecated_in=Version("2.15.0"),
            sunset_guidance=(
                "use smtplib, twisted.mail.smtp or a third-party email library instead"
            ),
        ),
    ),
    "scrapy.spiders.init": _REMOVED_IN_2_16,
    "scrapy.utils.decorators.defers": _MAYBE_DEFERRED,
    "scrapy.utils.defer.defer_fail": _discouraged(
        "2.14.0",
        "use twisted.internet.defer.fail instead",
    ),
    "scrapy.utils.defer.defer_result": _discouraged(
        "2.14.0",
        "use twisted.internet.defer.succeed or twisted.internet.defer.fail instead",
    ),
    "scrapy.utils.defer.defer_succeed": _discouraged(
        "2.14.0",
        "use twisted.internet.defer.succeed instead",
    ),
    "scrapy.utils.defer.mustbe_deferred": _MAYBE_DEFERRED,
    "scrapy.utils.misc.walk_modules": ImportedObject(
        versioning=Versioning(
            deprecated_in=Version("2.15.0"),
            sunset_guidance="use walk_modules_iter() instead",
        ),
    ),
    "scrapy.utils.python.MutableChain": ImportedObject(
        versioning=Versioning(deprecated_in=Version("2.16.0")),
    ),
    "scrapy.utils.ssl.ffi_buf_to_string": _INTERNAL_2_17,
    "scrapy.utils.ssl.get_temp_key_info": _INTERNAL_2_17,
    "scrapy.utils.ssl.x509name_to_string": _INTERNAL_2_17,
    "scrapy.utils.test.TestSpider": _REMOVED_IN_2_16,
    "scrapy.utils.test.assert_gcs_environ": _REMOVED_IN_2_16,
    "scrapy.utils.test.get_ftp_content_and_delete": _REMOVED_IN_2_16,
    "scrapy.utils.test.get_gcs_content_and_delete": _REMOVED_IN_2_16,
    "scrapy.utils.test.mock_google_cloud_storage": _REMOVED_IN_2_16,
    "scrapy.utils.test.skip_if_no_boto": _REMOVED_IN_2_16,
    "scrapy.utils.testproc": _REMOVED_IN_2_16,
    "scrapy.utils.testsite": _REMOVED_IN_2_16,
    "scrapy.utils.url.escape_ajax": _REMOVED_IN_2_16,
    **{
        f"scrapy.utils.url.{name}": ImportedObject(
            versioning=_SUNSET_2_16,
            replacement=f"w3lib.url.{name}",
        )
        for name in _W3LIB_URL_FUNCTIONS
    },
    "scrapy.utils.versions.scrapy_components_versions": ImportedObject(
        versioning=_SUNSET_2_16,
        replacement="scrapy.utils.versions.get_versions",
    ),
}
