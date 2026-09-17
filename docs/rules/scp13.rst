.. _scp13:

=====================================
SCP13: Incomplete requirements freeze
=====================================

What it does
============

Finds out if your :ref:`requirements file <requirements>` does not seem to be
fully frozen.


Why is this bad?
================

If you do not freeze all dependencies of your Scrapy project, you risk run time
errors or unexpected behavior when running your project in different
environments.

Use tools like pip-tools_ or poetry-auto-export_ to generate a requirements
file that freezes all your direct and indirect dependencies.

.. _pip-tools: https://pip-tools.readthedocs.io/en/stable/
.. _poetry-auto-export: https://github.com/Ddedalus/poetry-auto-export


Example
=======

.. code-block:: text

    scrapy>=2.17.0

Use instead:

.. code-block:: text

    aiohappyeyeballs==2.7.1
    aiohttp==3.14.3
    aiosignal==1.4.0
    attrs==26.1.0
    automat==25.4.16
    brotli==1.2.0
    certifi==2026.7.22
    cffi==2.1.1
    charset-normalizer==3.5.1
    constantly==23.10.4
    cryptography==50.0.1
    cssselect==1.5.0
    defusedxml==0.7.1
    filelock==3.32.7
    frozenlist==1.8.0
    hyperlink==21.0.0
    idna==3.19
    incremental==24.11.0
    itemadapter==0.13.1
    itemloaders==1.4.0
    jmespath==1.1.0
    lxml==6.1.3
    multidict==6.8.0
    packaging==26.3
    parsel==1.11.0
    platformdirs==4.11.8
    propcache==0.5.4
    protego==0.6.2
    pycparser==3.0
    pydispatcher==2.0.7
    pyopenssl==26.4.0
    queuelib==1.10.0
    requests==2.34.2
    requests-file==3.0.1
    scrapy==2.19.0
    service-identity==26.1.0
    tldextract==5.3.2
    twisted==26.4.0
    typing-extensions==4.16.0
    urllib3==2.8.0
    w3lib==2.4.1
    yarl==1.25.1
    zope-interface==8.6
