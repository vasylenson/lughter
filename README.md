# Spreadsheet processor for Lught BV

## Usage

1. `git clone` this repo, or just download the `src/` folder.
2. Make sure that `src/main.py` is executable (interpreter shebang is included for unix-like OSes)
3. Run in the command line with the path to the source `.csv` file as an argument

```bsh
src/main.py <path to csv>
```

```bsh
./main.py <path to csv>
```

Alternatively, run with a Python 3 interpreter, e.g.:

```bsh
python3 main.py <path to csv>
```

## Processing spec

### General shape of the output

The output is an `.xlsx` document with the following sheets:

- Water flow report
- Temperature report
- Power report
