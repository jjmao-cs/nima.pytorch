#!/bin/sh
export PYTHONPATH=.
export PATH_TO_AVA_TXT=./image/AVA_new_0710_3.txt
export PATH_TO_IMAGES=./image/AVA_chosen/
export PATH_TO_CSV=./tmp0924
mkdir $PATH_TO_CSV
export BATCH_SIZE=50
export NUM_WORKERS=1
export NUM_EPOCH=50
export INIT_LR=0.00001
export EXPERIMENT_DIR_NAME=$PATH_TO_CSV
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
