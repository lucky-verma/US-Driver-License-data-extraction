# US Driver License Data Extraction

A multi-approach machine learning project for extracting text data (name, DOB, address, state) from US driver's license images using object detection and OCR techniques.

## Overview

This repository explores multiple approaches for driver's license data extraction:

- **YOLO-v8 + EasyOCR**: Production-ready pipeline combining YOLOv8 for field detection with EasyOCR for text recognition
- **YOLO-v5**: Custom-trained YOLOv5 model for license field detection
- **Donut (Document Understanding Transformer)**: End-to-end transformer-based document parsing without OCR
- **pyTesseract**: Traditional OCR approach using Tesseract engine
- **YOLO + TensorFlow 1.0**: Legacy implementation using Darkflow

## Repository Structure

```
.
├── DATASET/                    # Training datasets (US & India driver licenses)
├── Donut/
│   ├── CORD/                   # Fine-tuning notebooks and data preparation scripts
│   └── deployment/             # Gradio web app for Donut model inference
├── YOLO-v5/
│   ├── LegacyTrain/            # Training artifacts
│   └── yolov5/                 # YOLOv5 implementation
├── YOLO-v8/
│   ├── main.py                 # FastAPI REST API endpoint
│   ├── streamlit-app.py        # Streamlit web interface
│   ├── parseq/                 # Scene text recognition model
│   └── new_models/             # Trained model weights
├── pyTesseract_OCR/            # Tesseract-based extraction
└── YOLO___TF1.0/               # Legacy TensorFlow 1.x implementation
```

## Quick Start

### YOLOv8 + EasyOCR (Recommended)

1. Install dependencies:
   ```bash
   cd YOLO-v8
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run streamlit-app.py
   ```

3. Or start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   API endpoint: `POST /predict` with image file

### Donut Transformer

1. Install dependencies:
   ```bash
   cd Donut/deployment
   pip install -r requirements.txt
   ```

2. Run the Gradio app:
   ```bash
   python gradio-app.py
   ```

### YOLOv5

1. Create conda environment:
   ```bash
   cd YOLO-v5
   conda env create -f my_conda_env_yolov5.yml
   conda activate YOLO-v5
   ```

2. Training:
   ```bash
   python train.py --img 640 --batch 4 --epochs 100 --data train/US_DL.yaml --cfg train/custom_yolov5l.yaml --weights train_L/yolov5l.pt
   ```

3. Inference:
   ```bash
   python detect.py --weights runs/train/{exp}/weights/best.pt --img 640 --conf 0.2 --source test/images
   ```

## Tech Stack

- **Deep Learning**: PyTorch, Ultralytics YOLOv8/v5, Hugging Face Transformers
- **OCR**: EasyOCR, pyTesseract, PARSeq
- **Web Frameworks**: FastAPI, Streamlit, Gradio
- **Computer Vision**: OpenCV, PIL/Pillow
- **Other**: PyTorch Lightning, CUDA support for GPU acceleration

## Models

| Approach | Detection | Text Recognition | Use Case |
|----------|-----------|------------------|----------|
| YOLOv8 + EasyOCR | YOLOv8 | EasyOCR | Production API/UI |
| Donut | Transformer | End-to-end | Zero-OCR pipeline |
| YOLOv5 | YOLOv5 | - | Field detection only |
| pyTesseract | - | Tesseract | Basic OCR |

## Extracted Fields

- Name
- Date of Birth (DOB)
- Address
- State

## License

See individual component licenses in `YOLO___TF1.0/licenses/`.
