#------------------------------------------------------------------------
# Run the scan_from_pdf script on
# a the list of *.pdf files provided
# 
# script command description (see scan_from_pdf.py -h)
# usage: scan_from_pdf.py [-h] [-r R] [-d D] [-o O] [-p P] PDF [PDF ...]
#
# Scan PDF images and place pages into directory
#
# positional arguments:
#   PDF         PDF File
#
# optional arguments:
#   -h, --help  show this help message and exit
#   -r R        Image resolution (at least 100, 600+ recommended)
#   -d D        Directory containing input PDF files
#   -o O        Directory containing Output collections of text files
#   -p P        Start page number (default is 0)
#------------------------------------------------------------------------
universe	= vanilla
executable 	= scan_all.sh
getenv		= true
output		= scan.out
error		= scan.err
log		= scan.log
arguments	= "-i /home2/lindbe2/workspace/ling575/HowardCarterNotes -o /home2/lindbe2/workspace/ling575/575_OCR/raw_texts/HowardCarterNotes -r 800"
transfer_executable = false
queue
