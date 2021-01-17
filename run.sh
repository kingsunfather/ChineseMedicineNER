#!/bin/bash

cd ./code
echo "Start to inference..."
python RoBERTa_MRC.py test gpu-0

cd ../
echo "Start to pack files..."
zip -r result.zip submit/* > /dev/null
echo $(ls -l result.zip)
