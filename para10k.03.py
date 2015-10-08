# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as souper
from html2text import html2text as h2t
import json
import requests

s_url = 'http://www.sec.gov/Archives/edgar/data/9092/000000909214000004/bmi-20131231x10k.htm'
# comment line above & uncoment next 3 lines to enable handling URL as argument
#import sys
#if len(sys.argv) > 2 and sys.argv[2][:5].find('http') >= 0 else s_url
#    s_url = sys.argv[2] #

o_SEC = requests.get(s_url)

t_SEC = h2t(o_SEC.text)

with open('/tmp/document.txt','w') as f_SEC:
    f_SEC.write(t_SEC)

t_sec = open('/Temp/document.txt','r').read()

o_sec = souper(o_SEC.text, 'html.parser')

l_texts = o_sec.findAll(text=True)

def f_displayable(element):
    if element.parent.name in ['table', 'style', 'script', '[document]', 'head', 'title']:
        return False
    elif str(element)[:4] == '<!--' and str(element)[-3:] == '-->':
        return False
    return True

l_displayed_texts = filter(f_displayable, l_texts)

l_para = []
m_apnd = l_para.append

for s_trng in l_displayed_texts:
    s_txt = h2t(s_trng).strip()
    n_len = len(s_txt)
    n_found = s_txt.find('$')
    if n_found >= 1 and n_found != n_len:
        i_ndx = t_sec.find(s_txt)
        m_apnd({'start':i_ndx, 'end':i_ndx + n_len, 'text':s_txt})

with open('/tmp/paragraphs.txt','w') as f_para:
    f_para.write(json.dumps(l_para))
