# assignment-01-python

## Installation

```console
pip install assignment-01-python
```


## Execution

```console
assignment-01-python --reference REFERENCE_FILE.FA.GZ --reads READS_FILE.FA.GZ
```
![Usage](./data/usage.png?raw=true)



## Running linter

Formatting can be checked and corrected using:

```
$ hatch fmt
```

## Running type checker

`mypy` can be run to validate types using:

```
$ hatch run types:check
```


## Running unit tests

Unit tests can be run with pytest or using `hatch.

`hatch` can be installed via pip:

```
$ uv pip install hatch
```

Then unit tests can be run with `hatch`:

```
$ hatch run test

