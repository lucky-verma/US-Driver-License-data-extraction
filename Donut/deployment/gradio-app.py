import torch
import re

import gradio as gr

from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel


def demo_process(input_img):
    # input_img = Image.fromarray(input_img)

    processor = DonutProcessor.from_pretrained("thinkersloop/donut-demo")
    pretrained_model = VisionEncoderDecoderModel.from_pretrained(
        "thinkersloop/donut-demo")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    pretrained_model.to(device)

    pixel_values = processor(input_img, return_tensors="pt").pixel_values

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


# task_prompt = f"<s_cord-v2>"

image = Image.open("./sample_1.jpg")
image.save("cord_sample_1.png")
image = Image.open("./sample_2.jpg")
image.save("cord_sample_2.png")
image = Image.open("./sample_3.jpg")
image.save("cord_sample_3.png")

demo = gr.Interface(
    fn=demo_process,
    inputs=gr.inputs.Image(type="pil"),
    outputs="json",
    title=f"Transformers demo for `cord-v2` task",
    description=
    """This model is trained with 66 driver's license images of CORD dataset. <br>""",
    # examples=[["cord_sample_1.png"], ["cord_sample_2.png"], ["cord_sample_3.png"]],
    cache_examples=False,
)

demo.launch()