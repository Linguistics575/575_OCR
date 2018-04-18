#!/bin/bash
for filename in $1/*.tiff; do
    echo "$filename"
    tesseract "$filename" -l eng $1/"$(basename "$filename" .tiff)"
done
