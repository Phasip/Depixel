#!/usr/bin/python
from PIL import Image, ImageDraw, ImageFont
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error
import numpy as np
from sklearn.preprocessing import normalize
import itertools
import random


fonts = [
    "fonts/segoeprb.ttf",
    "fonts/SegoeUISoundlines.ttf",
    "fonts/segoeuii.ttf",
    "fonts/Cantarell-Regular.otf",
    "fonts/segoescb.ttf",
    "fonts/SEGOEUISL.TTF",
    "fonts/segoeuib.ttf",
    "fonts/segoesc.ttf",
    "fonts/segoeuisl.ttf",
    "fonts/Cantarell-Regular.ttf",
    "fonts/segoeui.ttf",
    "fonts/tahoma.ttf",
    "fonts/segoen_slboot.ttf",
    "fonts/segoepr.ttf",
    "fonts/segoeuil.ttf",
    "fonts/segoeuiz.ttf",
    "fonts/segoe_slboot.ttf",
]
def target_backforth(t_img, a):
    alts = [Image.NEAREST, Image.BILINEAR, Image.BICUBIC, Image.ANTIALIAS]
    px = (a["pixel_w"],a["pixel_h"])
    rd = alts[a["resample_down"]]
    ru = alts[a["resample_up"]]
    return t_img.resize(px,resample=rd).resize(t_img.size,ru)
    
def get_error(l1,l2):
    return mean_squared_error(l1,l2)

cnt = 0
def get_img_pixels(pil_image, crop, dump=False):
    global cnt
    if crop is not None:
        pil_image = pil_image.crop(crop)
    arr = np.array(pil_image.getdata())
    #pix_val = normalize(arr.reshape(1, -1))*10
    pix_val = arr.reshape(1, -1)
    return pix_val
    
def prep_target(target_img, pixel_count,resample, crop, i):
    alts = [Image.NEAREST, Image.BILINEAR, Image.BICUBIC, Image.ANTIALIAS]
    t_img = Image.open(target_img).convert('F')
    prepped = t_img.resize(pixel_count,resample=alts[resample])
    return get_img_pixels(prepped,crop)
    
def gen_alternative(text, t_size, resample, fnt, width, height, x_margin, y_margin, i,dump=False):
    alts = [Image.NEAREST, Image.BILINEAR, Image.BICUBIC, Image.ANTIALIAS]
    img = Image.new('F', (width, height), color = i['c'])
    d = ImageDraw.Draw(img)
    d.text((x_margin,y_margin), text, font=fnt, fill=i['f'])
    if dump:
        img.convert("RGBA").save("pil_t2.png")
    img = img.resize((i["final_width"],i["final_height"]),resample=alts[i['downsize_resample']])
    img = img.crop(i['blur_area'])
    imgSmall = img.resize(t_size,resample=alts[resample])
    return imgSmall



best = 9999999999
def gen_inputs(bf_data,output=True):
    inputs = []
    keys = bf_data.keys()
    alts = 1
    for k in keys:
        v = bf_data[k]
        if type(v) is tuple:
            l = list(np.arange(*v))
            alts = alts*len(l)
            inputs.append(l)
        elif type(v) is list:
            inputs.append(v)
        else:
            inputs.append([v])
        if len(inputs[-1]) == 0:
            raise Exception("Key %s has zero inputs!"%k)
    if output:
        print("We have a total of: %d inputs to handle, should take around %d minutes to handle"%(alts,alts/1343/60))
    all_inputs = list(itertools.product(*inputs))
    random.shuffle(all_inputs)
    for p in all_inputs:
        yield dict(zip(keys,p))


def verify_input(inp, bf_data):
    for k in inp.keys():
        v = bf_data[k]
        if type(v) is not tuple:
            print("Warning: %s is single valued!"%k)
            continue
        l = list(np.arange(*v))
        if l[-1] == inp[k]:
            print("Warning: %s has max value! (%d)"%(k,inp[k]))
        if l[0] == inp[k]:
            print("Warning: %s has min value! (%d)"%(k,inp[k]))
