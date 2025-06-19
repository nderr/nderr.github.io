#!/usr/bin/env python

import yaml
import argparse as arg
import sys
import numpy as np

sys.path.append('..')

import doi2cite as d2c

parser = arg.ArgumentParser('./write_index.py')

parser.add_argument('infile',type=str,help='file to process')
args = parser.parse_args()

fn_in = args.infile

if not fn_in[-3:] == '.in':
    print('infile must end with \".in\"')
    sys.exit(-1)

fn_out = fn_in[:-3]

# read in yaml
with open('../info.yml','r') as stream:
    try:
        info = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

emphs        = 'N.J. Derr'
proper_nouns = info['proper_nouns']
justified    = False

with open(fn_in,'r') as f_in, open(fn_out,'w') as f_out:

    did_preprints = False

    for line in f_in:

        line = line.rstrip()

        if line.startswith('%%% JOBS %%%'):

            for i_d,job in enumerate(info['experience']):

                pos  = job['position']
                empl = job['employer']
                org  = job['organization']
                date = str(job['date'])

                print(f'{empl:s}, {org:s} \hfill {date:s}\\\\',file=f_out)
                print(f'\mbox{{}}\hspace{{1em}}{pos:s} \hfill',file=f_out)
                if 'advisor' in job:
                    print(f'\\\\\mbox{{}}\hspace{{1em}}Advisor: {job["advisor"]:s} \hfill',file=f_out,end='')

                if i_d < len(info['experience'])-1:
                    print('\\\\[0.5em]',file=f_out)

        elif line.startswith('%%% JOURNALS %%%'):

            for s in info['service']:
                print(f'{s["name"]:s} \\hfill {s["range"]:s} \\\\',file=f_out)

                print('\\begin{adjustwidth}{2em}{2em}',file=f_out)

                print('\\vspace{-2em}',file=f_out)

                if np.isscalar(s['organization']):
                    org = s['organization']
                    print(f'\\textit{{{org:s}}}',file=f_out)
                else:
                    for i_j,j in enumerate(s['organization']):

                        if i_j == 0:
                            print(f'\\textit{{{j:s}}}',file=f_out, end='')
                        else:
                            print(f', \\textit{{{j:s}}}',file=f_out, end='')

#                        if i_j == len(s['organization'])-1:
#                            print('\\\\',file=f_out)

                print('\\end{adjustwidth}',file=f_out)


        elif line.startswith('%%% AWARDS %%%'):

            for i_t,awd in enumerate(info['awards']):

                print(f'{awd["name"]:s} \\hfill {awd["awarder"]:s}, {awd["date"]:s}',end='',file=f_out)

                if 'note' in awd:

                    note_s = awd["note"].replace('$','\\$')
                    note_s = note_s.replace('%','\\%')

                    print(f'\\\\\\mbox{{}}\\hspace{{1em}}\\textit{{{note_s:s}}}',file=f_out)

                print('\\\\',file=f_out,end='')
                if i_t == len(info['awards'])-1:
                    print('[-1em]',file=f_out)
                print('',file=f_out)

        elif line.startswith('%%% TEACHING %%%'):
            print('\\mbox{}\\textit{Head Instructor (MIT):}\\\\',file=f_out)
            print('\\begin{tabular}{lll}',file=f_out)
            print('\\textbf{Course Number} & \\textbf{Course Name} & \\textbf{Term} \\\\',file=f_out)
            for i_t,cl in enumerate(info['teaching']['head']):

                print(f'{cl["code"]:s} & {cl["name"]:s} & {cl["term"]:s} \\\\',file=f_out)

            #print('18.384 & Undergraduate Seminar in Physical Mathematics & Fall 2023 \\\\',file=f_out)
            print('\\color{white}  Engineering Sciences 240 &\\color{white}  Advanced Scientific Computing II   &\\color{white}  Spring 2018 \\\\',file=f_out)
            print('\\end{tabular} \\\\',file=f_out)

            print('\\mbox{}\\textit{Recitation Leader (MIT):}\\\\',file=f_out)
            print('\\begin{tabular}{llll}',file=f_out)
            print('\\textbf{Course Number} & \\textbf{Course Name} & \\textbf{Lead Instructor} & \\textbf{Term} \\\\',file=f_out)
            for i_t,cl in enumerate(info['teaching']['recitation']):

                if 'notes' in cl and 'Bok' in cl['notes']:
                    blip = '*'
                else:
                    blip = ''


                print(f'{cl["code"]:s}{blip:s} & {cl["name"]:s} & {cl["prof"]:s} & {cl["term"]:s} \\\\',file=f_out)

            print('\\color{white} ',file=f_out)

            print('\\color{white}  Engineering Sciences 240* &\\color{white}  Advanced Scientific Computing II  &\\color{white}  Prof. Chris H. Rycroft  &\\color{white}  Spring 2018 \\\\',file=f_out)
            print('\\end{tabular}',file=f_out)

            print('\\\\\\mbox{}\\textit{Teaching Fellow (Harvard):}\\\\',file=f_out)
            print('\\begin{tabular}{llll}',file=f_out)
            print('\\textbf{Course Number} & \\textbf{Course Name} & \\textbf{Lead Instructor} & \\textbf{Term} \\\\',file=f_out)
            for i_t,cl in enumerate(info['teaching']['TA']):

                if 'notes' in cl and 'Bok' in cl['notes']:
                    blip = '*'
                else:
                    blip = ''


                print(f'{cl["code"]:s}{blip:s} & {cl["name"]:s} & {cl["prof"]:s} & {cl["term"]:s} \\\\',file=f_out)

            print('\\end{tabular}',file=f_out)


        elif line.startswith('%%% THESES %%%'):
            
            for i_d,work in enumerate(info['theses']):

                auth = work['author']
                adv  = work['advisor']
                title= work['title']
                year = str(work['year'])
                typ  = work['type']

                print(f'\\textbf{{{auth:s}}}, \\textit{{{title:s}}}, {typ:s}, advised by {adv:s} ({year:s}).',file=f_out)

                if i_d < len(info['theses'])-1:
                    print('\\\\[0.5em]',file=f_out)


        elif line.startswith('%%% SCHOOLS %%%'):

            for i_d,deg in enumerate(info['education']):

                inst = deg['institution']

                print(f'{inst:s} \\hfill ',file=f_out,end='')

                try:
                    for i,d in enumerate(deg['degrees']):
                        inits = d['initials']

                        #if 'modifier' in d:
                        #    inits += ' ' + d['modifier']

                        syr = d['start_year']
                        eyr = d['end_year']
                        yr  = f'{syr:d}--{eyr:d}'

                        if i > 0:
                            print(', ',file=f_out,end='')
                        print(f'{yr:s}',end='',file=f_out) 
                except KeyError as exc:
                    print('bad key!')
                    print(i)
                    print(d)
                    print(deg)
                    print(exc)
                    sys.exit(-1)

                print('\\\\',file=f_out)

                d_str = f'{inits:s} {deg["subject"]:s}'
                
                print(f'\mbox{{}}\hspace{{1em}}{d_str:s}',file=f_out,end='')

                if 'comment' in deg:
                    print(f'\\\\\\mbox{{}}\\hspace{{1em}}{deg["comment"]:s}',file=f_out,end='')

                print('\hfill ',file=f_out,end='')

                if (i_d < len(info['education'])-1):
                    print('\\\\[0.5em]',file=f_out)
                else:
                    print('',file=f_out)


        elif line.startswith('%%% INVITED %%%'):

            first_printed=False
            for i_t,talk in enumerate(info['presentations']):

                if 'invited' not in talk or not talk['invited']:
                    continue

                title = talk['title']
                venue = talk['venue']
                date  = str(talk['date'])
                city  = talk['city']

                if first_printed:
                    print('\\\\[0.5em]',file=f_out)

                print(f'\\textit{{{title:s}}}, {venue:s}, {city:s}, {date:s}.',file=f_out)
                first_printed = True

        elif line.startswith('%%% CONTRIBUTED %%%'):

            first_printed=False
            for talk in info['presentations']:

                if 'invited' in talk and talk['invited']:
                    continue

                title = talk['title']
                venue = talk['venue']
                date  = str(talk['date'])
                city  = talk['city']

                if first_printed:
                    print('\\\\[0.5em]',file=f_out)

                print(f'\\textit{{{title:s}}}, {venue:s}, {city:s}, {date:s}.',file=f_out)
                first_printed=True

        elif line.startswith('%%% PREPRINTS %%%'):

            did_preprints = True
#            print('\\begin{bibenum*}',file=f_out)

            first=True
            for obj in info['preprints']:

                arxiv_str = obj['arxiv']
                descr     = obj['descr']

                doi = d2c.DOI(arxiv_str,arxiv=True,emphs=emphs,links=False,
                    propers=proper_nouns,output='tex',descr=descr)

                doi.add_arxiv_journ(arxiv_str)

                if not first:
                    print('\\\\[0.5em]',file=f_out)

                first = False
                print(f'{doi.citation():s}',file=f_out)

        elif line.startswith('%%% PUBLIST %%%'):

            first = True
            for p in info['papers']:

                doi = d2c.DOI(p['doi'],output='tex',emphs=emphs,links=False,
                        propers=proper_nouns)

                if 'cofirst' in p:
                    doi.set_cofirst(True)

                if first:
                    if did_preprints:
                        print('\\\\[0.5em]',file=f_out)
                    first = False
                else:
                    print('\\\\[0.5em]',file=f_out)
                print(f'{doi.citation():s}',file=f_out)

#            print('\\end{bibenum*}',file=f_out)

        else:
            print(line,file=f_out)
