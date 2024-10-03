from setuptools import setup

name = "types-Flask-SocketIO"
description = "Typing stubs for Flask-SocketIO"
long_description = '''
## Typing stubs for Flask-SocketIO

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Flask-SocketIO`](https://github.com/miguelgrinberg/flask-socketio) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`Flask-SocketIO`.

This version of `types-Flask-SocketIO` aims to provide accurate annotations
for `Flask-SocketIO==5.4.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/Flask-SocketIO. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`e9c7346b0eefe1a1ab6536b1afd17b8d33acfa30`](https://github.com/python/typeshed/commit/e9c7346b0eefe1a1ab6536b1afd17b8d33acfa30) and was tested
with mypy 1.11.2, pyright 1.1.382.post1, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="5.4.0.20241002",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Flask-SocketIO.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['Flask>=0.9'],
      packages=['flask_socketio-stubs'],
      package_data={'flask_socketio-stubs': ['__init__.pyi', 'namespace.pyi', 'test_client.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
