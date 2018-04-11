#!/usr/bin/env python3
'''
Module containing useful functions to get WER, edit distance, numbers of
deletions, substitutions, insertions, and a printed alignment between reference
and hypothesis texts.

Can be run as a script on two files.

Verbose output looks like this:
    WER    EditDist #Substit #Delete #Insert #RefToks
    ---    -------- -------- ------- ------- --------
    0.7333       88       45      35       8      120

Horizontally printed alignment looks like this:
     Fuzzy Wuzzy was a     bear
John Fuzzy Wuzzy had hair.
I                S   S     D

Vertically printed alignment looks like this:
I       John
  Fuzzy Fuzzy
  Wuzzy Wuzzy
S was   had
S a     hair.
D bear
@author Jimmy Bruno
@date 4/10/2018
'''
import argparse
from collections import namedtuple
from itertools import chain

# DiffStats object returned by get_diff_stats
DiffStats = namedtuple('DiffStats', ['edit_distance', 'num_deletions',
                                     'num_insertions', 'num_substituions',
                                     'num_ref_elements', 'alignment'])


class AlignmentPrinter():
    '''
    Pretty prints alignment between reference and hypothesis, with annotations
    for Substitutions, Deletions, and Insertions.

    Parameters:
    -----------
        ref_elements : list
            list of elements from reference iterable
        hypothesis_elements : list
            list of elments from hypothesis iterable
        label_str : list
            list of strings indicating D(eletion), I(insertion),
            S(ubstitution), or " " if there's a match.
    '''

    def __init__(self, ref_elements, hypothesis_elements, label_str):
        self.ref_elements = ref_elements
        self.hypothesis_elements = hypothesis_elements
        self.label_str = label_str
        assert (len(self.ref_elements) ==
                len(self.hypothesis_elements) ==
                len(self.label_str))

    def __str__(self):
        if len(self.ref_elements) > 8:
            self.print(orient='vertical')
        else:
            self.print(orient='horizontal')
        return ""

    def print(self, orient='horizontal'):

        '''
        pretty prints an alignment to stdout

        Parameters:
        -----------
            orient : str ('horizontal' or 'vertical', defaults to 'horizontal')
                orientation of printout.  For long documents, 'vertical' will
                be more readable since this is not smart enough to insert
                appropriate line breaks in horizonal mode.
        '''
        assert orient == 'horizontal' or orient == 'vertical'

        if orient == 'horizontal':
            # we'll need to pad things to elements line up nicely horizontally

            # list of the maxiumum lengths of  (reference, hypothesis, label)
            max_lengths = [max(map(len, e)) for e
                           in zip(self.ref_elements,
                                  self.hypothesis_elements,
                                  self.label_str)]

            # list of reference elements with padding appropriate for printing
            padded_ref_elements = list(map(str.ljust,
                                           self.ref_elements,
                                           max_lengths))

            # list of hypothesis elements with padding appropriate for printing
            padded_hyp_elements = list(map(str.ljust,
                                           self.hypothesis_elements,
                                           max_lengths))

            # list of label elements with padding appropriate for printing
            padded_label_elements = list(map(str.ljust,
                                             self.label_str,
                                             max_lengths))

            print(" ".join(padded_ref_elements))
            print(" ".join(padded_hyp_elements))
            print(" ".join(padded_label_elements))

        else:
            # we'll need to pad things to create nice columns, which means that
            # we just have to add padding to the right side of the references

            # maximum length of any element
            max_length = max(map(len,
                                 list(chain(self.ref_elements,
                                            self.hypothesis_elements))))
            # do the padding
            padded_ref_elements = list(map(lambda x: str.ljust(x, max_length),
                                           self.ref_elements))
            for x in zip(self.label_str,
                         padded_ref_elements,
                         self.hypothesis_elements):

                print(" ".join(x))


def get_distance_matrix(ref, hypothesis):

    '''
    return an edit distance matrix

    Parameters:
    -----------
        ref : iterable
            the "reference" iterable, e.g. elements present in ref but absent
            in hypothesis will be deletions.

        hypothesis : iterable
            the "hypothesis iterable", e.g. elements present in hypothesis but
            absent in ref will be insertions

    Returns:
    --------
        distance_matrix : 2d list of lists
    '''
    # initialize the matrix
    ref_len = len(ref) + 1
    hyp_len = len(hypothesis) + 1
    distance_matrix = [[0] * hyp_len for _ in range(ref_len)]
    for i in range(ref_len):
        distance_matrix[i][0] = i
    for j in range(hyp_len):
        distance_matrix[0][j] = j

    # calculate the edit distances
    for i in range(1, ref_len):
        for j in range(1, hyp_len):

            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]

            if ref[i-1] != hypothesis[j-1]:
                substitution += 1

            distance_matrix[i][j] = min(insertion, deletion, substitution)

    return distance_matrix


def get_simple_wer(ref, hypothesis):
    '''
    simple helper function to quickly return the WER if that's all we're
    interested in

    Parameters:
    -----------
        ref : iterable
            the "reference" iterable, e.g. elements present in ref but absent
            in hypothesis will be deletions.
        hypothesis : iterable
            the "hypothesis iterable", e.g. elements present in hypothesis but
            absent in ref will be insertions

    Returns:
    --------
        wer : float
            Word-Error-Rate
    '''
    distance_matrix = get_distance_matrix(ref, hypothesis)

    i = len(distance_matrix) - 1
    j = len(distance_matrix[i]) - 1

    edit_distance = distance_matrix[i][j]

    # the reference is along the i dimension (rows) so the WER is:
    return float(edit_distance)/i


def get_diff_stats(ref, hypothesis, return_alignment=False):

    '''
    Return diff stats between reference and hypothesis, and optionally an
    AlignmentPrinter object.

    Parameters:
    -----------
        ref : iterable
            the "reference" iterable, e.g. elements present in ref but absent
            in hypothesis will be deletions.
        hypothesis : iterable
            the "hypothesis iterable", e.g. elements present in hypothesis but
            absent in ref will be insertions
        return_alignment : boolean (default : false)
            will return an AlignmentPrinter object

    Returns:
    --------
        a named tuple of
            edit_distance : int
                the edit distance between ref and hypothesis (where deletions,
                insertions, and substitutions all have an equal penalty of 1)
            num_deletions : int
                the number of deletions
            num_insertions : int
                the number of insertions
            num_substitutions : int
                the number of substituions
            num_ref_elements : int
                the total number of elements in ref
            alignment : AlignmentPrinter (only if return_alignment == True)
    '''
    distance_matrix = get_distance_matrix(ref, hypothesis)

    num_ref_elements = len(ref)
    i = num_ref_elements
    j = len(hypothesis)

    edit_distance = distance_matrix[i][j]

    num_deletions = 0
    num_insertions = 0
    num_substituions = 0

    # we'll need these if we want the alignment
    ref_elements = []
    hypothesis_elements = []
    label_str = []

    # start at the cell containing the edit distance and analyze the matrix to
    # figure out what is a deletion, insertion, or substitution.
    while i or j:
        # if deletion
        if distance_matrix[i][j] == distance_matrix[i-1][j] + 1:
            num_deletions += 1

            if return_alignment:
                ref_elements.append(ref[i-1])
                hypothesis_elements.append(" ")
                label_str.append('D')

            i -= 1

        # if insertion
        elif distance_matrix[i][j] == distance_matrix[i][j-1] + 1:
            num_insertions += 1

            if return_alignment:
                ref_elements.append(" ")
                hypothesis_elements.append(hypothesis[j-1])
                label_str.append('I')

            j -= 1

        # if match or substitution
        else:
            ref_element = ref[i-1]
            hypothesis_element = hypothesis[j-1]

            if ref_element != hypothesis_element:
                num_substituions += 1
                label = 'S'
            else:
                label = ' '

            if return_alignment:
                ref_elements.append(ref_element)
                hypothesis_elements.append(hypothesis_element)
                label_str.append(label)

            i -= 1
            j -= 1

    if return_alignment:

        ref_elements.reverse()
        hypothesis_elements.reverse()
        label_str.reverse()

        alignment = AlignmentPrinter(ref_elements,
                                     hypothesis_elements,
                                     label_str)

        return DiffStats(edit_distance, num_deletions, num_insertions,
                         num_substituions, num_ref_elements, alignment)
    else:
        return DiffStats(edit_distance, num_deletions, num_insertions,
                         num_substituions, num_ref_elements, None)


def main():
    parser = argparse.ArgumentParser(
        description="Calculates Word-Error-Rate (WER) for 2 files, ignoring "
                    "whitespace.  Note that WER is defined as (#insertions + "
                    "#deletions + #substitutions)/(#tokens in reference)")
    parser.add_argument("reference_file",
                        help='File to use as Reference')
    parser.add_argument("hypothesis_file",
                        help='File to use as hypothesis')
    parser.add_argument("--verbose", "-v",
                        help="In addition to WER, prints edit distance, "
                             "and number of deletions, insertions, and "
                             "substitutions.",
                        action='store_true',
                        default=False)
    parser.add_argument("--print_alignment", "-a",
                        required=False, choices=['horizontal', 'vertical'],
                        help="Print the aligned text horizonally or "
                             "vertically.  vertical will be more readable "
                             "for longer texts, but horizontal will be more "
                             "concise.")
    parser.add_argument("--ignore_order", "-i",
                        help='Will ignore order of tokens when set (by '
                             'sorting the hypothesis and reference sequences)',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    with open(args.reference_file) as f:
        reference = f.read().split()

    with open(args.hypothesis_file) as f:
        hypothesis = f.read().split()

    if args.ignore_order:
        # we ignore the impact of the order by sorting the elements
        reference.sort()
        hypothesis.sort()

    if args.verbose:
        return_alignment = True if args.print_alignment else False

        diff_stats = get_diff_stats(reference, hypothesis, return_alignment)

        (edit_distance,
         num_deletions,
         num_insertions,
         num_substituions,
         num_ref_elements,
         alignment) = diff_stats

        wer = float(edit_distance)/num_ref_elements

        print("WER    EditDist #Substit #Delete #Insert #RefToks")
        print("---    -------- -------- ------- ------- --------")
        print("{:.4f} {: >8d} {: >8d} {: >7d} {: >7d} {: >8}".format(
                        wer, edit_distance, num_substituions, num_deletions,
                        num_insertions, num_ref_elements))
    else:
        print("WER: ", get_simple_wer(reference, hypothesis))

    if args.print_alignment:
        alignment.print(orient=args.print_alignment)


if __name__ == '__main__':
    main()
