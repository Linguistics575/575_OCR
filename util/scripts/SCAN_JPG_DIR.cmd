#------------------------------------------------------------------------
# Run the scan_from_pdf script on
# a the list of *.pdf files provided
# 
# script command description (see scan_from_pdf.py -h)
# usage: scan_from_pdf.py [-h] [-r R] [-i I] [-o O] [-p P] [-l L] [-f F [F ...]] [-g]
#
# Scan PDF images and place pages into directory
#
# optional arguments:
#   -h, --help  show this help message and exit
#   -r R        Image resolution (at least 100, 600+ recommended)
#   -i I        Input Directory containing PDF files
#   -o O        Output Directory to which collections of text files are written
#   -p P        Start page number (default is 0)
#   -l L        Language being read (default is "eng")
#   -f F [F ...] PDF image files to be scanned (default is all)
#   -d          Turn on debug messages
#------------------------------------------------------------------------
universe	= vanilla
executable 	= scan_pages.sh
getenv		= true
output		= scan.out
error		= scan.err
log		= scan.log
arguments	= "/home2/lindbe2/workspace/ling575/1846-romer-pilgrimage-to-temples-tombs-v2 /home2/lindbe2/workspace/ling575/575_OCR/raw_texts/1846-romer-pilgrimage-to-temples-tombs-v2"
transfer_executable = false
queue
