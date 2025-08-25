# JUPYTER NOTEBOOK FORMAT STRUCTURE

## Overview

Jupyter notebooks (.ipynb files) are JSON documents with a specific structure that combines executable code, rich text, visualizations, and other media in a single document. Understanding this structure is essential when using Amazon Q Dev to create or modify notebooks.

## Basic Structure

A Jupyter notebook has the following main components:

```json
{
  "cells": [
    // Array of cell objects
  ],
  "metadata": {
    // Notebook metadata
  },
  "nbformat": 4,
  "nbformat_minor": 5
}
```

## Cell Types

### Code Cell

```json
{
  "cell_type": "code",
  "execution_count": null,
  "metadata": {},
  "outputs": [],
  "source": [
    "# This is a code cell",
    "print('Hello world')"
  ]
}
```

### Markdown Cell

```json
{
  "cell_type": "markdown",
  "metadata": {},
  "source": [
    "# This is a markdown cell",
    "Regular text goes here"
  ]
}
```

### Raw Cell

```json
{
  "cell_type": "raw",
  "metadata": {},
  "source": [
    "This content will not be processed"
  ]
}
```

## Metadata Structure

```json
"metadata": {
  "kernelspec": {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
  },
  "language_info": {
    "codemirror_mode": {
      "name": "ipython",
      "version": 3
    },
    "file_extension": ".py",
    "mimetype": "text/x-python",
    "name": "python",
    "nbconvert_exporter": "python",
    "pygments_lexer": "ipython3",
    "version": "3.8.10"
  }
}
```

## How Amazon Q Dev Should Handle Jupyter Notebooks

When Amazon Q Dev needs to modify Jupyter notebooks, it should follow these important practices:

### 1. Read the Entire Notebook First

Before making any changes, Amazon Q Dev should read the entire notebook file to understand its complete structure. This is crucial because notebooks are JSON documents, not simple text files.

### 2. Understand the Complete Structure

Amazon Q Dev needs to fully comprehend the notebook's structure before making changes:
- The cells array and its contents
- The metadata section
- The nbformat and nbformat_minor versions

### 3. Modifying Notebooks

When modifying a notebook, Amazon Q Dev should:

#### For Creating a New Notebook:
- Create a complete JSON structure with all required elements
- Include proper cells array, metadata, and format information
- Ensure the notebook has valid cell structures for each cell type

#### For Updating an Existing Notebook:
- Read the entire notebook first
- Make targeted changes to specific cells or add new cells
- Preserve the overall JSON structure
- Only modify cell content as needed while preserving the metadata section
- Always maintain the metadata at the end of the file after all cells (including any newly appended cells) to ensure notebook compatibility
- Write back the complete notebook with all changes

#### For Replacing Content in a Notebook:
- Identify the specific cells or content to replace
- Ensure replacements maintain the proper JSON structure
- Keep the metadata section intact
- Verify the resulting notebook is valid JSON

### 4. Common Mistakes to Avoid

- **Never append text directly**: Notebooks are JSON documents, not text files
- **Don't make partial updates**: Always work with the complete notebook structure
- **Maintain proper cell structure**: Each cell must have the required fields
- **Handle source fields correctly**: The "source" field should be a list of strings
- **Preserve execution counts**: For code cells, maintain execution_count values

### 5. Best Practices

- Always validate the resulting JSON structure
- Ensure cells are in the correct order
- Maintain the relationship between cells when making changes
- Preserve important metadata that might be used by Jupyter extensions
- When adding new cells, follow the existing notebook's style and formatting

## Conclusion

Understanding the Jupyter notebook format is essential for Amazon Q Dev when creating or modifying notebooks. By treating notebooks as complete JSON documents and following the practices outlined above, Amazon Q Dev can make reliable and effective changes to notebook files.
