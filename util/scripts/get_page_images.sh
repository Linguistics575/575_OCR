#!/bin/bash

fn=$(basename $1)

convert -density 300 $1 -strip -background white -alpha off $2/${fn%.*}_%04d.tiff
