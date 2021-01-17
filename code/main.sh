#!/bin/bash

cd ../data
unzip round1_test.zip > /dev/null

cd ../code
python RoBERTa_MRC.py test gpu-0

cd ../prediction_result
zip -r result.zip tmp/* > /dev/null
