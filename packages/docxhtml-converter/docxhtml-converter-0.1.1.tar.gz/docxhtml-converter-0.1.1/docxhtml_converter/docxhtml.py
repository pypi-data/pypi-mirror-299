from docx import Document
from docx.oxml import CT_Tbl, CT_P  # For identifying tables and paragraphs
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.paragraph import Paragraph
from docx.table import Table
import html

def iter_block_items(parent):
    """
    Yield each paragraph and table child within parent, in document order.
    Each returned value is an instance of either Table or Paragraph.
    """
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def get_html_from_docx(docx_file):
    # Load the document
    doc = Document(docx_file)
    
    html_output = ""
    list_type = None  # Tracks current list type: 'ul', 'ol', or None
    
    # Function to process a single paragraph into HTML
    def process_paragraph(para, in_list=False):
        nonlocal html_output
        para_html = ""

        # Get paragraph alignment
        alignment = para.alignment
        alignment_str = ""

        # Map alignment to CSS
        if alignment == WD_ALIGN_PARAGRAPH.LEFT:
            alignment_str = "text-align: left;"
        elif alignment == WD_ALIGN_PARAGRAPH.CENTER:
            alignment_str = "text-align: center;"
        elif alignment == WD_ALIGN_PARAGRAPH.RIGHT:
            alignment_str = "text-align: right;"
        elif alignment == WD_ALIGN_PARAGRAPH.JUSTIFY:
            alignment_str = "text-align: justify;"

        # Handle indentation
        indent = ""
        if para.paragraph_format.left_indent:
            indent += f"padding-left: {para.paragraph_format.left_indent.pt}px;"
        if para.paragraph_format.right_indent:
            indent += f"padding-right: {para.paragraph_format.right_indent.pt}px;"

        # Get font properties for each run in the paragraph
        def get_font_style(run):
            font_style = ""
            if run.font.name:
                font_style += f"font-family: {run.font.name};"
            if run.font.size:
                font_style += f"font-size: {run.font.size.pt}pt;"
            if run.font.color and run.font.color.rgb:
                font_style += f"color: #{run.font.color.rgb};"
            return font_style

        # Check if the paragraph is a heading
        if para.style.name.startswith('Heading') or para.style.name.startswith('Title'):
            para_html += f'<p style="{alignment_str} {indent}"><strong>'
        else:
            para_html += f'<p style="{alignment_str} {indent}">'

        # Iterate over each run in the paragraph
        for run in para.runs:
            # Get font style for the current run
            font_style = get_font_style(run)
            run_text = html.escape(run.text)

            # Check if bold and italic and apply tags accordingly
            if run.bold and run.italic:
                para_html += f'<strong><em style="{font_style}">{run_text}</em></strong>'
            elif run.bold:
                para_html += f'<strong style="{font_style}">{run_text}</strong>'
            elif run.italic:
                para_html += f'<em style="{font_style}">{run_text}</em>'
            else:
                para_html += f'<span style="{font_style}">{run_text}</span>'

        # Close the paragraph tag, and close the strong tag if it's a heading
        if para.style.name.startswith('Heading') or para.style.name.startswith('Title'):
            para_html += '</strong></p>\n'
        else:
            para_html += '</p>\n'

        return para_html

    # Function to handle tables
    def handle_table(table):
        table_html = "<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; width: 100%;'>\n"
        for row in table.rows:
            table_html += "<tr>\n"
            for cell in row.cells:
                # Start table cell
                table_html += "<td style='vertical-align: top;'>"
                cell_html = ""
                for cell_para in cell.paragraphs:
                    cell_html += process_paragraph(cell_para)
                table_html += cell_html
                table_html += "</td>\n"
            table_html += "</tr>\n"
        table_html += "</table>\n"
        return table_html

    # Iterate over the body elements
    for block in iter_block_items(doc):
        if isinstance(block, Table):
            # Close any open list before inserting a table
            if list_type:
                if list_type == 'ul':
                    html_output += "</ul>\n"
                elif list_type == 'ol':
                    html_output += "</ol>\n"
                list_type = None

            html_output += handle_table(block)
            continue

        if isinstance(block, Paragraph):
            para = block

            # Determine if the paragraph is part of a list
            if para.style.name.startswith('List Bullet'):
                current_list = 'ul'
            elif para.style.name.startswith('List Number'):
                current_list = 'ol'
            else:
                current_list = None

            # Manage list tags
            if current_list != list_type:
                if list_type:
                    # Close the previous list
                    if list_type == 'ul':
                        html_output += "</ul>\n"
                    elif list_type == 'ol':
                        html_output += "</ol>\n"
                if current_list:
                    # Open a new list
                    if current_list == 'ul':
                        html_output += "<ul>\n"
                    elif current_list == 'ol':
                        html_output += "<ol>\n"
                list_type = current_list

            # Start list item or paragraph
            if list_type:
                html_output += "<li>"
                # Iterate over runs and process
                for run in para.runs:
                    font_style = get_font_style(run)
                    run_text = html.escape(run.text)

                    # Check if bold and italic and apply tags accordingly
                    if run.bold and run.italic:
                        html_output += f'<strong><em style="{font_style}">{run_text}</em></strong>'
                    elif run.bold:
                        html_output += f'<strong style="{font_style}">{run_text}</strong>'
                    elif run.italic:
                        html_output += f'<em style="{font_style}">{run_text}</em>'
                    else:
                        html_output += f'<span style="{font_style}">{run_text}</span>'
                
                html_output += "</li>\n"
            else:
                # Process as a regular paragraph
                html_output += process_paragraph(para)

    # Close any remaining open list after processing all blocks
    if list_type:
        if list_type == 'ul':
            html_output += "</ul>\n"
        elif list_type == 'ol':
            html_output += "</ol>\n"

    # Wrap the content in a container div with A4 width
    complete_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Converted Document</title>
</head>
<body>
    <div style="max-width: 210mm; margin: auto; padding: 10mm;">
        {html_output}
    </div>
</body>
</html>"""

    return complete_html


def htmlifier(docx_path, output_html):
    

    html_content = get_html_from_docx(docx_path)

    # Save HTML content to a file
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("HTML file with tables, indentation, and lists generated successfully!")
