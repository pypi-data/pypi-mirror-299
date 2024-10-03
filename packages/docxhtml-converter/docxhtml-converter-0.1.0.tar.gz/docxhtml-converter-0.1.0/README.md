Updated README.md

# DOCX-HTML Converter

This package provides tools to convert DOCX documents to HTML and HTML back to DOCX, while preserving formatting such as tables, lists, and paragraphs.

## Features

- Convert DOCX to HTML with support for paragraphs, lists, tables, and inline formatting.
- Convert HTML to DOCX with support for lists, tables, inline styles (bold, italic), and more.

## Installation

Install the package via pip after uploading it to PyPI:

```bash
pip install docxhtml-converter

Usage
Convert DOCX to HTML

Use the htmlifier function to convert a DOCX file into HTML:

from docxhtml import htmlifier

docx_path = "document.docx"
output_html = "output.html"
htmlifier(docx_path, output_html)

Convert HTML to DOCX

Use the docxifier function to convert an HTML file back into DOCX:

from htmldocx import docxifier

input_html = "output.html"
output_docx = "regenerated.docx"
docxifier(input_html, output_docx)

These scripts allow you to easily convert between DOCX and HTML formats while maintaining formatting such as tables, lists, and paragraphs.
Example

Here's an example of how you can use both functions in a complete script:

from docxhtml import htmlifier
from htmldocx import docxifier

# Convert DOCX to HTML
docx_path = "document.docx"
output_html = "output.html"
htmlifier(docx_path, output_html)

# Convert HTML back to DOCX
input_html = "output.html"
output_docx = "regenerated.docx"
docxifier(input_html, output_docx)

