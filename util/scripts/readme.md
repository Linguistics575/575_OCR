# Scan From PDF utility

## The Python Script
The python script will extract pages from a PDF file as images and run the Tesseract scanner against each page, generating a series of page_####.txt files as output. The process typically takes between twenty to thirty seconds per page, depending on the size of the page and density of text.

The controls for the script are:
```
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
```
## Running the Script From Condor
### The Condor Command File
Since scanning a 500-page document could possibly take as much as four hours to complete, it is best to run the scanning utility on Condor so that it runs in the background. This cuts down on overuse of the server and lets you do other work while the scan is taking place. 

In the directory, you can see a sample SCAN_ALL.cmd file. This provides the instructions to Condor to let it know what to do. To scan the documents you are interseted in, you need to modify the "arguments" setting in the file. An example looks like this:


```
arguments	= "-i sample -o tmp -r 800 -f sample_journal.pdf"
```

This will read the file in "sample/sample_journal.pdf" and output the results to the directory "tmp/sample_journal", creating the sample_journal directory if necessary. To read your files, change the Input directory (-i value) and Files (-f values). For example, to read the files "file1.pdf" and "file2.pdf" from a directory called "myRepsitory" on your account, the arguments would look something like this:

```
arguments	= "-i /home/myAccount/myRepository -o /home/myAccount/myScannedFiles -r 800 -f file1.pdf file2.pdf"
```

If you want to read all of the PDF files in one directory, set the -i value to that directory, and leave out the -f value, like this:

```
arguments      = "-i /home/myAccount/myRepository -o/home/myAccount/myScannedFiles -r 800"
```

### Running the Condor Process
Once you have set the arguments as you want them, type the command:

    $ condor_submit SCAN_ALL.cmd

This will start the process in the background.

To see the status of the process, type the command:

    $ condor_q

and look for your account ID in the list of processes. The entry should look something like this:

```
OWNER    BATCH_NAME      SUBMITTED   DONE   RUN    IDLE   HOLD  TOTAL JOB_IDS
. . .
lindbe2  CMD: scan_al   5/17 11:21      _      1      _      _      1 103814.0
```

You will usually see a "1" under "IDLE" early on. To make sure it is working correctly, it is a good idea to wait until the condor_q command shows this under "RUN", telling you the process has started.

If the process ends early, the errors will be listed in the file "scan.err".


## Issues
### Tesseract Warning Messages
Some warnings will be reported by the scanner ("Tesseract") which are ignorable, but unfortunately cannot be prevented from being written to the scan.err file. These can look something like this:

```
Warning in pixReadFromTiffStream: bpp = 48; stripping 16 bit rgb samples down to
 8
Page 1
Warning in pixReadMemTiff: tiff page 1 not found
```

### ImageMagick GhostScript incompatibilities
Due to some issues with the image extraction code, which calls the ImageMagick application, and the current version of GhostScript on Patas, some PDF files cannot be read on Patas. If this happens, the error will be reported in the log file in the document output directory.

```
Could not create image files from "tmp/sample_journal/page_0000.tiff"
    Abandonining text extraction.
```
If this happens, it is possible to extract the image files outside of patas and then move them to the server to be scanned. This could take up a lot of memory for each document, depending on the number of pages being read and the desired resolution, so it is recommended to extract one document at a time this way.