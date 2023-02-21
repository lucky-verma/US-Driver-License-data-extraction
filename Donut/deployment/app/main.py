# fastapi app to serve the model as an API endpoint
# Input is base64 encoded image
# Output is JSON

import base64
import io
import uvicorn
import torch
import re

from transformers import DonutProcessor, VisionEncoderDecoderModel
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

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


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    processor = DonutProcessor.from_pretrained("thinkersloop/donut-demo")
    pretrained_model = VisionEncoderDecoderModel.from_pretrained(
        "thinkersloop/donut-demo")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    pretrained_model.to(device)

    pixel_values = processor(image, return_tensors="pt").pixel_values

    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(task_prompt,
                                            add_special_tokens=False,
                                            return_tensors="pt")["input_ids"]

    outputs = pretrained_model.generate(
        pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=pretrained_model.decoder.config.max_position_embeddings,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=1,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
        output_scores=True,
    )
    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token,
                                "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()

    return processor.token2json(sequence)

if __name__ == "__main__":
    uvicorn.run("fastapi-app:app", host="0.0.0.0", port=8000, reload=True, workers=4)
