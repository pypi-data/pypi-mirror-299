from setuptools import setup

name = "types-waitress"
description = "Typing stubs for waitress"
long_description = '''
## Typing stubs for waitress

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`waitress`](https://github.com/Pylons/waitress) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`waitress`.

This version of `types-waitress` aims to provide accurate annotations
for `waitress==3.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/waitress. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`91a58b07cdd807b1d965e04ba85af2adab8bf924`](https://github.com/python/typeshed/commit/91a58b07cdd807b1d965e04ba85af2adab8bf924) and was tested
with mypy 1.11.1, pyright 1.1.382.post1, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="3.0.0.20241001",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/waitress.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['waitress-stubs'],
      package_data={'waitress-stubs': ['__init__.pyi', 'adjustments.pyi', 'buffers.pyi', 'channel.pyi', 'compat.pyi', 'parser.pyi', 'proxy_headers.pyi', 'receiver.pyi', 'rfc7230.pyi', 'runner.pyi', 'server.pyi', 'task.pyi', 'trigger.pyi', 'utilities.pyi', 'wasyncore.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
