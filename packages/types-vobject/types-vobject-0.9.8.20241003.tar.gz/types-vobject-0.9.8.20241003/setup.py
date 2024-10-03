from setuptools import setup

name = "types-vobject"
description = "Typing stubs for vobject"
long_description = '''
## Typing stubs for vobject

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`vobject`](https://github.com/eventable/vobject) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`vobject`.

This version of `types-vobject` aims to provide accurate annotations
for `vobject==0.9.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/vobject. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`8acc85dbabb93619291ecd1bd0271d5e1e55f9ee`](https://github.com/python/typeshed/commit/8acc85dbabb93619291ecd1bd0271d5e1e55f9ee) and was tested
with mypy 1.11.2, pyright 1.1.383, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="0.9.8.20241003",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/vobject.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['vobject-stubs'],
      package_data={'vobject-stubs': ['__init__.pyi', 'base.pyi', 'behavior.pyi', 'change_tz.pyi', 'hcalendar.pyi', 'icalendar.pyi', 'ics_diff.pyi', 'vcard.pyi', 'win32tz.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
