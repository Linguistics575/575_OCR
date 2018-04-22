'''
Is the WER on the IAM sample correlated with punctuation?
use ONLY on this dataset!!!!  (Not at all general)
'''
from collections import Counter
from os import listdir, path
from scipy.stats import pearsonr


def get_voc():
    '''
    Function to return the vocabulary to determine what punctuation exists in
    the corpus
    '''
    global_counter = Counter()

    for f in listdir(gold_standard_dir):
        with open(path.join(gold_standard_dir, f)) as g:
            local_counter = Counter(g.read().split())

            global_counter += local_counter

    for k in sorted(global_counter.keys()):
        print(k)


def get_punct_percent(file):
    '''
    return a tuple of (number of total tokens,
                          number of punctuation tokens,
                          percent punctuation tokens)
    for file
    '''
    # list of punctuations in corpus found with get_voc()
    punctuations = set("!\"#&'(),-.:;?").union({"..."})

    with open(file) as f:
        counter = Counter(f.read().split())

    num_punctuations = sum([v for
                            k, v in counter.items()
                            if k in punctuations])

    total_tokens = sum(counter.values())

    percent_punct = float(num_punctuations)/total_tokens

    return(total_tokens, num_punctuations, percent_punct)


def main():
    gold_standard_dir = '../sample_gold_standards'
    eval_results_file = '../evaluation_results.txt'
    output_file = './punct_correlation_results.txt'

    wers = []  # holds the wers
    percent_puncts = []  # hold the percent punctionations
    raw_puncts = []  # counts of raw punctuation
    num_substitutions = []
    num_insertions = []
    num_deletions = []
    edit_dists = []

    output_fh = open(output_file, "w")

    print("FILENAME                  WER    num_punct ttl_tok pct_tok",
          file=output_fh)
    print("------------------------- ------ --------- ------- -------",
          file=output_fh)

    with open(eval_results_file) as f:
        for i, line in enumerate(f.readlines()):
            # we skip the first two lines which are headers
            if i <= 1:
                continue

            # and we stop when we get to the "---" delimiter for the end
            if line[:3] == '---':
                break

            (recognized_file,
             wer,
             edit_dist,
             num_delete,
             num_insert,
             num_subst,
             num_ref_toks) = line.split()

            wer = float(wer)

            basename = recognized_file[:-len(".recognized.txt")]

            gold_standard_file = path.join(gold_standard_dir,
                                           basename + ".gold.txt")

            (total_tokens,
             num_punctuations,
             percent_punct) = get_punct_percent(gold_standard_file)

            print("{: <25} {:.4f} {: >9d} {: >7d}  {:.4f}".format(
                    path.basename(gold_standard_file), wer,
                    num_punctuations, total_tokens, percent_punct),
                  file=output_fh)

            wers.append(wer)
            percent_puncts.append(percent_punct)
            raw_puncts.append(num_punctuations)  # counts of raw punctuation

    print("----------------------------------------------------------",
          file=output_fh)

    r, p = pearsonr(wers, percent_puncts)
    print("r(%puct, wer)={:.4f}".format(r), file=output_fh)

    output_fh.close()


if __name__ == '__main__':
    main()
