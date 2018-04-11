#!/bin/bash
# shell script to process many files and calculate WER
REFDIR="/media/jbruno/big_media/575_data/LFH_test_images/initial_evaluation_probe_1913/text_files"

HYPDIR="/media/jbruno/big_media/575_data/LFH_test_images/initial_evaluation_probe_1913/OHR_output"

file_names=( "IMG_8839_cropped_2"
                "IMG_8840_cropped_1"
                "IMG_8840_cropped_2"
                "IMG_8841_cropped_1"
                "IMG_8841_cropped_2"
                "IMG_8842_cropped_1"
                "IMG_8842_cropped_2"
                "IMG_8843_cropped_1"
                "IMG_8843_cropped_2"
                "IMG_8845_cropped_1"
                "IMG_8845_cropped_2"
                "IMG_8846_cropped_1"
                "IMG_8846_cropped_2"
                "IMG_8847_cropped_1"
                "IMG_8847_cropped_2"
                "IMG_8848_cropped_1"
                "IMG_8848_cropped_2"
                "IMG_8849_cropped_1"
                "IMG_8849_cropped_2" 
                "all_test_pages" )

for f in "${file_names[@]}"
do
    r="$REFDIR/$f.gold.txt"
    h="$HYPDIR/$f.ohr.txt"
    printf "$f "
    python wer.py $r $h
done
