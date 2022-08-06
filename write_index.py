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

arxiv2doi = lambda an : f'10.48550/ARXIV.{an:s}'

def setup_html_ordered_list(fout,key='key',pad='1.9em'):

    print("<style>",file=fout)
    print(f'ol.{key:s}>li::marker {{',file=fout)
    print("  content: \"[\" counter(list-item) \"]  \";",file=fout)
    print("}",file=fout)
    print(f'ol.{key:s} {{ padding-left: {pad:s}; }}',file=fout)
    print(f'ol.{key:s}>li:not(:last-child) {{',file=fout)
    print("  margin-bottom: 1em;",file=fout)
    print("}",file=fout)
    print("</style>",file=fout)


with open(fn_in,'r') as f_in, open(fn_out,'w') as f_out:

    for line in f_in:

        line = line.rstrip()

        if line.startswith('%%% PREPRINTS %%%'):


            key = 'brackets'
            setup_html_ordered_list(f_out,key=key)


            # read in yaml
            with open('info.yaml','r') as stream:
                try:
                    info = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)

            tot = len(info['papers']) + len(info['preprints'])

            print(f'<ol reversed class="{key:s}" start="{tot:d}">',file=f_out)

            np = len(info['preprints'])
            for i,arxiv_str in enumerate(info['preprints']):

                doi = d2c.DOI(arxiv2doi(str(arxiv_str)))
                doi.set_output('html')
                doi.add_emph_name('N.J. Derr')
                doi.set_links(True)
                doi.add_proper_nouns(info['proper_nouns'])
                print(f'<li>{doi.citation():s}\n\n</li>',file=f_out)

            print("</ol>",file=f_out)

        elif line.startswith('%%% PUBLIST %%%'):

            key = 'brackets'
            setup_html_ordered_list(f_out,key=key)

            print(f'<ol reversed class="{key:s}">',file=f_out)

            # read in yaml
            with open('info.yaml','r') as stream:
                try:
                    info = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)

            np = len(info['papers'])
            for p in info['papers']:

                doi = d2c.DOI(p['doi'])
                doi.set_output('html')
                doi.add_emph_name('N.J. Derr')
                doi.set_links(True)
                doi.add_proper_nouns(info['proper_nouns'])

                if 'arxiv' in p:
                    doi.add_arxiv(str(p['arxiv']))

                print(f'<li>{doi.citation():s}\n\n</li>',file=f_out)

            print("</ol>",file=f_out)
        else:
            print(line,file=f_out)
