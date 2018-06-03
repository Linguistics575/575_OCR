import PyPDF2 as pdf
import os
import argparse
import sys
import datetime

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
argparser.add_argument('-p', type=int, default=0, help='Start page number (default is 0)')

args = argparser.parse_args()

for fname in args.filename:
    pdfFile = open(fname, 'rb')
    pdfreader = pdf.PdfFileReader(pdfFile)

    endidx = fname.rfind('.pdf')
    dirname = fname[0:endidx]

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    logFile = open(dirname + '.log', 'w')

    sys.stdout.write('%s, %d pages\n' % (fname, pdfreader.numPages))
    logFile.write('Reading file "%s", %d pages, resolution:%d,  %s\n' % (fname, pdfreader.numPages, args.r, datetime.datetime.now().strftime("%I:%M%p, %B %d, %Y")))
    for pg in range(pdfreader.numPages):
        with Image(filename='%s[%d]' % (fname, pg), resolution=args.r) as img:
            img.save(filename='%s/page%d.jpg' % (dirname, (pg+args.p)))
            logFile.write('page %d - w:%d, h:%d\n' % (pg+args.p, img.width, img.height))
        sys.stdout.write('%d ' % (pg + args.p))
        sys.stdout.flush()
    logFile.flush()