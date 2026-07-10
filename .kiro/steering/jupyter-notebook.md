---
inclusion: fileMatch
fileMatchPattern: '**/*.ipynb'
---

# Jupyter Notebook editing rules for this workspace

Jupyter notebooks (`.ipynb`) are JSON documents — not text files. Apply these rules whenever you create, read, or modify a notebook in this workspace.

## Notebook structure

```json
{
  "cells": [ /* array of cell objects */ ],
  "metadata": { /* notebook metadata */ },
  "nbformat": 4,
  "nbformat_minor": 2
}
```

When creating a new notebook, match the existing project's `nbformat_minor` (2 in this workspace) unless explicitly told otherwise.

### Cell shapes

```json
// Code cell
{
  "cell_type": "code",
  "execution_count": null,
  "metadata": {},
  "outputs": [],
  "source": ["# This is a code cell\n", "print('hello')\n"]
}

// Markdown cell
{
  "cell_type": "markdown",
  "metadata": {},
  "source": ["# Heading\n", "\n", "Body text here.\n"]
}

// Raw cell
{
  "cell_type": "raw",
  "metadata": {},
  "source": ["This content will not be processed\n"]
}
```

### Required metadata block

The display_name and kernel name reflect the participant's local environment (e.g., `Python 3` / `python3` if installed system-wide, or `venv` if using a project venv). Match what the existing baseline notebook uses; do not invent new kernel names.

```json
"metadata": {
  "kernelspec": {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
  },
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

## Editing workflow

### Before any change

1. **Read the entire notebook** as JSON. Understand the full `cells` array, `metadata` block, and `nbformat` / `nbformat_minor` versions.
2. Identify the exact cell index you intend to add/modify/delete.

### Creating a new notebook

- Emit a complete JSON structure with `cells`, `metadata`, `nbformat`, `nbformat_minor`.
- Each cell must have all required fields for its type.
- Match the workspace's existing `language_info.version` (Python 3.12 here).

### Updating an existing notebook

- Read the current file first.
- Make targeted edits to specific cells; do not rewrite unrelated cells.
- Preserve the overall JSON structure: cell ordering, metadata, format markers.
- Always keep the `metadata` block at its position; do not reorder it relative to `cells`.
- Write back the **complete** notebook (not a fragment).

### Replacing a cell's content

- Identify the cell by index in `cells`.
- Replace the `source` array (list of strings, each ending with `\n` for non-final lines).
- Keep `cell_type` and `metadata` intact.
- For a code cell whose `source` you are actually changing, reset only that cell's `execution_count` to `null` and `outputs` to `[]` (its old output no longer matches the new code). Do **not** touch `execution_count` or `outputs` on any cell you are not editing.

### Appending new cells (the common incremental-lab case)

Each lab adds cells to the participant's existing notebook. The participant has **already run** the earlier cells, so those cells hold real `execution_count` numbers and `outputs`, and the results live in a **still-running kernel** (editing the file on disk does not restart the kernel).

- **Preserve every existing cell byte-for-byte** — `source`, `execution_count`, and `outputs` all unchanged. Only add the new cell objects (at the end, or at the intended index).
- New code cells you add start unrun: `"execution_count": null`, `"outputs": []`.
- **Never** re-serialize the whole notebook with existing cells' `execution_count` reset to `null` or `outputs` emptied. Doing so makes the reloaded notebook look never-run, so the participant needlessly re-runs completed SageMaker Processing/Training/Deploy jobs from scratch even though the kernel state is intact. The correct participant action after an append is to run only the new cells against the live kernel.

## Common mistakes — never do these

- ❌ **Append text directly** — notebooks are JSON, not text files. Always parse and re-serialize.
- ❌ **Partial JSON updates** — work with the complete document.
- ❌ **Drop required cell fields** — every cell type has required keys; missing keys break notebook loaders.
- ❌ **Pass a single string in `source`** — `source` must be a list of strings (or a single string per the spec, but the workshop convention is the list form).
- ❌ **Strip `outputs` or `execution_count` from cells you are not editing.** When appending or making a targeted edit, existing already-run cells must keep their `execution_count` and `outputs`. Clear them only for the specific cell whose `source` you changed, or across the whole notebook **only** when the user explicitly asks for a "clean" notebook.

## Best practices

- Validate the resulting JSON structure (it must parse with `json.load`).
- Cells must be in the intended logical order.
- Preserve metadata fields used by extensions (cell tags, slideshow info, etc.).
- For new cells, match the existing notebook's style: same indentation, same comment density, same code-cell-vs-markdown rhythm.

## v3 SDK reminder

When generating training/processing/inference code inside a notebook cell, follow `.kiro/steering/sagemaker-v3.md`. Do not produce v2-style imports — they will fail at runtime in this workspace's pinned `sagemaker==3.12.0`.
