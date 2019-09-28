# [The origin Author's README](originREADME.md)


# Pytroch NIMA Additional Files

## Index
  * [train script (run_train.sh)](#train-script)
  * [environment variable script (var.sh)](#environment-variable-script)
  * [draw.py](#draw-py)
  *  [get_adjust.py](#getadjust-py)
  *  [get_high.py](#gethigh-py)
  *  [opt4.py](#opt4-py)
  *  [tmpXXX folders](#tmpxxx-floders)
  *  nima/
      - [nima_new.py](#nimanimanew-py)
      - [nima_adjust.py](#nimanimaadjust-py)

### train script
    A linux script that includes the main training script needed.
    Contains 'prepare_dataset' and 'train_model' command in the origin author cli.py

    NOTICE:
      1. Before command line echo prepare, there should echo "Done" first.
      2. The training progress will not echo to command, if needed, refer to linux official command instructions.

### environment variable script
    A linux script that includes the setting of environment variable the train_model and test_model required.

    NOTICE:
      1. Before the script used, the folder name of the tmp directory should be modify. (Please the "$PATH_TO_CSV" line)


### draw py
    Using opt4.py ,an Genetic Algorithm (GA), to estimate 
    the best contrast and brightness parameter for the input image. (judge by score)

    Compare with all the possibility contrast and brightness combination to the input image,
    output a 3D graph shows the whole combination score distributes ans where the GA score locates.

### get_adjust py
    A tool that can get the adjust image depends on the input given.

    The output will pop up a window shows the image adjust with the parameter inputs.


### get_high py
    A tool that can get the highest score image form the directory chosen.
    Score calculate by the txt file AVA provided for made by user.

    txt format : (Copy from AVA Dataset)

    **************************************************************************
    Content of AVA.txt
    **************************************************************************

    Column 1: Index

    Column 2: Image ID 

    Columns 3 - 12: Counts of aesthetics ratings on a scale of 1-10. Column 3 
    has counts of ratings of 1 and column 12 has counts of ratings of 10.

    Columns 13 - 14: Semantic tag IDs. There are 66 IDs ranging from 1 to 66.
    The file tags.txt contains the textual tag corresponding to the numerical
    id. Each image has between 0 and 2 tags. Images with less than 2 tags have
    a "0" in place of the missing tag(s).

    Column 15: Challenge ID. The file challenges.txt contains the name of 
    the challenge corresponding to each ID.
    **************************************************************************

### opt4 py
    A Genetic Algorithm (GA)(中文:基因型演算法) approach 
    to get the highest score from adjusting input image by brightness and contrast.

    Using half of time compare to finding the high score from trying all combinations.
    (Time messure calculate by messure_opt4.py and nima/nima_adjust.py)

    USAGE:
        From terminal:
            python opt4.py (YOUR_IMAGE_PATH) 
        From Other Files:
            import opt4
            opt4.starts(YOUR_IMAGE_PATH)

    BE AWARE:
        The model pth is fixed in this file, moodify it if any changes
        (at around line no. 264)

### tmpXXX floders
    XXX means the date the model trainned or the ordered.
    the epoch of model inside the folder is mention on the filename.
    usually we uses the last epoch of the training, unless the validation has less loss rate.
    
    Our model only trains on part of the AVA Dataset image, which has the fellowing tags.
     20 Architecture
     21 Black and White
     2 Cityscape
     23 Travel
     10 Urban
     14 Landscape

### nima/nima_new py
    The main file the image Testing and image Adjust is done.

### nima/nima_adjust py
    An old version of adjusting image by fixed contrast and brightness, or all combinations of contrast and brightness.
