# Scan From PDF utility

## The Python Script
The python script will extract pages from a PDF file as images and run the Tesseract scanner against each page, generating a series of page_####.txt files as output. The process typically takes between twenty to thirty seconds per page, depending on the size of the page and density of text.

The controls for the script are:

scan_from_pdf.py
All command line arguments are optional:

  -h, --help        show this help message and exit

  -f <PDF-file> [<PDF-file> ...]  PDF Filenames
        This specifies the files to be scanned. If left empty, it will attempt scan all documents with a *.pdf file type in the target input diretory. Filenames may specify a directory path. If the -i Input Directory option is also used, then this path specification is appended to the input directory.

  -i <Input Directory>  Input Directory containing input PDF files
        The directory from which all PDF files to be scanned will be read. By default, it will either use the current directory or the path specified in the -f file specification.

  -o <Output Directory> Output Directory for collections of text files
        The directory to which all scanned results will be output. If not specified, they will be written to the current directory. The results of PDF scan operation 

  -r <resolution>   Image resolution in dpi (at least 100, 600+ recommended)
        The resolution of the output image, in dpi (dots per inch). Note that a high DPI does not improve the quality of the image if it already has a low resolution. In general, a resolution of at least 600 dpi is recommended.

  -l <language code>  Language being scanned
       The language of the document(s) being scanned, in three-character ISO-639-2 code. Default is "eng" (English).

  -p <page number>  Start page number (default is 0)
       Page number used in the output files. This could be useful if you know that all of your documents start on page 1, for example. The default is 0, meaning the first page will be stored in "page_0000.txt".

  -d                Turn on Debug messages
       If this is specified, then debugging messages are written to the screen, tracking the operations.

## Running the Script From Condor

## Issues
