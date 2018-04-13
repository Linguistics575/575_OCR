'''
script to take a sample of 100 forms from the IAM database, stored locally.
Takes the sample and copies the files.
All paths are hard-coded.
'''
import numpy as np
import os
from shutil import copy
from sys import stderr


def get_all_form_ids(form_file):
    '''
    Return a list of all form_ids from the form_file
    the form_ids are the first whitespace delimited element on the line.
    "#" is a comment character, so skip those lines
    '''
    form_ids = []

    with open(form_file) as f:
        for line in f.readlines():
            if line.startswith("#"):
                continue
            elements = line.split()
            if elements:
                form_ids.append(elements[0])

    return form_ids


def take_sample(population, sample_size, seed_value=0):
    '''
    Take a sample from a population using a seed for a random state

    Parameters:
    -----------
        population : list
            population from which to sample
        sample_size : int
        seed_value : int (defaults to 0)
            seed to use for random state (for reproducibility purposes)

    Returns:
    --------
        sample : list
            sample of size sample_size from population taken using seed_value
    '''
    random_state = np.random.RandomState(seed=seed_value)

    sample = random_state.choice(population, sample_size, replace=False)

    return sorted(sample)


def main():
    # file that lists all the forms:
    form_file = r'/media/jbruno/big_media/575_data/IAM/ascii/forms.txt'

    # file that will list the members of our sample
    sample_list_file = './sample_forms.ls'

    # directory that holds all the images
    png_dir = '/media/jbruno/big_media/575_data/IAM/forms'

    # directory to hold the sample:
    sample_dir = "./sample_png_files"

    # if it doesn't exist, make it:
    if not os.path.isdir(sample_dir):
        os.mkdir(sample_dir)

    # read in all the form ids
    all_form_ids = get_all_form_ids(form_file)

    sample_size = 100
    seed_value = 9

    sample = take_sample(all_form_ids, sample_size, seed_value)

    # output the members of our sample to the list file:
    with open(sample_list_file, "w") as f:
        for form in sample:
            print(form, file=f)

    # and copy the files over
    for form in sample:
        source = os.path.join(png_dir, form + ".png")

        # we're going to call these "not_done" because we're going to manually
        # crop them.  As we crop them, we'll take the "not_done" away from the
        # filename
        dest = os.path.join(sample_dir, form + "not_done.png")

        if os.path.exists(dest):
            print(dest, "exists.  Skipping this one.", file=stderr)

        else:
            copy(source, dest)


if __name__ == '__main__':
    main()
