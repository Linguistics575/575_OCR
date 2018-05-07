from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.tokenize import word_tokenize
import argparse

argparser = argparse.ArgumentParser(description = 'Caclulate the BLEU score between two text files')
argparser.add_argument('reference_file', metavar='reference', help='Gold Standard Reference Text File')
argparser.add_argument('candidate_file', metavar='candidate', help='Candidate Text File')

args = argparser.parse_args()

ref_file = open(args.reference_file, 'r')
can_file = open(args.candidate_file, 'r')

tkn_ref = word_tokenize(ref_file.read())
tkn_can = word_tokenize(can_file.read())
cc = SmoothingFunction()
print('raw BLEU = %s' % sentence_bleu([tkn_ref], tkn_can))
print('smoothed BLEU4 = %s' % sentence_bleu([tkn_ref], tkn_can, smoothing_function=cc.method4))
