'''
Script to create gold standard transcription files for IAM forms by parsing
the IAM ascii files.

This is really ineffecient, but it works.

Jimmy, 2018-04-14
'''
import argparse
from os import mkdir, path
import re
from sys import stderr


def get_transcription(form, ascii_file):

    # this will help us save some iterations.  Just stop reading the file once
    # you're done with the form you want.
    found_form = False

    transcription_lines = []

    with open(ascii_file) as f:
        for line in f.readlines():
            if line.startswith("#"):
                continue

            split_line = line.split()

            if not split_line:
                continue

            contains_form_from_line = split_line[0].split("-")

            if len(contains_form_from_line) > 2:
                form_from_line = "-".join(contains_form_from_line[:2])
            else:
                continue

            if form_from_line == form:
                found_form = True
                # the words are always the 8th element
                words = split_line[8].split("|")
                output_line = " ".join(words)
                transcription_lines.append(output_line)
            else:
                if found_form:
                    break
    return "\n".join(transcription_lines)


def main():
    parser = argparse.ArgumentParser(
                    description='create gold standard transcription'
                                ' files for IAM forms by parsing the IAM ascii'
                                ' files.')
    parser.add_argument("form_list", help='list file of forms to create '
                                          'transcriptions for')
    parser.add_argument('IAM_ascii_file', help='path to IAM lines.txt file')
    parser.add_argument('output_dir')
    args = parser.parse_args()

    if not path.exists(args.output_dir):
        mkdir(args.output_dir)

    with open(args.form_list) as f:
        for form in f.readlines():
            form = form.strip()
            if form:
                print("Processing ", form, file=stderr)

                transcription = get_transcription(form, args.IAM_ascii_file)

            gold_file = path.join(args.output_dir, form + '.gold.txt')

            with open(gold_file, "w") as g:
                print(transcription, file=g)


if __name__ == '__main__':
    main()
