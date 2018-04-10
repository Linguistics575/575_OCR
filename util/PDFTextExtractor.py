import PyPDF2 as pdf
import argparse
import sys

# Python script to extract embedded text from paged PDF files.
# Files to be extracted can be listed in the command line.
# The resulting text files are output to identically named files, with "_text.txt" appended instead of ".pdf"
# The suffix being appended may be modified with the "-x" command line option.

def text_filename(filename, suffix):
    return '%s%s.txt' % (filename[0:filename.rfind('.pdf')], suffix)

argparser = argparse.ArgumentParser(description='Extract existing text pages from a PDF file')
argparser.add_argument('filename', metavar='F', nargs='+', help='PDF File')
argparser.add_argument('-x', default='_text', help='Suffix to place on *.txt file (Defaults to "_text")')
argparser.add_argument('-p', type=int, default=0, help='Start page number (default is 0)')

args = argparser.parse_args()

for fname in args.filename:
    pdfFile = open(fname, 'rb')
    outFile = open(text_filename(fname, args.x), 'w')
    pdfreader = pdf.PdfFileReader(pdfFile)

    sys.stdout.write('%s ==> %s, %d pages\n' % (fname, text_filename(fname, args.x), pdfreader.numPages))
    for pg in range(pdfreader.numPages):
        pageObj = pdfreader.getPage(pg)

        outFile.write('\n===\npg. %d\n---\n%s\n' % (pg+args.p, pageObj.extractText()))
        sys.stdout.write('%d ' % (pg+args.p))
        sys.stdout.flush()