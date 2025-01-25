# implementing-search-python 

## Installation

```console
pip install . 
```

## Execution

```console
implementing-search-python COMMAND --reference REFERENCE_FILE.FA.GZ --reads READS_FILE.FA.GZ
```
![Usage](./data/usage.png?raw=true)


`COMMAND` can be any of:
* `naive search --reference REFERENCE_FILE.FA.GZ --reads READS_FILE.FA.GZ`
* ` suffix_array search --reference REFERENCE_FILE.FA.GZ --reads READS_FILE.FA.GZ`
* `fm_index construct --reference REFERENCE_FILE.FA.GZ --output OUTPUT_FILE.IDX`
* ` fm_index search --index INDEX.IDX --reads READS_FILE.FA.GZ`

The `fm_index search` command additionally supports `--mismatches` and `--use-pigeon`.

All search commands have a `--quiet` flag which supresses printing match results.


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

