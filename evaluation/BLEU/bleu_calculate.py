from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.tokenize import word_tokenize
import argparse

argparser = argparse.ArgumentParser(description = 'Caclulate the BLEU score between two text files')
argparser.add_argument('candidate_file', metavar='candidate', help='Candidate Text File')
argparser.add_argument('reference_file', metavar='reference', nargs='+', help='Gold Standard Reference Text File')

args = argparser.parse_args()

can_file = open(args.candidate_file, 'r')

references = list()
for ref in args.reference_file:
    references.append(open(ref, 'r').read())

tkn_can = word_tokenize(can_file.read())
cc = SmoothingFunction()
print('raw BLEU = %s' % sentence_bleu(references, tkn_can))
print('smoothed BLEU4 = %s' % sentence_bleu(references, tkn_can, smoothing_function=cc.method4))
