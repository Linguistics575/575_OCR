import os
import sys
import argparse



argparser = argparse.ArgumentParser(description = 'Scan PDF images and place pages into directory')
argparser.add_argument('filename', metavar='PDF', nargs='+', help='PDF File')
argparser.add_argument('-r', type=int, default=600, help='Image resolution (at least 100, 600+ recommended)')
argparser.add_argument('-d', type=str, default='', help='Directory containing input PDF files')
argparser.add_argument('-o', type=str, default='', help='Directory containing Output collections of text files')
argparser.add_argument('-p', type=int, default=0, help='Start page number (default is 0)')

args = argparser.parse_args()
convert_cmd = 'convert -density %d %s -strip -background white -alpha off %s'
page_count_cmd = "pdfinfo %s | grep 'Pages' | awk '{print $2}'"

for fname in args.filename:

    if len(args.o) > 0:
        if not os.path.exists(args.o):
            sys.stderr.write('ERROR: Directory "%s" does not exist\n' % args.o)
            sys.stderr.flush()
            raise OSError

    if len(args.d) > 0:
        if not os.path.exists(args.d):
            sys.stderr.write('ERROR: Directory "%s" does not exist\n' % args.d)
            sys.stderr.flush()
            raise OSError

    if fname[-4:].lower() == '.pdf':

        if len(args.d) > 0:
            pdfFilePath = os.path.join(args.d, fname)
        else:
            pdfFilePath = fname

        pdf_page_count_cmd = page_count_cmd % pdfFilePath
        pageCount = int(os.popen(pdf_page_count_cmd).read().strip())
        # pdfFile = open(pdfFilePath, 'rb')
        # pdfreader = PdfFileReader(pdfFile)

        if len(args.o) > 0:
            output_directory = os.path.join(args.o, os.path.basename(fname)[:-4])
        else:
            output_directory = fname[:-4]

        if not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)
            except OSError as e:
                raise

        for pageno in range(args.p, args.p + pageCount):
            text_filename = 'page_%04d' % pageno
            output_filename = text_filename + '.tiff'
            input_filepage = '%s[%d]' % (pdfFilePath, pageno)

            output_filepath = os.path.join(output_directory, output_filename)
            os.system(convert_cmd % (args.r,
                                     input_filepage.replace(' ', '\\ ').replace('-','\\-'),
                                     output_filepath.replace(' ', '\\ ').replace('-','\\-')))

            text_filepath = os.path.join(output_directory, text_filename)
            os.system('tesseract %s -l eng %s' % (output_filepath.replace(' ', '\\ '),
                                                  text_filepath.replace(' ', '\\ ')))
            os.remove(output_filepath)