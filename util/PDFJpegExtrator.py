import PyPDF2 as pdf
import os
import argparse
import sys

from wand.image import Image

argparser = argparse.ArgumentParser(description='Convert PDF pages to JPG files')
argparser.add_argument('filename', metavar='F', nargs='+', help='PDF File')
argparser.add_argument('-r', type=int, default=250, help='Image resolution (at least 100, 250+ recommended)')

args = argparser.parse_args()

for fname in args.filename:
    pdfFile = open(fname, 'rb')
    pdfreader = pdf.PdfFileReader(pdfFile)

    endidx = fname.rfind('.pdf')
    dirname = fname[0:endidx]

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    sys.stdout.write('%s, %d pages\n' % (fname, pdfreader.numPages))
    for pg in range(pdfreader.numPages):
        with Image(filename='%s[%d]' % (fname, pg), resolution=args.r) as img:
            img.save(filename='%s/page%d.jpg' % (dirname, pg))
        sys.stdout.write('%d ' % (pg + 1))
        sys.stdout.flush()