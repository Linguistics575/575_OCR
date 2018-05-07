import os
import sys
import argparse



argparser = argparse.ArgumentParser(description = 'Scan PDF images and place pages into directory')
argparser.add_argument('filename', metavar='PDF', nargs='+', help='PDF File')
argparser.add_argument('-r', type=int, default=600, help='Image resolution (at least 100, 600+ recommended)')
argparser.add_argument('-d', type=str, default='', help='Directory containing input PDF files')
argparser.add_argument('-o', type=str, default='', help='Directory containing Output collections of text files')
argparser.add_argument('-p', type=int, default=0, help='Start page number (default is 0)')
argparser.add_argument('-g', action='store_true', default=False)

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

        if not os.path.exists(pdfFilePath):
            sys.stderr.write('ERROR: File "%s" does not exist\n' % pdfFilePath)
            break

        pdf_page_count_cmd = page_count_cmd % pdfFilePath
        if args.g:
            print ('calling %s' % pdf_page_count_cmd)
        pageCount = int(os.popen(pdf_page_count_cmd).read().strip())
        if args.g:
            print ('generating %d image files' % pageCount)

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
            if args.g:
                print(convert_cmd % (args.r,
                                     input_filepage.replace(' ', '\\ '),
                                     output_filepath.replace(' ', '\\ ')))
            try :
                os.system(convert_cmd % (args.r,
                                     input_filepage.replace(' ', '\\ '),
                                     output_filepath.replace(' ', '\\ ')))
            except Excption as e:
                print('Caught Convert Exception: %s' % e)
                raise e

            if not os.path.exists(output_filepath):
                print('ERROR : Could not create image file "%s"' % output_filepath)
                break

            text_filepath = os.path.join(output_directory, text_filename)
            if args.g:
                print('tesseract %s -l eng %s' % (output_filepath.replace(' ', '\\ '),
                                                  text_filepath.replace(' ', '\\ ')))
            os.system('tesseract %s -l eng %s' % (output_filepath.replace(' ', '\\ '),
                                                  text_filepath.replace(' ', '\\ ')))
            os.remove(output_filepath)
