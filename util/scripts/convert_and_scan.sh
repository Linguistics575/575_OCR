#!/bin/bash

./get_page_images.sh $1 $2
./scan_pages.sh $2
rm $2/*.tiff
