# -*- encoding: utf-8 -*-
'''
@File    :   getfilter.py
@Time    :   2022/07/22
@Author  :   Mingyu Li
@Contact :   lmytime@hotmail.com
'''


import os
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

r = requests.get('http://svo2.cab.inta-csic.es/theory/fps/index.php')
r.encoding = r.apparent_encoding
bsoj = BeautifulSoup(r.content, 'lxml', from_encoding=r.encoding)

namelist = bsoj.findAll("a", {"onmouseout": "UnTip()"})
telescope = [name.text for name in namelist][1:]

for tel in tqdm(telescope):
    print(tel)
    url = f"http://svo2.cab.inta-csic.es/theory/fps/index.php?gname={tel}"
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    bsoj = BeautifulSoup(r.content, 'lxml', from_encoding=r.encoding)
    namelist = bsoj.findAll("a", {"onmouseout": "UnTip()"}, "href")
    instrument = [name.text for name in namelist][202: -12]
    if(len(instrument) == 0):
        instrument.append("")
    print(instrument)
    for ins in instrument:
        url = f"http://svo2.cab.inta-csic.es/theory/fps/index.php?gname={tel}&gname2={ins}"
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        bsoj = BeautifulSoup(r.content, 'lxml', from_encoding=r.encoding)
        namelist = bsoj.findAll(
            "td", "filfld", string=re.compile(f"{tel}/[\S].[\S]"))
        fils = [name.text for name in namelist]
        for fil in fils:
            print(fil)
            url = f"http://svo2.cab.inta-csic.es/theory/fps/getdata.php?format=ascii&id={fil}"
            r = requests.get(url, allow_redirects=True)
            os.makedirs(f"filters/{tel}", exist_ok=True)
            with open(f"filters/{fil}.dat", 'wb') as f:
                f.write(r.content)
    # Remove the last line of the file, to download all files
    break