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
executable 	= scan_all.sh
getenv		= true
output		= scan.out
error		= scan.err
log		= scan.log
arguments	= "-i sample -o tmp -r 800 -f sample_journal.pdf -d"
transfer_executable = false
queue
