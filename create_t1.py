#!/usr/bin/python
# 1. install pypy3 from source (Not APT!)
# 2. pypy3 -m ensurepip
# 3. pypy3 -m pip install cython
# 4. pypy3 -m pip install sklearn pillow
import sys
import sys
from Depixel import *

input_info_bf = {
    "pixel_w":(70,110),
    "pixel_h":4,
    "resample_down":(0,4),
    "resample_up":(0,4),
}
bf_data = {
    "pixels_w":89,
    "pixels_h":4,
    "test_resample":1,
    "font_id":10,
    "font_size":21,
    "resample":1,
    "downsize_resample":0,
    "width":561,
    "blur_area":[(0,0,522,22)],
    "height":25,
    'final_width':522,
    'final_height':22,
    "x_margin":2,
    "y_margin":-3,
    "c":(40,80),
    "f":(155,205),
}

            
def find_target_pixels():
    target_a = Image.open(sys.argv[1]).convert('F')
    target_ap = get_img_pixels(target_a,None)
    best_v = 999999
    best_d = None
    for i in gen_inputs(input_info_bf):
        target_b = get_img_pixels(target_backforth(target_a,i),None)
        r = mean_squared_error(target_ap,target_b)
        if r < best_v:
            best_v = r
            best_d = i
            #print("Best: %f: %s"%(best_v,best_d))
    print(best_d)
    verify_input(best_d, input_info_bf)
    target_new = target_backforth(target_a,best_d)
    target_new.convert("RGBA").save('target_new.png')
    return((best_d["pixel_w"],best_d["resample_down"]))

#print("Target seems to be %d pixels wide and best downsized with %d (change bf vals manually!)"%find_target_pixels())

# Returns last pixel that was fully affected by text
def pixel_width(fnt, text, x_margin, img_width, pixel_width):
    fw,_ = fnt.getsize(text)
    fw += x_margin
    return int(round(float(fw*pixel_width)/img_width))

targets = {}
font_objects = {}
def get_best(bf_data,text,target_file, px=None,output=True, width_calc_drop=0):
    global font_objects
    global targets
    if px is not None:
        crop = (0,0,px,4)
    best = 9999999
    best_inp = None
    if output:
        print(bf_data)
    for i in gen_inputs(bf_data,output):
        #i["width"] = int((i["height"]*i["pixels_w"])/float(i["pixels_h"]))
        pixel_count = (i["pixels_w"],i["pixels_h"])
        
        f_key = (i["font_id"],i["font_size"])
        if f_key not in font_objects:
            font_objects[f_key] = ImageFont.truetype(fonts[i["font_id"]], i["font_size"])
        fnt = font_objects[f_key]
        pixel_w = pixel_width(fnt, text, i["x_margin"],i["width"],i["pixels_w"])
        if px is None:
            crop = (0,0,pixel_w-1,4)
            
        t_key = (pixel_count,i["test_resample"],crop)
        if t_key not in targets:
            targets[t_key] = prep_target(target_file, pixel_count, i["test_resample"],crop,i)
        
        target = targets[t_key]
        args = ()
        alt1 = gen_alternative(text, pixel_count, i["resample"], fnt, i["width"], i["height"], i["x_margin"], i["y_margin"],i)
        r = get_error(get_img_pixels(alt1,crop),target)
        if r < best:
            best_inp = i
            best_img = alt1
            best_w = fnt.getsize(text[:len(text)-width_calc_drop])[0]
            best = r
            if output:
                gen_alternative(text, pixel_count, i["resample"], fnt, i["width"], i["height"], i["x_margin"], i["y_margin"],i,dump=True)
                print("Best: %f: %s"%(best,i))
    if output:
        verify_input(best_inp, bf_data)
    if output:
        print("Best: %f: %s"%(best,best_inp))
        best_img.convert("RGBA").save('pil_text.png')
    return best_inp,best,best_w

if __name__ == "__main__":
    #bf2,_,_ = get_best(bf_data,"https://vpn.twttr.com/dana-na/auth/url_default/welcome.cgi",target_file=sys.argv[1])
    bf2,_,_ = get_best(bf_data,"https://",target_file=sys.argv[1])
    print(bf2)

# With full text:
# Best: 0.006874: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 3, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 557, 'blur_area': (0, 0, 522, 22), 'height': 23, 'final_width': 522, 'final_height': 22, 'x_margin': -1, 'y_margin': -4, 'c': 54, 'f': 220}
# Best: 0.006683: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 3, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 557, 'blur_area': (0, 0, 522, 22), 'height': 23, 'final_width': 522, 'final_height': 22, 'x_margin': -1, 'y_margin': -4, 'c': 66, 'f': 235}
# Best: 0.007030: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 3, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 557, 'blur_area': (0, 0, 522, 22), 'height': 23, 'final_width': 522, 'final_height': 22, 'x_margin': -1, 'y_margin': -4, 'c': 54, 'f': 230}
# Best: 0.006627: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 3, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 557, 'blur_area': (0, 0, 522, 22), 'height': 24, 'final_width': 522, 'final_height': 22, 'x_margin': -1, 'y_margin': -3, 'c': 66, 'f': 235}
# Best: 0.005884: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 3, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 558, 'blur_area': (0, 0, 522, 22), 'height': 25, 'final_width': 522, 'final_height': 22, 'x_margin': 0, 'y_margin': -3, 'c': 58, 'f': 208}
# Best: 0.005884: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 3, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 558, 'blur_area': (0, 0, 522, 22), 'height': 25, 'final_width': 522, 'final_height': 22, 'x_margin': 0, 'y_margin': -3, 'c': 58, 'f': 208}
# Best: 0.005870: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 3, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 558, 'blur_area': (0, 0, 522, 22), 'height': 25, 'final_width': 522, 'final_height': 22, 'x_margin': 0, 'y_margin': -3, 'c': 58, 'f': 212}    
# Best: 0.005801: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 3, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 561, 'blur_area': (0, 0, 522, 22), 'height': 25, 'final_width': 522, 'final_height': 22, 'x_margin': 2, 'y_margin': -3, 'c': 62, 'f': 228}
# Best: 0.004994: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 1, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 561, 'blur_area': (0, 0, 522, 22), 'height': 25, 'final_width': 522, 'final_height': 22, 'x_margin': 2, 'y_margin': -3, 'c': 67, 'f': 224}
# Best: 0.004941: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 1, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 561, 'blur_area': (0, 0, 522, 22), 'height': 25, 'final_width': 522, 'final_height': 22, 'x_margin': 2, 'y_margin': -3, 'c': 71, 'f': 222}
# Only https://
# Best: 0.021147: {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 1, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 561, 'blur_area': (0, 0, 522, 22), 'height': 25, 'final_width': 522, 'final_height': 22, 'x_margin': 2, 'y_margin': -3, 'c': 60, 'f': 238}
