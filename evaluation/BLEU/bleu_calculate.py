from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.tokenize import word_tokenize
import argparse

argparser = argparse.ArgumentParser(description = 'Caclulate the BLEU score between two text files')
argparser.add_argument('-r', metavar='reference', help='Gold Standard Reference Text File')
argparser.add_argument('-c', metavar='candidate', help='Candidate Text File')

args = argparser.parse_args()

ref_file = open(args.r, 'r')
can_file = open(args.c, 'r')

tkn_ref = word_tokenize(ref_file.read())
tkn_can = word_tokenize(can_file.read())
cc = SmoothingFunction()
print('raw BLEU = %s' % sentence_bleu([tkn_ref], tkn_can))
print('BLEU 4 = %s' % sentence_bleu([tkn_ref], tkn_can, smoothing_function=cc.method4))