# 575_OCR
holds work for 575_OCR project.
At present, this repository contains resources in 2 directories:
- `azure/`: contains a script to run an image through the MS Azure Handwriting Recognition API and related resources.  (See readme there)
- `evaluation/`: contains a script to calculate Word-Error-Rate and various experiments and evaluations.
---
    7 April, 2:25 PM PDT: Added Python utility files for PDFs. Added one sample PDF and extracted text. (Other PDFs and output will be placed in dropbox, since they get rather large.)

    10 April, 7:25 PM PDT: Checked in WER script that now accurately calculates WER.

    11 April, 11:38 AM PDT: Checked in log file to track resolution used on Martineau documents. (Baedeker data yet to be added.)

    10 April, 7:25 PM PDT: Checked in WER script that now accurately calculates WER.
    10 April, 7:54 PM PDT: Checked in script to take sample from IAM handwriting DB
                           and also a file listing the sample of 100, under /evaluation.
    14 April, 12:18 PM PDT: Script to call MS Azure API to do handwriting
                            recognition.  Jimmy is generally really happy with it.
                            OCR recognition could do with more testing.
    15 April, 5:00 PM PDT : WER script can now operate in batch mode and print out a summary.
    15 April, 9:00 PM PDT : Checked in evaluation results of Azure API on IAM Handwriting dataset

