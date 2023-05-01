## streamlit app ##
import streamlit as st
import cv2
import time
import numpy as np
import easyocr
from PIL import Image
import torch
from ultralytics import YOLO

# st configuration
st.set_page_config(layout="wide",
                   page_title="License",
                   page_icon="🚗",
                   initial_sidebar_state="expanded"
                   )

# hide made with streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Load object detection model
model = YOLO("./new_models/best.pt")
reader = easyocr.Reader(['en'], gpu=True)

st.title("US Drivers License Extraction")
st.write("Upload an image to extract text from it")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    coll1, coll2, col3 = st.columns([2,1,2])
    with coll1:
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        # st loading bar
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)

    with coll2:
        # time the process
        start_time = time.time()

        # Run YOLOv8 model
        results = model.predict(source=image, augment=True, conf=0.60, iou=0.35)

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
            temp = reader.readtext(np.array(cropped),
                                    detail=0,
                                    # width_ths = 0.14,
                                    allowlist='0123456789/-' if int(box.cls[0]) == 1 else None,
                                    )
            if temp:
                # Name processing
                if int(box.cls[0]) == 2 and len(temp) > 3:
                    temp.pop(0); temp.pop(1)
                    easy_results[names[int(box.cls[0])]] = [temp]

                # DOB processing
                elif int(box.cls[0]) == 1:
                    if len(temp) > 1:
                        temp.pop(0); easy_results[names[int(box.cls[0])]] = [temp]
                    else:
                        temp = temp[0][-10:]
                        easy_results[names[int(box.cls[0])]] = [temp]

                # State processing
                elif int(box.cls[0]) == 3:
                    temp = [word for word in temp if len(word) > 3]
                    easy_results[names[int(box.cls[0])]] = [temp]

                else:
                    easy_results[names[int(box.cls[0])]] = [temp]

    with col3:
        # Display results from easyOCR
        st.write("OCR Results")
        st.write(easy_results)

    # Display time taken
    st.success("Time taken: %s seconds" % (time.time() - start_time))

    # display time and status  
    print("Last parse: ", time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))


