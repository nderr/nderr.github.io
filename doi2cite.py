#!/usr/bin/env python3

import requests as req
import argparse as arg
import sys

# class representing a DOI
class DOI:

    arxiv_doi    = lambda s : f'10.48550/ARXIV.{s:s}'
    output_types = ['tex','markdown','html']
    emph_types   = ['bold','ital']

    def set_cofirst(self,cof):
        self.cofirst = cof

    def set_links(self,links):
        self.links = links

    def add_arxiv(self,arxiv_num):

        if self.info['publisher'] == 'arXiv':
            return

        self.arxiv = DOI(DOI.arxiv_doi(arxiv_num))

    def bold(self,s):
        if self.output == 'tex':
            return f'\\textbf{{{s:s}}}'
        elif self.output == 'markdown':
            return f'**{s:s}**'
        elif self.output == 'html':
            return f'<b>{s:s}</b>'

    def ital(self,s):
        if self.output == 'tex':
            return f'\\textit{{{s:s}}}'
        elif self.output == 'markdown':
            return f'*{s:s}*'
        elif self.output == 'html':
            return f'<em>{s:s}</em>'

    def col(self,s,color):
        if color == '':
            return s
        elif self.output == 'tex':
            return f'\\textcolor{{{color:s}}}{{{s:s}}}'
        elif self.output == 'markdown' or self.output == 'html':
            return f'<span style=\"color:{color:s}\">{s:s}</span>'

    def link(self,s,url):
        if self.output == 'html':
            return f'<a href="{url:s}" class="link"><span>{s:s}</span></a>'

    def emph(self,s,t,c):


        if t == 'bold':
            return self.bold(self.col(s,c))
        elif t == 'ital':
            return self.ital(self.col(s,c))
        else:
            print(f'emph type must be one of:')
            for t in DOI.emph_types:
                print(f'  {t:s}')
            sys.exit(-1)

    def __init__(self,doi,silent=False):


        # go get citation information as JSON
        url = f'https://doi.org/{doi:s}'
        headers = {'accept': 'application/vnd.citationstyles.csl+json'}

        if not silent:
            print(f'Fetching DOI {doi:s}')
        r = req.get(url,headers=headers)

        # check for success
        if r.status_code != 200:
            print(f'failed with code {r.status_code:d} ({r.text:s})')
            sys.exit(-1)

        self.info = r.json()

        self.links = False
        self.emphs = []
        self.output = 'tex'
        self.propers = []
        self.arxiv = None
        self.cofirst = None

    def add_proper_nouns(self,propers):
        for p in propers:
            if p not in self.propers:
                self.propers.append(p)

    def set_output(self,output):

        if output in DOI.output_types:
            self.output = output

        else:
            print('output type must be one of:')
            for ot in DOI.output_types:
                print(f'  {ot:s}') 
            sys.exit(-1)
    
    # name - name to ephasize
    # color - text color for name
    # typ - 1=bold, 2=italics
    def add_emph_name(self,name,color='',typ='bold'):

        contains = False
        for n,t,c in self.emphs:
            if n == name:
                return

        self.emphs.append((name,typ,color))


    # static function to spit out name
    def name(self,author):

        # get first name(s) and grab initials
        g  = author['given']
        ns = g.split()
        inits = [w[0] for w in ns]

        # get family name
        l = author['family']

        # assemble initials
        out = ''
        for i in inits:
            out += f'{i:s}.'

        # add family name
        out += f' {l:s}'

        for n,t,c in self.emphs:

            if n == out:

                # double curlies to escape
                out = out.replace(n,self.emph(n,t,c))

        return out

    # helper function to spit out citation
    def author_list(self):

        out = ''
        auth = self.info['author']
        n_auth = len(self.info['author'])

        # if one author, just give name + period
        if n_auth == 1:

            return self.name(auth[0])

        # if two, name1 and name2
        elif n_auth == 2:

            a1 = self.name(auth[0])
            a2 = self.name(auth[1])

            if self.cofirst is not None:
                return f'{a1:s}* and {a2:s}*'

        # if more, separate first n-1 with commas
        else:

            out = ''
            for i,a in enumerate(auth):
            
                if i < n_auth-1:

                    if i < 2 and self.cofirst is not None:
                        out += self.name(a) + '*, '
                    else:
                        out += self.name(a) + ', '
                else:
                    out += f'and {self.name(a):s}'

            return out

    def journal_info(self):

        # check if arxiv
        if self.info['publisher'] == 'arXiv':

            year = self.info['issued']['date-parts'][0][0]
            arxiv_num = self.info['DOI'].split('ARXIV.')[-1]
            return f'arXiv: {arxiv_num:s}'

        # otherwise, used jouranl formula
        out = self.info['container-title']

        # add volume
        out += ' ' + self.bold(self.info['volume'])

        # add page
        if "page" in self.info:
            out += f', {self.info["page"]:s}'
        elif "article-number" in self.info:
            out += f', {self.info["article-number"]:s}'

        # PNAS hack
        elif self.info['container-title']== \
                'Proceedings of the National Academy of Sciences':

            num = int(self.info['DOI'].split('pnas.')[-1])

            out += f', e{num:d}'

        

    #%    pag = obj['first-page']

        return out

    def citation(self):

        auths = self.author_list()

        # send to lower case
        title = self.info['title'].lower()

        # capitalize any proper nouns
        for p in self.propers:
            title = title.replace(p.lower(),p)

        # capitalize first letter and italicize
        title = self.ital(title[0].upper() + title[1:])

        if self.links:
            title = self.link(title,self.info["URL"])

        j_info = self.journal_info()
        year = self.info['issued']['date-parts'][0][0]

        out = f'{auths:s}. {title:s}. {j_info:s} ({year:d}).'

        if self.arxiv is not None:
            a_link = self.link('arXiv',self.arxiv.info['URL'])
            out += f' [{a_link:s}]'

        return out

if __name__ == '__main__':

    # set up arguments
    parser = arg.ArgumentParser('./doi2cite.py')
    parser.add_argument('doi',type=str,help='a DOI string representing a citation')
    parser.add_argument('-t','--type',type=str,default='tex',dest='type',
            help='type of output (tex, markdown, plaintext)')
    parser.add_argument('-e','--emph',nargs='+',dest='emph',action='append',
            help='list of quoted names to emphasize')
    args = parser.parse_args()

    doi = DOI(args.doi)
    doi.set_output(args.type)

    if args.emph is not None:
        for e in args.emph:


            if len(e) == 1:
                doi.add_emph_name(e[0])
            elif len(e) == 2:
                doi.add_emph_name(e[0],typ=e[1])
            else:
                doi.add_emph_name(e[0],typ=e[1],color=e[2])

    print(doi.citation())
