import os
import sys
import argparse



argparser = argparse.ArgumentParser(description = 'Scan PDF images and place pages into directory')
argparser.add_argument('-f', metavar='PDF', nargs='+', help='PDF Filenames')
argparser.add_argument('-r', type=int, default=600, help='Image resolution (at least 100, 600+ recommended)')
argparser.add_argument('-l', type=str, default='eng', help='Language being scanned')
argparser.add_argument('-i', type=str, default='', help='Input Directory containing input PDF files')
argparser.add_argument('-o', type=str, default='', help='Output Directory for collections of text files')
argparser.add_argument('-p', type=int, default=0, help='Start page number (default is 0)')
argparser.add_argument('-d', action='store_true', default=False, help="Turn on Debug messages")

args = argparser.parse_args()
convert_cmd = 'convert -density %d %s -strip -background white -alpha off %s'
page_count_cmd = "pdfinfo %s | grep 'Pages' | awk '{print $2}'"

if args.d:
    print('Received request for scanning:')
    if args.f:
        print('COMMAND: scan_from_pdf.py -r %d -i %s -o %s -p %d -f %s\n' % (args.r, args.i, args.o, args.p, ' '.join(map(str, args.f))))
    else:
        print('COMMAND: scan_from_pdf.py -r %d -i %s -o %s -p %d\n' % (args.r, args.i, args.o, args.p))

def confirm_directory_exists(dir):
    if len(dir) > 0:
        if not os.path.exists(dir):
            sys.stderr.write('ERROR: Directory "%s" does not exist\n' % dir)
            raise FileNotFoundError
        else:
            return dir
    else:
        return ''

def create_directory_if_not_exists(dir):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except OSError as e:
            raise

def confirm_file_exists(filepath):
    if not os.path.exists(filepath):
        sys.stderr.write('ERROR: File "%s" does not exist\n' % filepath)
        return False
    return True

def count_pages(pdfFilePath):
    pdf_page_count_cmd = page_count_cmd % pdfFilePath
    try:
        return int(os.popen(pdf_page_count_cmd).read().strip())
    except ValueError:
        sys.stderr.write('Could not read page count')
        return 0

outputDirectory = confirm_directory_exists(args.o)
inputDirectory = confirm_directory_exists(args.i)

if args.d:
    if len(inputDirectory) > 0:
        print('reading from directory "%s"' % inputDirectory)
    else:
        print('reading from current directory')
    if len(outputDirectory) > 0:
        print('writing to directory "%s"' % outputDirectory)
    else:
        print('writing to current directory')

if not args.f:
    print('reading all files from %s' % inputDirectory)
    fileList = os.listdir(inputDirectory)
else:
    fileList = args.f

if args.d:
    print('reading files: %s' % ' '.join(map(str, fileList)))

for fname in fileList:
    if fname.lower().endswith('pdf'):
        pdfFilePath = os.path.join(inputDirectory, fname)
        pdfFileBaseName = os.path.basename(pdfFilePath)[:-4]

        if not confirm_file_exists(pdfFilePath):
            break

        pageCount = count_pages(pdfFilePath)
        if args.d:
            print ('generating %d image files' % pageCount)

        document_output_directory = os.path.join(outputDirectory, pdfFileBaseName)
        create_directory_if_not_exists(document_output_directory)

        logFile = open(os.path.join(document_output_directory, pdfFileBaseName + '.log'), 'w')

        pageno = args.p
        fileCanReadImage = True

        logFile.write('COMMAND: scan_from_pdf.py -r %d -i %s -o %s -p %d -f %s\n' % (args.r, args.i, args.o, args.p, fname))
        logFile.write('Reading %d pages from "%s"\n' % (pageCount, pdfFileBaseName))
        logFile.write('    resolution %d dpi\n' % args.r)
        logFile.write('    page numbering starts at %d\n' % args.p)
        while pageno in range(args.p, args.p + pageCount) and fileCanReadImage:
            text_filename = 'page_%04d' % pageno
            output_filename = text_filename + '.tiff'
            input_filepage = '%s[%d]' % (pdfFilePath, pageno)

            output_filepath = os.path.join(document_output_directory, output_filename)
            if args.d:
                print(convert_cmd % (args.r,
                                     input_filepage.replace(' ', '\\ '),
                                     output_filepath.replace(' ', '\\ ')))
            try :
                os.system(convert_cmd % (args.r,
                                     input_filepage.replace(' ', '\\ '),
                                     output_filepath.replace(' ', '\\ ')))
            except Exception as e:
                print('Caught Convert Exception: %s' % e)
                logFile.write('ERROR in convert invocation -- aborting command\n')
                logFile.close()
                raise e

            if not os.path.exists(output_filepath):
                sys.stderr.write('ERROR : Could not create image file "%s"\n' % output_filepath)
                logFile.write('Could not create image files from "%s"\n    Abandonining text extraction.' % output_filepath)
                logFile.close()
                fileCanReadImage = False
                break
            else:
                text_filepath = os.path.join(document_output_directory, text_filename)
                if args.d:
                    print('tesseract %s -l %s %s' % (output_filepath.replace(' ', '\\ '),
						  args.l,
                                                  text_filepath.replace(' ', '\\ ')))
                os.system('tesseract %s -l %s %s' % (output_filepath.replace(' ', '\\ '),
                                                  args.l,
                                                  text_filepath.replace(' ', '\\ ')))
                os.remove(output_filepath)

                logFile.write('    page %d\n' % pageno)
                pageno += 1

        logFile.close()
