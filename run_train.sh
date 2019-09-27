#!bin/sh
python nima/cli.py prepare-dataset --path_to_ava_txt $PATH_TO_AVA_TXT --path_to_save_csv $PATH_TO_CSV   --path_to_images $PATH_TO_IMAGES
echo prepare
CUDA_VISIBLE_DEVICES=1 python nima/cli.py train-model --path_to_save_csv $PATH_TO_CSV  --path_to_images $PATH_TO_IMAGES  --batch_size $BATCH_SIZE  --num_workers $NUM_WORKERS --num_epoch $NUM_EPOCH --init_lr $INIT_LR   --experiment_dir_name $EXPERIMENT_DIR_NAME
echo train
