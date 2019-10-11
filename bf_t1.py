#!/usr/bin/python
import sys
# TODO: Fix this to work for others
from Depixel import *
import bisect
import itertools
from t1.create_t1 import get_best


class TopList:
    def __init__(self, vals):
        self.size = vals
        self.max_size = 100000
        self.s = {}
    
    def add(self, name, score):
        if len(self.s) >= self.max_size:
            self.get()
                
        if name in self.s:
            self.s[name] = min(self.s[name],score)
            return
        self.s[name] = score
    
    def get(self):
        tmp = sorted([(self.s[n],n) for n in self.s.keys()])[:self.size]
        self.s = {}
        for v,k in tmp:
            self.s[k] = v
        return tmp
        
# Created using create_t1.py
i =  {'pixels_w': 89, 'pixels_h': 4, 'test_resample': 1, 'font_id': 10, 'font_size': 21, 'resample': 1, 'downsize_resample': 0, 'width': 561, 'blur_area': (0, 0, 522, 22), 'height': 25, 'final_width': 522, 'final_height': 22, 'x_margin': 2, 'y_margin': -3, 'c': 48, 'f': 190}

for k in i.keys():
    i[k] = [i[k]]

ln=3

start = "https://"
#chars = "vpntwrcom.-/"
chars = "abcdefghijklmnopqrstuvwxyz."

top = TopList2(10)
avg_score = 99999989
top.add(start,99999989)

banned = ["mm","..","::","--"] +  \
         ["".join(p) for p in itertools.product("mw",repeat=ln)] + \
         [x+x+x for x in chars]
if ln >= 3:
    banned += ["".join(p) for p in itertools.product(".:/-i",repeat=ln)]
banned.append("ap")
if "://" in banned:
    banned.remove("://")
while "www" in banned:
    banned.remove("www")

td = {0:top}
while True:
    best_v = 999999
    targets = {}
    tl = []
    for k in td.keys():
        tl = tl + td[k].get()
    td = {}
    for score,topt in tl:
        if score > avg_score:
            print("Dropping: %s"%topt)
            continue
        for alt in itertools.product(chars,repeat=ln):
            altS = "".join(alt)
            ctxt = topt+altS
            skip = False
            for b in banned:
                if b in ctxt:
                    skip = True
                    break
            if skip:
                continue
            d, r, pixel_w = get_best(i, ctxt,output=False, target_file=sys.argv[1],width_calc_drop=ln-1)
            pixel_w = 1
            #print("fs: %d, mx: %d, my:%d"%(d["font_size"],d["x_margin"],d["y_margin"]))
            if pixel_w not in td:
                td[pixel_w] = TopList2(100)
            top = td[pixel_w]
            best_d = ctxt
            best_v = r
            if ln > 1:
                top.add(best_d[:-ln+1],best_v)
            else:
                top.add(best_d,best_v)
    
    scores = []
    for k in td.keys():
        for score,txt in td[k].get():
            scores.append(score)
    #avg_score = sorted(scores)[:30][-1]
    print("LOOP: %f"%avg_score)
    print([(x,td[x].get()) for x in td.keys()])
    #print(top_px)
    #print(top.l)
    
