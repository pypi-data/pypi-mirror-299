from setuptools import setup, find_packages

setup(
    name="docxhtml-converter",  # The package name
    version="0.1.1",  # Version number
    author="Marl Nox",  # Your name
    author_email="marlind.maksuti@gmail.com",  # Your email
    description="A package to convert DOCX to HTML and HTML to DOCX with formatting preservation.",
    long_description=open("README.md").read(),  # Detailed project description from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/MarlNox/docxhtml-converter",  # URL to the project’s repo
    packages=find_packages(),  # Automatically find all packages inside directories with __init__.py
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "python-docx",
        "beautifulsoup4",
    ],  # External packages as dependencies
    python_requires='>=3.6',  # Minimum Python version
    entry_points={
        "console_scripts": [
            "docx-to-html=docxhtml_converter.docxhtml:htmlifier",
            "html-to-docx=docxhtml_converter.htmldocx:docxifier",
        ],
    },  # Entry points for command-line use
)

