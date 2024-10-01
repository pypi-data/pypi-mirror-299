# Taipan

Taipan is a simple imperative programming language.

## Requirements

- [Python 3.12](https://www.python.org/downloads/release/python-3120/) or later
- [clang](https://clang.llvm.org/)
- [clang-format](https://clang.llvm.org/docs/ClangFormat.html) (optional)

## Install

```bash
pip install taipan-lang
```

## Usage

### Build

```bash
taipan build <file>
```

### Build to C

```bash
taipan compile -c <file>
```

### Run

```bash
taipan run <file>
```

### Help

```bash
taipan --help
```

## Development

### Requirements

- [Poetry](https://python-poetry.org/docs/)

### install

```bash
poetry install
pre-commit install
```

### Run

```bash
poetry run taipan ...
```

### Test

```bash
poetry run pytest
```
