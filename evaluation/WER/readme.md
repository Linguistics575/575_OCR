# Word-Error-Rate (WER) Calculator
`wer.py` will calculate the WER by comparing the text in a gold standard file (called the reference) with the text of a hypothesis file, ignoring whitespace.  

WER = (#substitutions + #insertions + #deletions) / (# tokens in _reference_ text). 

The script can be run on a single <reference, hypothesis> pair of files, or on a batch of such pairs, listed in a mapping file of paths.

## Usage:
There are 2 forms of the command depending on whether a single <reference_file, hypothesis_file> pair is being processed or a batch of them.

##### single pair mode
To calculate the WER on a single <_reference_, _hypothesis_> pair, the form of the command is:
`python wer.py single reference_file hypothesis_file`

##### batch mode
To calcuate the WER on a batch of <_reference_, _hypothesis_> pairs, the form of the command is:
`python wer.py batch mapping_file`
where `mapping_file` is a text file listing pairs of whitespace-separated paths, with the first path pointing to the reference file and the second path pointing to the hypothesis file, e.g.:
```
path/to/reference/for/text1.txt     path/to/hypothesis/for/text1.txt
path/to/reference/for/text2.txt     path/to/hypothesis/for/text2.txt
etc...
```
#### options and output
The basic output in `single` mode is simply the WER:
```
% python wer.py single reference.txt hypothesis.txt 
hypothesis.txt WER:  0.6
```
In batch mode, the WERs for all the mapping pairs will be output, in addition to a weighted average of the WERs for all pairs in the file:
```
% python wer.py batch mapping_file.ls
a01-007.recognized.txt WER:  0.10144927536231885
a01-063x.recognized.txt WER:  0.14285714285714285
------------------------------
WEIGHTED AVERAGE WER:  0.1232869863
```
In addition, it is possible to pass the following options in either mode:
```
  --verbose, -v         In addition to WER, prints edit distance, and number
                        of deletions, insertions, and substitutions.
  --print_alignment {horizontal,vertical}, -a {horizontal,vertical}
                        Print the aligned text horizonally or vertically.
                        vertical will be more readable for longer texts, but
                        horizontal will be more concise.
  --ignore_order, -i    Will ignore order of tokens when set (by sorting the
                        hypothesis and reference sequences)
```
##### Examples:
```
% python wer.py batch mapping_file.ls --verbose
FILENAME                  WER    EditDist #Substit #Delete #Insert #RefToks
------------------------- ------ -------- -------- ------- ------- --------
a01-007.recognized.txt    0.1014        7        4       0       3       69
a01-063x.recognized.txt   0.1429       11        2       1       8       77
------------------------- ------ -------- -------- ------- ------- --------
WEIGHTED AVERAGE WER      0.1233       18        6       1      11      146
```

```
% python wer.py single reference.txt hypothesis.txt -a horizontal --verbose
FILENAME                  WER    EditDist #Substit #Delete #Insert #RefToks
------------------------- ------ -------- -------- ------- ------- --------
hypothesis.txt            1.4000        7        1       3       3        5
Fuzzy Wuzzy was a  bear            
      Wuzzy had no hair on his eye.
D           S   S  S    I  I   I 
```
