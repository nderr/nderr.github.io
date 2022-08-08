#!/usr/bin/env python3

import yaml
import doi2cite as d2c
import argparse as arg
import sys

parser = arg.ArgumentParser('./write_index.py')

parser.add_argument('infile',type=str,help='file to process')
args = parser.parse_args()

fn_in = args.infile

if not fn_in[-3:] == '.in':
    print('infile must end with \".in\"')
    sys.exit(-1)

fn_out = fn_in[:-3]

def start_html_ordered_list(fout,key='key',pad='0em',tot=-1):

    print("<style>",file=fout)
    print(f'ol.{key:s}>li::marker {{',file=fout)
    print("  content: \"[\" counter(list-item) \"]  \";",file=fout)
    print("}",file=fout)
    print(f'ol.{key:s} {{ padding-left: {pad:s}; }}',file=fout)
    print(f'ol.{key:s}>li:not(:last-child) {{',file=fout)
    print("  margin-bottom: 0.5em;",file=fout)
    print("}",file=fout)
    print("</style>",file=fout)

    if tot > 0:
        print(f'<ol reversed class="{key:s}" start="{tot:d}">',file=f_out)
    else:
        print(f'<ol reversed class="{key:s}">',file=f_out)

def list_item(fout,doi,justified=False):

    if justified:
        stags = '<li><p style="text-align:justify;margin:0;">'
        etags = '</p></li>'
    else:
        stags = '<li>'
        etags = '</li>'

    print(f'{stags:s}{doi.citation():s}{etags:s}',file=fout)

def end_html_ordered_list(fout):
    print('</ol>',file=fout)

# read in yaml
with open('info.yaml','r') as stream:
    try:
        info = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

emphs        = 'N.J. Derr'
proper_nouns = info['proper_nouns']
justified    = True

with open(fn_in,'r') as f_in, open(fn_out,'w') as f_out:

    for line in f_in:

        line = line.rstrip()

        if line.startswith('%%% PREPRINTS %%%'):


            #tot = len(info['preprints'])
            #for p in info['papers']:
            #    if 'selected' in p:
            #        tot = tot+1

            start_html_ordered_list(f_out)

            for obj in info['preprints']:

                arxiv_str = obj['arxiv']
                descr     = obj['descr']

                doi = d2c.DOI(arxiv_str,arxiv=True,emphs=emphs,links=True,
                    propers=proper_nouns,output='html',descr=descr)

                list_item(f_out,doi,justified=justified)

            #end_html_ordered_list(f_out)

        elif line.startswith('%%% PUBLIST %%%'):

            #start_html_ordered_list(f_out)

            for p in info['papers']:

                doi = d2c.DOI(p['doi'],output='html',emphs=emphs,links=True,
                        propers=proper_nouns)

                if 'cofirst' in p:
                    doi.set_cofirst(True)

                if 'arxiv' in p:
                    doi.add_arxiv(str(p['arxiv']))

                if 'selected' in p:
                    list_item(f_out,doi,justified=justified)

            end_html_ordered_list(f_out)

        else:
            print(line,file=f_out)
