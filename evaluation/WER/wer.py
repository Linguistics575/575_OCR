#!/usr/bin/env python3
'''
copy paste and modify of fantastic tool at https://github.com/zszyellow/WER-in-python
Made python3, added print_alignment parameter to wer
added argparser
Jimmy 4/7/2018

NOTE: WER = (S+D+I)/N, where:
        S = numnber of substitutions
        D = number of deletions
        I = number of insertions
        N = number of words in the reference (S + D + number correct)

TODO: For OCR, we should probably tokenize the inputs
      (e.g. 'hair.' --> 'hair .')

      Also, should clean up some more and create a pull request on original
      repository for this guy.
'''

import argparse
import numpy


def editDistance(r, h):
    '''
    This funciton is to calculate the edit distance of refernce sentence and the hypothesis sentence.
    Main algorithm used is dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    '''
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8).reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0: 
                d[0][j] = j
            elif j == 0: 
                d[i][0] = i
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d


def getStepList(r, h, d):
    '''
    This function is to get the list of steps in the process of dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
        d -> the matrix built when calulating the editting distance of h and r.
    '''
    x = len(r)
    y = len(h)
    list = []
    while True:
        if x == 0 and y == 0:
            break
        elif d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1] and x >= 1 and y >= 1: 
            list.append("e")
            x = x - 1
            y = y - 1
        elif d[x][y] == d[x][y-1]+1 and y >= 1:
            list.append("i")
            x = x
            y = y - 1
        elif d[x][y] == d[x-1][y-1]+1 and x >= 1 and y >= 1:
            list.append("s")
            x = x - 1
            y = y - 1
        else:
            list.append("d")
            x = x - 1
            y = y
    return list[::-1]

def alignedPrint(list, r, h, result):
    '''
    This funcition is to print the result of comparing reference and hypothesis sentences in an aligned way.
    
    Attributes:
        list   -> the list of steps.
        r      -> the list of words produced by splitting reference sentence.
        h      -> the list of words produced by splitting hypothesis sentence.
        result -> the rate calculated based on edit distance.
    '''
    print("REF:", end=' ')
    for i in range(len(list)):
        if list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(" "*(len(h[index])), end=' ')
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) < len(h[index2]):
                print(r[index1] + " " * (len(h[index2])-len(r[index1])), end=' ')
            else:
                print(r[index1], end=' ')
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(r[index], end=' ')
    print()
    print("HYP:", end=' ')
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=' ')
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print(h[index2] + " " * (len(r[index1])-len(h[index2])), end=' ')
            else:
                print(h[index2], end=' ')
        else:
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(h[index], end=' ')
    print()
    print("EVA:", end=' ')
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print("D" + " " * (len(r[index])-1), end=' ')
        elif list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print("I" + " " * (len(h[index])-1), end=' ')
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print("S" + " " * (len(r[index1])-1), end=' ')
            else:
                print("S" + " " * (len(h[index2])-1), end=' ')
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=' ')
    print()
    print("WER: " + result)


def wer(r, h, print_alignment=False):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split()) 

    Parameters:
    -----------
        r : sequence
            reference
        h : sequence
            hypothesis
        print_alignment : boolean (default False)
            prints alignment if true

    """
    # build the matrix
    d = editDistance(r, h)

    # print the result in aligned way
    result = float(d[len(r)][len(h)]) / len(r) * 100
    result = str("%.2f" % result) + "%"

    if print_alignment:

        # find out the manipulation steps
        step_list = getStepList(r, h, d)
        alignedPrint(step_list, r, h, result)
    else:
        print("WER: ", result)


def main():
    parser = argparse.ArgumentParser(
        description="Calculates WER for 2 files, ignoring whitespace.")
    parser.add_argument("reference_file",
                        help='File to use as Reference')
    parser.add_argument("hypothesis_file",
                        help='File to use as hypothesis')
    parser.add_argument("--print_alignment", "-p",
                        help="Prints alignment when set",
                        action='store_true',
                        default=False)
    parser.add_argument("--ignore_order", "-i",
                        help='Will ignore order of tokens when set (by '
                             'sorting the hypotheses and reference sequences)',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    with open(args.reference_file) as f:
        r = f.read().split()

    with open(args.hypothesis_file) as f:
        h = f.read().split()

    if args.ignore_order:
        wer(sorted(r), sorted(h), args.print_alignment)
    else:
        wer(r, h, args.print_alignment)


if __name__ == '__main__':
    main()
