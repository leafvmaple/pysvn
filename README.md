# pysvn

![PyPI](https://img.shields.io/pypi/v/pysvn)

This is a Python package that can operate `svn`, provide `log`, `diff`, `numstat` operation.

## Install

Binary installers for the latest released version are available at the `Pypi`.

```
python -m pip install --upgrade pysvn
```

## Usage

### Init

> initialize the client on `cwd`

```python
import pysvn

client = pysvn.Client(cwd = os.getcwd(), stdout = subprocess.PIPE)
```

### log

> Show the log messages for a set of revision(s) and/or path(s)..

```python
client.log(decoding = 'utf8')
```

### diff

> Display local changes or differences between two revisions or paths

```python
client.diff(start_version, end_version = None, decoding = 'utf8', cache = False)
```

### numstat

> Shows number of added and deleted lines in decimal notation and pathname

```python
client.numstat(start_version, end_version = None, decoding = 'utf8', cache = False)
```

## License

[BSD](https://github.com/leafvmaple/pysvn/blob/main/LICENSE)