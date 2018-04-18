#!/bin/bash

convert -density 300 $1 -strip -background white -alpha off $2/1848-martineau-eastern-life_%04d.tiff
