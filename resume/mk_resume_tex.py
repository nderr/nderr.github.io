import sys
import jinja2 as j2
import doi2cite as d2c

from yaml import safe_load, YAMLError

if __name__ == '__main__':

    # load jinja template from FS
    loader = j2.FileSystemLoader('.')

    # create jinja environment, use conventions from BetterJinja ext
    env = j2.Environment(
        block_start_string="((*",
        block_end_string="*))",
        variable_start_string="(((",
        variable_end_string=")))",
        comment_start_string="((=",
        comment_end_string="=))",
        loader=loader,
        undefined=j2.StrictUndefined
    )

    # load template
    template_file = 'resume.tex.j2'
    template = env.get_template(template_file)

    # read in info.yaml
    with open('./info_res.yaml', 'r') as f:
        info = safe_load(f)

    info['selected'] = []
    for p in info['papers']:
        if 'selected' in p and p['selected']:
            p['cite'] = d2c.DOI(p['doi'],silent=True)
            p['cite'].add_proper_nouns(info['proper_nouns'])
            info['selected'].append(p['cite'])

    info['selected'].sort(key=lambda x: x.cited_by(),reverse=True)

    # render the template with the given context
    rendered = template.render(info)
    
    print(rendered)
