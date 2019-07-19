from PIL import Image, ImageDraw,ImageFont
import numpy as np
import json
import collections
import io


def imread(image):
    if isinstance(image, bytes):
        image = io.BytesIO(image)
        image.seek(0)
    return np.array(Image.open(image).convert(mode='RGB'))



def parse_params(path):
    with open(path, 'r') as f:
        content = json.load(f)
    return collections.namedtuple("Params", content.keys())(*content.values())


def draw(image, bboxs, names):
    image = ImageDraw.Draw(image)
    fontsize = 25
    font = ImageFont.truetype("arial.ttf", fontsize)
    for i in range(bboxs.shape[0]):
        bbox = bboxs[i]
        image.rectangle((bbox[0], bbox[1], bbox[2], bbox[3]), outline='red')
        image.text((bbox[0], bbox[1]), names[i], fill='red',font =font)
