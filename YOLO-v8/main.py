"""
FastAPI app to serve the yolov8 model and easyOCR as an API endpoint
"""

import uvicorn
import torch
import io
import cv2
import numpy as np
import easyocr
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ultralytics import YOLO

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("best.pt")
reader = easyocr.Reader(['en'], gpu=True)

@app.get("/")
async def root():
    return {"message": "CNN+OCR Drivers License Extraction API. \n Visit /docs for more info."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # make sure image is PIL.Image.Image
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)

    # Run YOLOv8 model
    results = model.predict(source=image, classes=[1, 3])

    # Run OCR on each detected bounding box
    boxes = results[0].boxes

    final_results = {}
    for box in boxes:
        names = {0: 'address', 1: 'dob', 2: 'name', 3: 'state'}

        print(type(image))
        # crop each box
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cropped = image.crop((x1, y1, x2, y2))

        # run OCR on each cropped box and match with the class name
        temp = reader.readtext(np.array(cropped), detail=0)
        if temp:
            final_results[names[int(box.cls[0])]] = [temp]

    return final_results
        

