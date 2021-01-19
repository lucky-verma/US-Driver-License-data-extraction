### Basic training commands

#### train command with custom datasets and annotations 
`python flow --model cfg/tiny-yolo-4c.cfg  --train --dataset "C:\Users\lucki\WORK\OFFICE\VAST\DL-data-extraction\YOLO___TF1.0\licenses" --annotation "C:\Users\lucki\WORK\OFFICE\VAST\DL-data-extraction\YOLO___TF1.0\annotations"`


#### print results from a `.cfg` and `.weights` model
`python flow --imgdir sample_img/ --model cfg/tiny-yolo-4c.cfg --load bin/yolov3-spp.weights --threshold 0.3 --json `


### [Changes did]:

1. `classes = 5` & `.XML` labels (also, called as VOC format) (https://github.com/thtrieu/darkflow/issues/1011)
2. Visual Studio Dep error (https://github.com/thtrieu/darkflow/issues/788) further, general model used for training 
3. reshape tensor error (https://github.com/thtrieu/darkflow/issues/465)
4. expected value error (https://github.com/thtrieu/darkflow/issues/900)
5. can try tweaking the threshold (--threshold 0.3) OR can edit last section of `.cfg`
6. saving checkpoint as `.pb`
7. resume training from a checkpoint (https://github.com/thtrieu/darkflow/issues/701)


### [NOW]

1. Training on custom weights `tiny-yolo-voc.weights`
`python flow --model cfg/tiny-yolo-4c.cfg --load bin/tiny-yolo-voc.weights --train --dataset "C:\Users\lucki\WORK\OFFICE\VAST\DL-data-extraction\YOLO___TF1.0\licenses" --annotation "C:\Users\lucki\WORK\OFFICE\VAST\DL-data-extraction\YOLO___TF1.0\annotations" --epoch 200 --gpu 1.0`

2. converting checkpoint to `.pb`
`python flow --model cfg/tiny-yolo-4c.cfg --load -1 --savepb`

3. loading the `.pb` graph
`python flow --pbLoad built_graph/tiny-yolo-4c.pb --metaLoad built_graph/tiny-yolo-4c.meta --imgdir sample_img/`


