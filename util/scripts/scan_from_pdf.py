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

def count_pages():
    pdf_page_count_cmd = page_count_cmd % pdfFilePath
    return int(os.popen(pdf_page_count_cmd).read().strip())

def file_base_name(pdfFilePath):
    return os.path.basename(pdfFilePath)[:-4]


outputDirectory = confirm_directory_exists(args.o)
inputDirectory = confirm_directory_exists(args.d)

for fname in args.filename:
    if fname[-4:].lower() == '.pdf':
        pdfFilePath = os.path.join(inputDirectory, fname)
        pdfFileBaseName = os.path.basename(pdfFilePath)[:-4]

        if not confirm_file_exists(pdfFilePath):
            break

        pageCount = count_pages()
        if args.g:
            print ('generating %d image files' % pageCount)

        document_output_directory = os.path.join(outputDirectory, pdfFileBaseName)
        create_directory_if_not_exists(document_output_directory)

        pageno = args.p
        fileCanReadImage = True
        while pageno in range(args.p, args.p + pageCount) and fileCanReadImage:
            text_filename = 'page_%04d' % pageno
            output_filename = text_filename + '.tiff'
            input_filepage = '%s[%d]' % (pdfFilePath, pageno)

            output_filepath = os.path.join(document_output_directory, output_filename)
            if args.g:
                print(convert_cmd % (args.r,
                                     input_filepage.replace(' ', '\\ '),
                                     output_filepath.replace(' ', '\\ ')))
            try :
                os.system(convert_cmd % (args.r,
                                     input_filepage.replace(' ', '\\ '),
                                     output_filepath.replace(' ', '\\ ')))
            except Exception as e:
                print('Caught Convert Exception: %s' % e)
                raise e

            if not os.path.exists(output_filepath):
                print('ERROR : Could not create image file "%s"' % output_filepath)
                fileCanReadImage = False
                break
            else:
                text_filepath = os.path.join(document_output_directory, text_filename)
                if args.g:
                    print('tesseract %s -l eng %s' % (output_filepath.replace(' ', '\\ '),
                                                  text_filepath.replace(' ', '\\ ')))
                os.system('tesseract %s -l eng %s' % (output_filepath.replace(' ', '\\ '),
                                                  text_filepath.replace(' ', '\\ ')))
                os.remove(output_filepath)
                pageno += 1
