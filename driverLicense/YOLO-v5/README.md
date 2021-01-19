### Getting data ready
1. Can use `labelImg` or `roboflow.ai` for annotating.
2. get atleast 100 datapoints with 7:2:1 train:valid:test ratio.

### Training commands
1. `python train.py --img 640 --batch 4 --epochs 100 --data train/US_DL.yaml --cfg train/custom_yolov5l.yaml --weights train_L/yolov5l.pt`
2. To get realtime training feedback like tensorbaord but, over the cloud`pip install wandb`
3. TensorBoard `tensorboard --logdir /content/yolov5/runs`

### Running best ProboTrained models
1. weights can be found here : `yolov5/runs/train/{ex(n)}/weights/best.pt`
2. run by : `python detect.py --weights runs/train/{ex(n)}/weights/best.pt --img 640 --conf 0.2 --source test/images`