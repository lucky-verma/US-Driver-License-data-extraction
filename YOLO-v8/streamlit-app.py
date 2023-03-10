## streamlit app ##
import streamlit as st
import cv2
import time
import numpy as np
import easyocr
from PIL import Image
from parseq.strhub.data.module import SceneTextDataModule
import torch
from ultralytics import YOLO

# Load model and image transforms
parseq = torch.hub.load('baudm/parseq', 'parseq', pretrained=True).eval()
img_transform = SceneTextDataModule.get_transform(parseq.hparams.img_size)

# Load model
model = YOLO("./new_models/best.pt")
reader = easyocr.Reader(['en'], gpu=True)

st.title("US Drivers License Extraction")
st.write("Upload an image to extract text from it")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    coll1, coll2 = st.columns(2)
    with coll1:
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.info("Extracting text from image...")

    with coll2:
        # time the process
        start_time = time.time()

        # Run YOLOv8 model
        results = model.predict(source=image, augment=True)

        # Run OCR on each detected bounding box
        boxes = results[0].boxes

        easy_results = {}
        parseq_results = {}

        for box in boxes:
            names = {0: 'address', 1: 'dob', 2: 'name', 3: 'state'}

            # crop each box
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cropped = image.crop((x1, y1, x2, y2))
            cropped = cropped.resize((cropped.width*3, cropped.height*3))

            # add padding to cropped image 
            cropped = np.array(cropped)
            # cropped = cv2.copyMakeBorder(cropped, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            cropped = Image.fromarray(cropped)

            st.image(cropped, caption=f'{names[int(box.cls[0])]}', use_column_width=True)

            # run easyOCR on each cropped box and match with the class name
            temp = reader.readtext(np.array(cropped), detail=0)
            if temp:
                easy_results[names[int(box.cls[0])]] = [temp]

            # Run parseq model
            logits = parseq(img_transform(cropped).unsqueeze(0))

            # greedy decoding
            pred = logits.softmax(-1)
            label, confidence = parseq.tokenizer.decode(pred)

            if label:
                parseq_results[names[int(box.cls[0])]] = [label]
        
    # Display time taken
    st.write("Time taken: %s seconds" % (time.time() - start_time))

    # Display results in two columns
    st.write("Results:")
    col1, col2 = st.columns(2)
    with col1: 
        st.write("EasyOCR:")
        st.json(easy_results)
    with col2:
        st.write("Parseq:")
        st.json(parseq_results)




