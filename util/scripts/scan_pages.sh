#!/bin/bash
for filename in $1/*.jpg; do
    echo "$filename"
    tesseract "$filename" -l eng $2/"$(basename "$filename" .jpg)"
done
