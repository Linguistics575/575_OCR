import PyPDF2 as pdf
import os
import argparse
import sys

from wand.image import Image

# Extract each page of the JPG files entered as a directory of JPG image files
# The files to be extracted can be entered as a list. The output will appear
# in directories identically named to the file (minus the ".pdf" extension.
#
# Resolution defaults to 250 and may be modified with the "-r" command line option.
# In general, resolution below 100 will not be useful. Of course, the JPG file sizes
# will increase with the resolution. In general, a resolution of 250 to 400 seems to
# be readable for most of the PDF files in the system. Some continue to have problems,
# particularly the Egyptian Gazettes and some of the Baedeckers.

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