# Jupyter notebook cell format

Notebooks (`.ipynb`) are JSON. Follow these rules when programmatically creating or editing cells.

## Top-level shape

```json
{
  "cells": [],
  "metadata": {},
  "nbformat": 4,
  "nbformat_minor": 2
}
```

## Cell shapes

```json
// Code cell
{
  "cell_type": "code",
  "execution_count": null,
  "metadata": {},
  "outputs": [],
  "source": ["line 1\n", "line 2\n"]
}

// Markdown cell
{
  "cell_type": "markdown",
  "metadata": {},
  "source": ["# Heading\n", "\n", "Body.\n"]
}

// Raw cell
{
  "cell_type": "raw",
  "metadata": {},
  "source": ["unprocessed text\n"]
}
```

## Required metadata block

```json
"metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {
    "codemirror_mode": {"name": "ipython", "version": 3},
    "file_extension": ".py",
    "mimetype": "text/x-python",
    "name": "python",
    "nbconvert_exporter": "python",
    "pygments_lexer": "ipython3",
    "version": "3.12.10"
  }
}
```

## Editing rules

1. Read the entire notebook before any change.
2. Treat the file as JSON; never append text directly.
3. Make targeted edits to specific cells; preserve overall structure.
4. `source` is a list of strings (newline-terminated for non-final lines).
5. For code cells, preserve `execution_count` and `outputs` unless intentionally clearing.
6. Write back the complete document.

## Validation

After any edit:
- File must parse with `json.load`.
- `nbformat` ≥ 4, `nbformat_minor` present.
- Every cell has `cell_type`, `metadata`, `source`.
- Code cells additionally have `execution_count` and `outputs`.
